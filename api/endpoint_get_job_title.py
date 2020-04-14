from data_sources.google import google_search_scrape, google_translate

from job_titles.ner_hard_match import get_job_titles as get_job_titles_1
from job_titles.ner_flair_model import get_job_titles as get_job_titles_2

from helpers import get_entities, process_entities
from helpers import get_api_output_head_from_input_entities
import globals
from private import tor_password

from proxy.proxy_generator import ProxyChanger, check_if_can_connect_to_google_translate

proxy_changer = ProxyChanger(tor_password=tor_password)


def get_job_title(input, ner_threshold=0.95, google_search_loc='en', filter_input=True):

    output = dict()

    if filter_input:
        entities = get_entities(input.title(), globals.nlp_models)
        print(entities)
        person_name = process_entities(entities)
        output.update(get_api_output_head_from_input_entities(entities))
        if not person_name:
            return {'warning': 'I am built to recognize names, but I dont see any :('}
    else:
        person_name = input

    # proxy configure
    proxy_changer.get_new_proxy(minutes_between_changes=1, connection_check=check_if_can_connect_to_google_translate)
    proxies = {'http': 'socks5h://localhost:9050', 'https': 'socks5h://localhost:9050'}

    print('Google scrape')
    # TODO: passing location (google_search_loc) triggers capthca. Modified to pass None to overcome this
    google_data = google_search_scrape(person_name, exact_match=True, proxies=None, loc=None)  # loc = google_search_loc

    if not google_data:
        return {'warning': 'google did not return the search results'}

    google_data = google_translate(google_data, proxies=proxies)

    print('Job titles')
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

    return output


# -------------- #
from flask import Flask
from flask import jsonify
from flask_restful import Resource, Api, reqparse
import os

app = Flask(__name__)
api = Api(app)
app.config['JSON_SORT_KEYS'] = False  # do not sort data


class job_title(Resource):
    def get(self):

        parser = reqparse.RequestParser()
        parser.add_argument('input', type=str)
        parser.add_argument('ner_threshold', type=float, default=0.95)
        parser.add_argument('google_search_loc', type=str, default='us')
        parser.add_argument('filter_input', type=int, default=1)
        args = parser.parse_args()
        try:
            output = get_job_title(args['input'], args['ner_threshold'], args['google_search_loc'], args['filter_input'])
        except Exception as e:
            output = {'something went wrong': ':(', 'traceback': str(e)}

        # this or cant communicate with javascript axios
        output = jsonify(output)
        output.headers.add('Access-Control-Allow-Origin', '*')

        return output


api.add_resource(job_title, '/api/job_title', endpoint='/job_title')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
