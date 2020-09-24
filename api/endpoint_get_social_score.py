from data_sources.instagram import get_instagram_users
from data_sources.wikipedia import get_wiki_search
from data_sources.twitter import get_twitter_users
from data_sources.google import get_google_search_result_count

import concurrent.futures

from helpers import get_entities, process_entities
from helpers import get_api_output_head_from_input_entities
import globals

from private import proxy_dict
from log_cofig import handler as log_handler

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


def get_social_score(input, filter_input=True, use_proxy=1, collected_data=1, debug=0):

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

    # the following is for executing a number of functions in parallel
    # it would be better if this was refactored to use async
    # but the following fns (except parts of get_instagram_users) are synchronous
    # therefore one way to speed it without refactoring up is to run in parallel

    # keys are indicative, used to sort output later on
    # values are tuples where first item is the function
    # the rest of the items are function args
    # TODO: improve the readability of giving args with *args **kwargs
    fn_list = {
        'google': (get_google_search_result_count, person_name, True, proxies, 'us'),
        'wikipedia': (get_wiki_search, person_name),
        'instagram': (get_instagram_users, person_name, proxies),
        'twitter': (get_twitter_users, person_name)
    }

    # lets create the executor and execute
    # the above defined fns in parallel
    fn_outputs = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        # dict with keys as executors and values as strings of data sources
        # this is needed to map outputs to its sources. Keys are executors because
        # it only works this way inside concurrent.futures.as_completed
        futures = {executor.submit(*fn_list[key]): key for key in fn_list}
        for future in concurrent.futures.as_completed(futures):
            fn_outputs[futures[future]] = future.result()

    # making final output
    output_data = {
        'data': {
            'google': {'items': fn_outputs['google']},
            'wikipedia': fn_outputs['wikipedia'],
            'twitter': fn_outputs['twitter'],
            'instagram': fn_outputs['instagram']
        }
    }

    output['scores'] = get_score(scorer_dict, output_data['data'])
    output.update(output_data)

    if collected_data == 0:
        del output['data']

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


class social_score(Resource):
    def get(self):

        parser = reqparse.RequestParser()
        parser.add_argument('input', type=str, required=True)
        parser.add_argument('filter_input', type=int, default=1)
        parser.add_argument('use_proxy', type=int, default=1)
        parser.add_argument('collected_data', type=int, default=1)
        parser.add_argument('debug', type=int, default=0)
        args = parser.parse_args()

        try:
            output = get_social_score(**args)
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


api.add_resource(social_score, '/api/social_score', endpoint='/social_score')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
