from flask import Flask, jsonify, Response, abort
from flask_restful import Resource, Api, reqparse, request

from werkzeug.exceptions import HTTPException

import os
import requests

app = Flask(__name__)
api = Api(app, prefix='/')


# ------------- #
# authentication


def auth(fn, *args, **kwargs):
    def inner(*args, **kwargs):

        api_keys = {'asdasd', '123'}
        api_key = request.args.get('api_key')

        if not api_key:
            return jsonify({'message': 'Missing api_key'})

        if api_key in api_keys:
            return fn(*args, **kwargs)
        else:
            return jsonify({'message': 'Authentication error, invalid api_key'})

    return inner


# ------------- #
# proxy
@auth
def proxy(request, to_url):

    # parse request
    args = request.args.to_dict()
    # headers = request.headers

    # proxy to the endpoint
    r = requests.get(to_url, params=args)
    # print(r.url, r.status_code, r.text, r.headers)

    response = Response(response=r.text,
                        status=r.status_code,
                        mimetype='application/json')

    return response


class job_title(Resource):
    def get(self):
        response = proxy(request, 'https://jobtitle-mu7u3ykctq-lz.a.run.app/api/job_title')
        return response


class web_score(Resource):
    def get(self):
        response = proxy(request, 'https://socialscore-mu7u3ykctq-lz.a.run.app/api/social_score')
        return response


api.add_resource(job_title, '/job_title')
api.add_resource(web_score, '/web_score')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
