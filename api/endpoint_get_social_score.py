from data_sources.instagram import instagram_users
from data_sources.wikipedia import get_wiki_search
from data_sources.twitter import get_twitter_users
from data_sources.google import get_google_search_num_items

from helpers import get_entities, process_entities
from helpers import get_api_output_head_from_input_entities
import globals


def get_social_score(input):

    entities = get_entities(input, globals.nlp_models)
    print(entities)
    person_name = process_entities(entities)

    if not person_name:
        return {'warning': 'I am built to recognize names, but I dont see any :('}

    print('Google counts')
    google_counts = get_google_search_num_items(person_name)
    print('Wikipedia')
    wiki_data = get_wiki_search(person_name)
    print('Instagram')
    instagram_data = instagram_users(person_name)
    print(instagram_data)
    print('Twitter')
    twitter_data = get_twitter_users(person_name)

    # making final output
    output = dict()
    output.update(get_api_output_head_from_input_entities(entities))
    output['google'] = {'items': google_counts}
    output['wikipedia'] = wiki_data
    output['twitter'] = twitter_data
    output['instagram'] = instagram_data

    return output


# -------------- #
from flask import Flask
from flask import jsonify
from flask_restful import Resource, Api, reqparse
import os

app = Flask(__name__)
api = Api(app)
app.config['JSON_SORT_KEYS'] = False  # do not sort data


class social_score(Resource):
    def get(self):

        parser = reqparse.RequestParser()
        parser.add_argument('input', type=str)
        args = parser.parse_args()
        try:
            output = get_social_score(args['input'])
        except:
            output = {'something went wrong': ':('}

        # this or cant communicate with javascript axios
        output = jsonify(output)
        output.headers.add('Access-Control-Allow-Origin', '*')

        return output


api.add_resource(social_score, '/api/social_score', endpoint='/social_score')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))