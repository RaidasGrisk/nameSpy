from flask import Flask
from flask import jsonify
from flask_restful import Resource, Api, reqparse

from main import get_social_score, get_job_title

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
        except:
            output = {'something went wrong': ':('}

        # this or cant communicate with javascript axios
        output = jsonify(output)
        output.headers.add('Access-Control-Allow-Origin', '*')

        return output


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


# http://127.0.0.1:5000/api/social_score?input=Raidas%20Griskevicius
# http://127.0.0.1:5000/api/job_title?input=Raidas%20Griskevicius

api.add_resource(job_title, '/api/job_title', endpoint='/job_title')
api.add_resource(social_score, '/api/social_score', endpoint='/social_score')

if __name__ == '__main__':
    app.run(debug=True)
