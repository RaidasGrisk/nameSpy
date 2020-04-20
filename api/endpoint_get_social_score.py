"""
TODO: tor proxy and insta data wrapper to check if connection is ok
TODO: google search 'NoneType' object has no attribute 'get_text'
"""

from data_sources.instagram import get_instagram_users
from data_sources.wikipedia import get_wiki_search
from data_sources.twitter import get_twitter_users
from data_sources.google import get_google_search_num_items

from helpers import get_entities, process_entities
from helpers import get_api_output_head_from_input_entities
import globals

from private import tor_password
from proxy.proxy_generator import ProxyChanger
proxy_changer = ProxyChanger(tor_password=tor_password)


# having hard time loading these pickled files
# https://stackoverflow.com/questions/50465106/attributeerror-when-reading-a-pickle-file
from web_score.make_score import get_score
import pickle

class MyCustomUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if module == "__main__":
            module = "web_score.make_score"
        return super().find_class(module, name)


with open('web_score/scorers/scorer_dict.pkl', 'rb') as f:
    unpickler = MyCustomUnpickler(f)
    scorer_dict = unpickler.load()


def get_social_score(input, filter_input=True):

    output = dict()

    if filter_input:
        entities = get_entities(input.title(), globals.nlp_models)
        print(entities)
        person_name = process_entities(entities)
        output.update(get_api_output_head_from_input_entities(entities))
        if not person_name:
            return {'warning': 'I am built to recognize names, but I dont see any :('}
    else:
        output.update(get_api_output_head_from_input_entities({'PERSON': [input.title()]}))
        person_name = input

    print('Google counts')
    google_counts = get_google_search_num_items(person_name, exact_match=True)
    print('Wikipedia')
    wiki_data = get_wiki_search(person_name)
    print('Instagram')
    proxy_changer.get_new_proxy(minutes_between_changes=1, connection_check=lambda: True)
    proxies = {'http': 'socks5h://localhost:9050', 'https': 'socks5h://localhost:9050'}
    instagram_data = get_instagram_users(person_name, proxies)
    print(instagram_data)
    print('Twitter')
    twitter_data = get_twitter_users(person_name)

    # making final output
    output_data = {'data': {}}
    output_data['data']['google'] = {'items': google_counts}
    output_data['data']['wikipedia'] = wiki_data
    output_data['data']['twitter'] = twitter_data
    output_data['data']['instagram'] = instagram_data

    output['scores'] = get_score(scorer_dict, output_data['data'])
    output.update(output_data)

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
        parser.add_argument('filter_input', type=int, default=1)
        args = parser.parse_args()
        try:
            output = get_social_score(args['input'], args['filter_input'])
        except:
            output = {'something went wrong': ':('}

        # this or cant communicate with javascript axios
        output = jsonify(output)
        output.headers.add('Access-Control-Allow-Origin', '*')

        return output


api.add_resource(social_score, '/api/social_score', endpoint='/social_score')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))