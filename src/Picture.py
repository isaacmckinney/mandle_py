import numpy as np

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

async def generatePicFromStylizedPoints(stylizedPoints, reso):

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

    im.show(title='sample')
    
    return 1