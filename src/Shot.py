



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