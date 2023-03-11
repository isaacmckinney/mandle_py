import numpy as np
from os import getcwd, mkdir, path

from PIL import Image

async def stylizeStabiliesForPic(stabilities, style, reso, max_stability):

    size = reso[0] * reso[1]
    stylizedPoints = [None]*size
    #print(stabilities[0])
    for p in range(len(stabilities)):
        if stabilities[ p ] < max_stability - 1:
            stylizedPoints[ p ] = style [ stabilities[ p ] % len( style ) ]
        else:
            stylizedPoints[ p ] = [ 0, 0, 0, 255 ]
        
    
    return stylizedPoints

async def generatePicFromStylizedPoints(stylizedPoints, reso, id):

    formattedStylizedArray = np.zeros((reso[1], reso[0], 4), dtype=np.uint8)

    p_counter = 0

    for row in range(reso[0]):

        for col in range(reso[1]):

            formattedStylizedArray[col, row, 0] = (np.uint8) (stylizedPoints[ p_counter ][0])
            formattedStylizedArray[col, row, 1] = (np.uint8) (stylizedPoints[ p_counter ][1])
            formattedStylizedArray[col, row, 2] = (np.uint8) (stylizedPoints[ p_counter ][2])
            formattedStylizedArray[col, row, 3] = (np.uint8) (stylizedPoints[ p_counter ][3])

            p_counter = p_counter + 1
    
    im = Image.fromarray(formattedStylizedArray, mode="RGBA")
    if (path.exists(getcwd() +"\\src\\generated\\")):
        pass
    else:
        mkdir(getcwd() +"\\src\\generated\\")
    newFilename = getcwd() +"\\src\\generated\\" + str(id) + ".png"
    print("FILE PATH: ", newFilename)
    im.save(newFilename)
    #im = Image.open(newFilename)
    #im.show()

    
    return 1

async def getPictureFilePath(id):
    filename = getcwd() +"\\src\\generated\\" + str(id) + ".png"
    
    return { "filepath": filename }
