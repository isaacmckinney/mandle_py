from flask import Flask, jsonify, request, make_response
from flask_restful import Resource, Api

import Shot

app = Flask(__name__)

p = "Here We Go!"

@app.route('/webhook', methods=['POST'])
def webhook():

    if request.method == 'POST':
        print(request.json)
        return 'success', 200
    else:
        abort(400)

@app.route('/testHook', methods=['GET'])
def testHook():
    if request.method == 'GET':
        print(p)
        return make_response(jsonify({'data': str(p)})), 200
    else:
        abort(400)

@app.route('/testBook/<testVar>', methods=['GET'])
def testBook(testVar=None):
    if request.method == 'GET':
        print(str(testVar))
        return make_response(jsonify({'data': str(testVar)})), 200
    else:
        abort(400)

@app.route('/createNewShot', methods=['POST'])
def createNewShot():

    if request.method == 'POST':
        if (request.json['name'] != None and request.json['limits'] != None and request.json['reso'] != None and request.json['maxStability'] != None):

            newShot = Shot.Shot(request.json['name'], request.json['limits'], request.json['reso'], request.json['maxStability'])

            print(newShot.getName())
            print(newShot.getLimits())
            print(newShot.getReso())
            print(newShot.getMaxStability())

            return 'success', 200
        else:
            abort(400)
    else:
        abort(400)

if __name__ == '__main__':
    app.run(debug=True, port=5000)