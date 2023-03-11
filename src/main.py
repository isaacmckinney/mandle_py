from flask import Flask, jsonify, request, make_response, Response, send_file
from flask_restful import Resource, Api
from flask_cors import CORS


import Shot
import Picture
from db import createNewShotEntry, fetchShotById, updateStabilitiesById, fetchStabilitiesById, fetchShotForCopy, fetchAllShotsInfo

app = Flask(__name__)
cors = CORS(app)

# Rainbow sequence
ROYGBIV = [ 
    [148, 0, 211, 255], 
    [75, 0, 130, 255], 
    [0, 0, 255, 255],
    [0, 255, 0, 255], 
    [255, 255, 0, 255], 
    [255, 127, 0, 255], 
    [255, 0 , 0, 255] 
]

#######################################################################
#################### Example Template Webhooks ########################
#######################################################################

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

#######################################################################
############################## END ####################################
#######################################################################

# Create a new Shot entry in the db, ready to calculate stabilities
# Expected attributes in JSON request
# name: string, limits: [float, float, float, float], reso: [int, int], maxStability: int
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

# Calculate stabilities for existing shot entry
# Expected attributes in JSON request
# id: string, max_stability: int, z_value: float
@app.route('/calculateStabilitiesById', methods=['POST'])
async def calculateStabilitiesById():

    if request.method == 'POST':
        if (request.json['id'] != None and request.json['max_stability'] != None and request.json['z_value'] != None):

            shot_props = await fetchShotById( request.json['id'] )

            positionalVals = await Shot.createPointsList( shot_props['limits'], shot_props['reso'] )

            stabilityVals = await Shot.checkStability( positionalVals, request.json['z_value'], request.json['max_stability'] )

            await updateStabilitiesById( request.json['id'], stabilityVals )

            return make_response(jsonify({"Status": "success"})), 200
        
        else:
            abort(400)
    else:
        abort(400)

# Generate image from calculated stabilities of existing shot in db
# Expected attributes in JSON request
# id: string
@app.route('/createPicFromStabilities', methods=['POST'])
async def createPicFromStabilities():

    if request.method == 'POST':
        if (request.json['id'] != None):

            shot_props = await fetchShotById( request.json['id'] )

            stabilityVals = await fetchStabilitiesById( request.json['id'] )

            stylizedArray = await Picture.stylizeStabiliesForPic( stabilityVals['stabilities'], ROYGBIV, shot_props['reso'], stabilityVals['max_stability'] )

            pic = await Picture.generatePicFromStylizedPoints( stylizedArray, shot_props['reso'], request.json['id'] )

            return make_response(jsonify({"Status": "success"})), 200
        
        else:
            abort(400)
    else:
        abort(400)

# Create new shot from zooming in on existing shot
# Expected attributes in JSON request
# id: string, zoomDiv: int, selection: int
# zoomDiv: defines the number of divisions on a shot to zoom to
# selection: indicates which 'zoomDiv' was selected to zoom to
@app.route('/createShotFromZoom', methods=['POST'])
async def createShotFromZoom():

    if request.method == 'POST':
        if (request.json['id'] != None and request.json['zoomDiv'] != None and request.json['selection'] != None):

            shot_props = await fetchShotForCopy( request.json['id'] )

            newLimits = await Shot.zoomBounds( shot_props['limits'], request.json['zoomDiv'], request.json['selection'] )

            newId = await createNewShotEntry( shot_props['name'], newLimits['limits'], shot_props['reso'], shot_props['max_stability'] )
            
            return make_response(jsonify({"Status": "success", "id": newId})), 200
        
        else:
            abort(400)
    else:
        abort(400)

# fetch local .png rendering of shot and respond with the file
# Expected parameter in webhook URL
# id: string
@app.route('/fetchPicture/<id>', methods=['GET'])
async def fetchPicture(id=None):
    if request.method == 'GET':
        
        img = await Picture.getPictureFilePath( id )
            
        return send_file( img['filepath'] )

    else:
        abort(400)

# fetch local .png rendering of shot and respond with the file
@app.route('/fetchShotIds', methods=['GET'])
async def fetchShotIds():
    if request.method == 'GET':

        shots_data = await fetchAllShotsInfo()
            
        return make_response(jsonify({'data': shots_data['results']})), 200

    else:
        abort(400)

if __name__ == '__main__':
    app.run(debug=True, port=5000)