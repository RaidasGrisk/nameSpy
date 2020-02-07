from flask import Flask
from flask import jsonify
from flask_restful import Resource, Api, reqparse

from main import get_api_data

app = Flask(__name__)
api = Api(app)
app.config['JSON_SORT_KEYS'] = False  # do not sort data


class BarAPI(Resource):
    def get(self):

        parser = reqparse.RequestParser()
        parser.add_argument('input', type=str)
        args = parser.parse_args()
        try:
            output = get_api_data(args['input'])
        except:
            output = {'something went wrong': ':('}

        # this or cant communicate with javascript axios
        output = jsonify(output)
        output.headers.add('Access-Control-Allow-Origin', '*')

        return output


api.add_resource(BarAPI, '/api', endpoint='api')

if __name__ == '__main__':
    app.run(debug=True)