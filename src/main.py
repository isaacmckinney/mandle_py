from flask import Flask, jsonify, request, make_response
from flask_restful import Resource, Api

app = Flask(__name__)

api = Api(app)

class templateRestFunction(Resource):

    def get(self):
        return make_response(jsonify({'message': 'example-response'}))
    
    def post(self):
        recieved_data = request.get_json()
        print("________________________________________________________________________________________________")
        print(recieved_data)
        print("________________________________________________________________________________________________")
        return make_response(jsonify({'data': recieved_data}), 201)

api.add_resource(templateRestFunction, '/')

if __name__ == '__main__':
    app.run(debug=True, port=5000)