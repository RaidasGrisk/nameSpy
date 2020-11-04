from data_sources.google import get_google_search_result_items, google_translate

from job_titles.ner_hard_match import get_job_titles as get_job_titles_1
from job_titles.ner_flair_model import get_job_titles as get_job_titles_2

from helpers import get_filtered_input
from private import proxy_dict
from log_config import handler as log_handler

from helpers import get_nlp_models
nlp_models = get_nlp_models()


def make_output(input,
                ner_threshold=0.95,
                country_code='en',
                filter_input=True,
                use_proxy=1,
                debug=0):

    # make output: name
    if filter_input:
        output_name_part = get_filtered_input(input.title(), nlp_models)
        if not output_name_part.get('input'):
            return output_name_part
    else:
        output_name_part = {'input': input}

    proxies = proxy_dict if use_proxy == 1 else {}

    # make output: job titles
    # 1. scrape google search
    # 2. translate all to english
    # 3. run models to detect job titles
    # can not improve this with concurrency
    google_data = get_google_search_result_items(
        output_name_part['input'],
        exact_match=True,
        proxies=proxies,
        country_code=country_code
    )

    # can I remove this?
    if not google_data:
        return {'warning': 'google did not return the search results'}

    google_data = google_translate(google_data, proxies=proxies)

    job_titles_1 = get_job_titles_1(google_data)
    job_titles_2 = get_job_titles_2(google_data, ner_threshold=ner_threshold)

    # combine both job detection methods into one dict
    for key, value in job_titles_2.items():
        if job_titles_1.get(key):
            job_titles_1[key]['count'] += 1
            job_titles_1[key]['sources'].update(value['sources'])
        else:
            job_titles_1.update({key: value})
    job_titles = job_titles_1

    # sort by job title count
    job_titles = dict(sorted(job_titles.items(),
                             key=lambda x: x[1].get('count'),
                             reverse=True))

    # convert sets to list for JSON + do other cleaning
    for title, _ in job_titles.items():
        job_titles[title]['sources'] = \
            list(job_titles[title]['sources'])

    output_job_titles_part = {'titles': job_titles}

    # make output: log
    output_log_part = {'log': [str(i) for i in log_handler.log]}

    # combine parts into final output
    output = {
        **output_name_part,
        **output_job_titles_part,
        **[output_log_part if debug == 1 else {}][0],
    }

    return output


# -------------- #
from flask import Flask
from flask import jsonify
from flask_restful import Resource, Api, reqparse
import os
import traceback

app = Flask(__name__)
api = Api(app)
app.config['JSON_SORT_KEYS'] = False  # do not sort data


class job_title(Resource):
    def get(self):

        parser = reqparse.RequestParser()
        parser.add_argument('input', type=str, required=True)
        parser.add_argument('filter_input', type=int, default=1)
        parser.add_argument('use_proxy', type=int, default=1)
        parser.add_argument('ner_threshold', type=float, default=0.95)
        parser.add_argument('country_code', type=str, default='us')
        parser.add_argument('debug', type=int, default=0)
        args = parser.parse_args()

        try:
            output = make_output(**args)
            status_code = 200
        except Exception as e:
            output = {
                'error': 'something went wrong :(',
                'traceback': str(e),
                'full_traceback': str(traceback.format_exc()),
                'log': [str(i) for i in log_handler.log]
            }
            status_code = 500  # HTTP_500_INTERNAL_SERVER_ERROR
        finally:
            # clear the log here because otherwise if an exception is caught
            # the log will not be cleared if it is done inside the main function
            log_handler.flush()

        output = jsonify(output)
        output.status_code = status_code

        # this or cant communicate with javascript axios
        output.headers.add('Access-Control-Allow-Origin', '*')

        return output


api.add_resource(job_title, '/api/job_title', endpoint='/job_title')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
