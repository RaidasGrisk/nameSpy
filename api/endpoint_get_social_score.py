'''
TODO: fail when cannot connect to proxy:
"HTTPSConnectionPool(host='www.google.com', port=443):
Max retries exceeded with url: /search?as_epq=ryan+amegable (Caused by ProxyError('Cannot connect to proxy.',
OSError('Tunnel connection failed: 502 Proxy Error (destination unreachable)')))"
'''

from data_sources.instagram import get_instagram_users
from data_sources.wikipedia import get_wiki_search
from data_sources.twitter import get_twitter_users
from data_sources.google import get_google_search_result_count

from helpers import get_entities, process_entities
from helpers import get_api_output_head_from_input_entities
import globals

from private import proxy_dict

# having hard time loading these pickled files
# https://stackoverflow.com/questions/50465106/attributeerror-when-reading-a-pickle-file
from web_score.make_score import get_score
import pickle

class MyCustomUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if module == '__main__':
            module = 'web_score.make_score'
        return super().find_class(module, name)


with open('web_score/scorers/scorer_dict.pkl', 'rb') as f:
    unpickler = MyCustomUnpickler(f)
    scorer_dict = unpickler.load()


def get_social_score(input, filter_input=True, use_proxy=1, collected_data=1):

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

    # TODO: this whole block could be ran async?
    # http://www.hydrogen18.com/blog/python-await-multiple.html
    google_counts = get_google_search_result_count(person_name,
                                                   exact_match=True,
                                                   proxies=proxies,
                                                   country_code='us')
    wiki_data = get_wiki_search(person_name)
    instagram_data = get_instagram_users(person_name, proxies)
    twitter_data = get_twitter_users(person_name)

    # making final output
    output_data = {'data': {
        'google': {'items': google_counts},
        'wikipedia': wiki_data,
        'twitter': twitter_data,
        'instagram': instagram_data
    }}

    output['scores'] = get_score(scorer_dict, output_data['data'])
    output.update(output_data)

    if collected_data == 0:
        del output['data']

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
        parser.add_argument('input', type=str, required=True)
        parser.add_argument('filter_input', type=int, default=1)
        parser.add_argument('use_proxy', type=int, default=1)
        parser.add_argument('collected_data', type=int, default=1)
        args = parser.parse_args()

        try:
            output = get_social_score(**args)
        except Exception as e:
            output = {'something went wrong': ':(', 'traceback': str(e)}

        # this or cant communicate with javascript axios
        output = jsonify(output)
        output.headers.add('Access-Control-Allow-Origin', '*')

        return output


api.add_resource(social_score, '/api/social_score', endpoint='/social_score')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
