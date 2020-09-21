from data_sources.google import get_google_search_result_items, google_translate

from job_titles.ner_hard_match import get_job_titles as get_job_titles_1
from job_titles.ner_flair_model import get_job_titles as get_job_titles_2

from helpers import get_entities, process_entities
from helpers import get_api_output_head_from_input_entities
import globals
from private import proxy_dict
from log_cofig import handler as log_handler


def get_job_title(input, ner_threshold=0.95, country_code='en', filter_input=True, use_proxy=1, debug=0):

    output = dict()

    if filter_input:
        entities = get_entities(input.title(), globals.nlp_models)
        person_name = process_entities(entities)
        output.update(get_api_output_head_from_input_entities(entities))
        if not person_name:
            return {'warning': 'I am built to recognize names, but I don`t see any :('}
    else:
        output.update(get_api_output_head_from_input_entities({'PERSON': [input.title()]}))
        person_name = input

    proxies = proxy_dict if use_proxy == 1 else {}

    google_data = get_google_search_result_items(person_name,
                                                 exact_match=True,
                                                 proxies=proxies,
                                                 country_code=country_code)

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

    # sorted(job_titles, key=job_titles.get('count'))
    job_titles = dict(sorted(job_titles.items(), key=lambda x: x[1].get('count'), reverse=True))

    # convert sets to list for JSON + do other cleaning
    for title, _ in job_titles.items():
        job_titles[title]['sources'] = list(job_titles[title]['sources'])

    # make final output
    output['google'] = {'titles': job_titles}

    if debug == 1:
        output['log'] = [str(i) for i in log_handler.log]

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
            output = get_job_title(**args)
        except Exception as e:
            output = {'something went wrong': ':(',
                      'traceback': str(e),
                      'full_traceback': str(traceback.format_exc()),
                      'log': [str(i) for i in log_handler.log]}
        finally:
            # clear the log here because otherwise if an exception is caught
            # the log will not be cleared if it is done inside the main function
            log_handler.flush()

        # this or cant communicate with javascript axios
        output = jsonify(output)
        output.headers.add('Access-Control-Allow-Origin', '*')

        return output


api.add_resource(job_title, '/api/job_title', endpoint='/job_title')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
