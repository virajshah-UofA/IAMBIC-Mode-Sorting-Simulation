import numpy as np

class MPLCModeSorter:
    def __init__(self, simX, simY, numPhaseMasks, planeDist):
        self.simX = simX
        self.simY = simY
        self.numPixels = (len(simX), len(simX[0]))

        self.numPhaseMasks = numPhaseMasks
        self.planeDist = planeDist

        self.phaseMasks = None
        self.initialPhaseMasks()

    def getXYCoords(self):
        return self.simX, self.simY

    def getNumPixels(self):
        return self.numPixels

    def getNumPhaseMasks(self):
        return self.numPhaseMasks

    def getPlaneDist(self):
        return self.planeDist

    def initializePhaseMasks(self):
        self.phaseMasks = [np.zeros(self.numPixels) for _ in range(self.numPhaseMasks)]
        return 0
