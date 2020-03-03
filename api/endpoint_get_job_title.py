from data_sources.google import google_search_scrape, google_translate

from job_titles.find_job_titles import get_job_titles as get_job_titles_1
from job_titles.core_nlp_ner import get_job_titles as get_job_titles_2

from helpers import get_entities, process_entities
from helpers import get_api_output_head_from_input_entities
from globals import nlp_models
import re


def get_job_title(input):

    entities = get_entities(input, nlp_models)
    print(entities)
    person_name = process_entities(entities)

    if not person_name:
        return {'warning': 'I am built to recognize names, but I dont see any :('}

    print('Google search')
    google_data = google_search_scrape(person_name, exact_match=True, pages=1)
    print('Google translate')
    google_data = google_translate(google_data)

    print('Job titles')
    job_titles_1 = get_job_titles_1(google_data)
    job_titles_2 = get_job_titles_2(google_data)
    job_titles_combined = job_titles_1 + job_titles_2

    job_titles = {}
    for source_dict in job_titles_combined:
        for source, titles in source_dict.items():
            for title in titles:
                title = re.sub(r'\W+', ' ', title)
                title = title.lower()
                if title in job_titles.keys():
                    job_titles[title].append(source)
                else:
                    job_titles[title] = [source]

    # job_titles = {'py': job_titles_1, 'stanfordNLP': job_titles_2}

    # making final output
    output = dict()
    output.update(get_api_output_head_from_input_entities(entities))

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
        args = parser.parse_args()
        try:
            output = get_job_title(args['input'])
        except Exception as e:
            output = {'something went wrong': ':(', 'traceback': str(e)}

        # this or cant communicate with javascript axios
        output = jsonify(output)
        output.headers.add('Access-Control-Allow-Origin', '*')

        return output


api.add_resource(job_title, '/api/job_title', endpoint='/job_title')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
