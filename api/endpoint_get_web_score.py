from data_sources.instagram import get_instagram_users
from data_sources.wikipedia import get_wiki_search
from data_sources.twitter import get_twitter_users
from data_sources.google import get_google_search_result_count

from helpers import get_filtered_input
from private import proxy_dict
from log_config import handler as log_handler

import concurrent.futures
import dill

from helpers import get_nlp_models
nlp_models = get_nlp_models()

# load score models
preprocess_pipe_path = 'web_score/scorers/preprocess_pipe.pkl'
model_pipe_path = 'web_score/scorers/model_pipe.pkl'
with open(preprocess_pipe_path, 'rb') as i, open(model_pipe_path, 'rb') as j:
    preprocess_pipe = dill.load(i)
    model_pipe = dill.load(j)


def make_output(input, filter_input=True, use_proxy=1, collected_data=1, debug=0):

    # make output: name
    if filter_input:
        output_name_part = get_filtered_input(input.title(), nlp_models)
        if not output_name_part.get('input'):
            return output_name_part
    else:
        output_name_part = {'input': input}

    proxies = proxy_dict if use_proxy == 1 else {}

    # the following is for executing a number of functions in parallel
    # it would be better if this was refactored to use async
    # but the following fns (except parts of get_instagram_users) are synchronous
    # therefore one way to speed it without refactoring up is to run in parallel

    # keys are indicative, used to sort output later on
    # values are tuples where first item is the function
    # the rest of the items are function args
    # TODO: improve the readability of giving args with *args **kwargs
    person_name = output_name_part['input']
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

    # make output: data
    output_data_part = {
        'data': {
            'google': {'items': fn_outputs['google']},
            'wikipedia': fn_outputs['wikipedia'],
            'twitter': fn_outputs['twitter'],
            'instagram': fn_outputs['instagram']
        }
    }

    # make output: scores
    preprocessed_data = preprocess_pipe.transform([output_data_part['data']])
    separate_scores = model_pipe.named_steps['ECDF'].transform(preprocessed_data).T[0].to_dict()
    web_score = model_pipe.transform(preprocess_pipe.transform([output_data_part['data']]))[0]

    keys_mapping = {
        'google_items': 'google',
        'wikipedia_items': 'wikipedia',
        'twitter_followers_mean': 'twitter',
        'instagram_followers_mean': 'instagram'
    }
    separate_scores = {keys_mapping[k]: v for k, v in separate_scores.items()}
    final_score = {'web_score': web_score}
    output_score_part = {'scores': {**final_score, **separate_scores}}

    # make output: log
    output_log_part = {'log': [str(i) for i in log_handler.log]}

    # combine parts into final output
    output = {
        **output_name_part,
        **output_score_part,
        **[output_data_part if collected_data == 1 else {}][0],
        **[output_log_part if debug == 1 else {}][0],
    }

    return output


# -------------- #
from flask import Flask
from flask import jsonify, Response
from flask_restful import Resource, Api, reqparse
import os
import traceback

app = Flask(__name__)
api = Api(app)
app.config['JSON_SORT_KEYS'] = False  # do not sort data


class web_score(Resource):
    def get(self):

        parser = reqparse.RequestParser()
        parser.add_argument('input', type=str, required=True)
        parser.add_argument('filter_input', type=int, default=1)
        parser.add_argument('use_proxy', type=int, default=1)
        parser.add_argument('collected_data', type=int, default=1)
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


api.add_resource(web_score, '/api/web_score', endpoint='/web_score')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
