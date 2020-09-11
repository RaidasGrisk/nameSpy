from flask import Flask, jsonify, Response, make_response
from flask_restful import Resource, Api, request
import requests
import os
import datetime
import json

app = Flask(__name__)
api = Api(app, prefix='/v1')

# ------------- #
# database connection
from pymongo import MongoClient
from private import mongo_details  # dict with user/psw/cluster/connection url


url = mongo_details['url'].format(*[mongo_details[i] for i in ['user', 'password', 'cluster']])
db_client = MongoClient(url)


# ------------- #
# authentication
def auth(fn, *args, **kwargs):
    def inner(*args, **kwargs):

        # to clarify: the object 'request' is part of *args
        # that is being passed to wrapped function, in this case 'proxy'
        api_key = request.args.get('api_key')

        # if key is not provided limit by number of same IP requests per time period
        if not api_key:

            filter = {
                'request.ip': request.headers.get('X-Forwarded-For', request.remote_addr),
                'time': {'$gte': str(datetime.datetime.now() - datetime.timedelta(days=1))}
            }
            call_count = db_client['logs']['api_calls'].count_documents(filter)

            if call_count > 50:
                output = {'message': 'You have reached a limit of 50 calls a day. Get an api_key!'}
                return make_response(jsonify(output), 401)

        # if api_key is provided but is not in the db
        elif not db_client['data']['api_keys'].find_one({'api_key': api_key}):
            output = {'message': 'Provided api_key does not exist'}
            return make_response(jsonify(output), 401)

        # else pass through
        return fn(*args, **kwargs)

    return inner


# ------------- #
# logging
def log(fn, *args, **kwargs):
    def inner(*args, **kwargs):

        response = fn(*args, **kwargs)

        # to clarify: the object 'request' is part of *args
        # that is being passed to wrapped function, in this case 'proxy'
        log = {
            'time': str(datetime.datetime.now()),
            'request': {
                'ip': request.headers.get('X-Forwarded-For', request.remote_addr),
                'path': request.path,
                'args': request.args.to_dict()
            },
            'response': {
                'status_code': response.status_code,
                'response': json.loads(response.response[0])
            }
        }

        # push the log to db
        # should use insert_one because insert is depreciated,
        # but using insert because of the following issue:
        # https://stackoverflow.com/questions/28664383/mongodb-not-allowing-using-in-key
        # check_keys = false, to let insert dicts with keys containing '.' and '$'.
        db_client['logs']['api_calls'].insert(log, check_keys=False)
        return response
    return inner


# ------------- #
# proxy
@log
@auth
def proxy(request, to_url):

    # TODO: parse request headers and also pass method
    # parse request args
    args = request.args.to_dict()

    # proxy to the endpoint
    r = requests.get(to_url, params=args)

    response = Response(response=r.text,
                        status=r.status_code,
                        mimetype='application/json')

    return response


class job_title(Resource):
    def get(self):
        response = proxy(request, 'https://jobtitle-mu7u3ykctq-lz.a.run.app/api/job_title')
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response


class web_score(Resource):
    def get(self):
        response = proxy(request, 'https://socialscore-mu7u3ykctq-lz.a.run.app/api/social_score')
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response


api.add_resource(job_title, '/job_title')
api.add_resource(web_score, '/web_score')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
