
async def createPointsList(limits, reso):
        
        newPointsList = []

        xChunkSize = ( limits[1] - limits[0] ) / reso[0]

        yChunkSize = ( limits[3] - limits[2] ) / reso[1]

        for x in range(reso[0]):
            for y in range(reso[1]):
                newPoint = [ limits[0] + ( x * xChunkSize ), limits[3] - ( y * yChunkSize ) ]
                newPointsList.append(newPoint)
        
        return newPointsList

async def checkStability(points, z, steps):
    stabilityList = []
    p_counter = 0
    for p in points:
        cnum = complex(p[0], p[1])
        cnum_tracker = complex(p[0], p[1])
        i = 0
        boundsTracker = False
        while(i < steps and not boundsTracker):
            cnum_tracker = (cnum_tracker**z) + cnum
            if cnum_tracker.real > 5 or cnum_tracker.imag > 5 or cnum_tracker.real < -5 or cnum_tracker.imag < -5:
                boundsTracker = True
            i = i + 1
        p_counter = p_counter + 1
        if p_counter % 100000 == 0:
            print("Caclulated Stability of " + str(p_counter) + " points")
        stabilityList.append(i)
    
    return stabilityList


class Shot:

    def __init__(self, name, limits, reso, maxStability):
        self.name = name
        self.limits = limits
        self.reso = reso
        self.maxStability = maxStability
    
    def getName(self):
        return self.name

    def setName(self, newName):
        self.name = newName
    
    def getId(self):
        return self.id

    def setId(self, newId):
        self.id = newId
    
    def getLimits(self):
        return self.limits

    def setLimits(self, newLimits):
        self.limits = newLimits

    def getReso(self):
        return self.reso

    def setReso(self, newReso):
        self.reso = newReso
    
    def getMaxStability(self):
        return self.maxStability

    def setMaxStability(self, newMaxStability):
        self.maxStability = newMaxStability
    
    def getStabilities(self):
        return self.stabilities

    def setStabilities(self, newStabilities):
        self.stabilities = newStabilities