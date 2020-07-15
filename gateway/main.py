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


url = mongo_details['url'].format(mongo_details['user'],
                                  mongo_details['password'],
                                  mongo_details['cluster'])
db_client = MongoClient(url)


# ------------- #
# authentication
def auth(fn, *args, **kwargs):
    def inner(*args, **kwargs):

        api_keys = {'123'}
        api_key = request.args.get('api_key')

        # if key is not provided limit by number of same IP requests per time period
        if not api_key:

            time_frame = str(datetime.datetime.now() - datetime.timedelta(days=1))
            filter = {
                'request.ip': request.headers.get('X-Forwarded-For', request.remote_addr),
                'time': {'$gte': time_frame}
            }
            call_count = db_client['logs']['api_calls'].count_documents(filter)

            if call_count > 50:
                return make_response(jsonify({'message': 'You have reached a limit of 50 calls a day. Get an api_key!'}), 401)

        # if api_key is provided but is not in the db
        elif api_key not in api_keys:
            return make_response(jsonify({'message': 'Provided api_key does not exist'}), 401)

        # else pass through
        return fn(*args, **kwargs)

    return inner


# ------------- #
# proxy
@auth
def proxy(request, to_url):

    # parse request
    args = request.args.to_dict()

    # proxy to the endpoint
    r = requests.get(to_url, params=args)

    response = Response(response=r.text,
                        status=r.status_code,
                        mimetype='application/json')

    return response


# ------------- #
# logging
def log(db_client, request, response):

    print(request.headers)

    # make log entry
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

    # push log to db
    db_client['logs']['api_calls'].insert_one(log)

    return True


class job_title(Resource):
    def get(self):
        response = proxy(request, 'https://jobtitle-mu7u3ykctq-lz.a.run.app/api/job_title')
        response.headers.add('Access-Control-Allow-Origin', '*')
        log(db_client, request, response)
        return response


class web_score(Resource):
    def get(self):
        response = proxy(request, 'https://socialscore-mu7u3ykctq-lz.a.run.app/api/social_score')
        response.headers.add('Access-Control-Allow-Origin', '*')
        log(db_client, request, response)
        return response


api.add_resource(job_title, '/job_title')
api.add_resource(web_score, '/web_score')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# ----------- #

# # https://projector-video-pdf-converter.datacamp.com/5865/chapter1.pdf
# filter = {'request.path': '/v1/web_score', 'time': {'$lte': str(datetime.datetime.now())}}
# db_client['logs']['api_calls'].count_documents(filter)
#
# filter = {'time': {'$lte': str(datetime.datetime.now())}}
# for doc in db_client['logs']['api_calls'].find(filter):
#     print(doc)

# # create new db / collection and document
# db = db_client['logs']
# log_collection = db['api_calls']
# log_collection.insert_one({'demo_try': 1, 'asdasd': 'asdads'})
#
# db = db_client.list_database_names()[0]
# collection = db_client[db].list_collection_names()[0]
#
# for item in db_client[db][collection].find():
#     print(item)
#     break