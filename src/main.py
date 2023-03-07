from flask import Flask, jsonify, request, make_response
from flask_restful import Resource, Api



import Shot
import Picture
from db import createNewShotEntry, fetchShotById, updateStabilitiesById, fetchStabilitiesById

app = Flask(__name__)

p = "Here We Go!"

ROYGBIV = [ 
    [148, 0, 211, 255], 
    [75, 0, 130, 255], 
    [0, 0, 255, 255],
    [0, 255, 0, 255], 
    [255, 255, 0, 255], 
    [255, 127, 0, 255], 
    [255, 0 , 0, 255] 
]

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
async def createNewShot():

    if request.method == 'POST':
        if (request.json['name'] != None and request.json['limits'] != None and request.json['reso'] != None and request.json['maxStability'] != None):

            newShot = Shot.Shot(request.json['name'], request.json['limits'], request.json['reso'], request.json['maxStability'])

            await createNewShotEntry(request.json['name'], request.json['limits'], request.json['reso'], request.json['maxStability'])

            return 'success', 200
        else:
            abort(400)
    else:
        abort(400)

@app.route('/calculateStabilitiesById', methods=['POST'])
async def calculateStabilitiesById():

    if request.method == 'POST':
        if (request.json['id'] != None and request.json['max_stability'] != None and request.json['z_value'] != None):

            #newShot = Shot.Shot(request.json['name'], request.json['limits'], request.json['reso'], request.json['maxStability'])

            shot_props = await fetchShotById( request.json['id'] )

            positionalVals = await Shot.createPointsList( shot_props['limits'], shot_props['reso'] )

            stabilityVals = await Shot.checkStability( positionalVals, request.json['z_value'], request.json['max_stability'] )

            await updateStabilitiesById( request.json['id'], stabilityVals )

            return 'success', 200
        else:
            abort(400)
    else:
        abort(400)

@app.route('/createPicFromStabilities', methods=['POST'])
async def createPicFromStabilities():

    if request.method == 'POST':
        if (request.json['id'] != None):

            shot_props = await fetchShotById( request.json['id'] )

            stabilityVals = await fetchStabilitiesById( request.json['id'] )
            #print(stabilityVals['stabilities'][:50])
            stylizedArray = await Picture.stylizeStabiliesForPic( stabilityVals['stabilities'], ROYGBIV, shot_props['reso'], stabilityVals['max_stability'] )
            #print(stylizedArray[:25])
            pic = await Picture.generatePicFromStylizedPoints( stylizedArray, shot_props['reso'],  )

            return 'success', 200
        else:
            abort(400)
    else:
        abort(400)

if __name__ == '__main__':
    app.run(debug=True, port=5000)