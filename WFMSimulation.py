import numpy as np
from Mode import Mode

class WFMSimulation:
    def __init__(self, **kwargs):
        self.simParams = kwargs
        self.loadSimParams(**kwargs)
        self.createSimXYGrid()
        self.initializeInOutModes()
        self.createMPLCModeSorter()

    def loadSimParams(self, **kwargs):
        self.wavelength = kwargs['wavelength']
        self.numModes = kwargs['numModes']
        self.numPixels = kwargs['numPixels']
        self.pixelSize = kwargs['pixelSize']

        self.simX = None
        self.simY = None
        self.inModes = None
        self.outModes = None

    def createSimXYGrid(self):
        nPixX = self.numPixels[0]
        nPixY = self.numPixels[1]
        X = (np.arange(1, nPixY + 1) - (nPixY / 2 + 0.5)) * self.pixelSize
        Y = (np.arange(1, nPixX + 1) - (nPixX / 2 + 0.5)) * self.pixelSize
        self.simX, self.simY = np.meshgrid(X, Y)
        return self.simX, self.simY

    def initializeInOutModes(self):
        self.inModes = [Mode(self.simX, self.simY) for _ in range(self.numModes)]
        self.outModes = [Mode(self.simX, self.simY) for _ in range(self.numModes)]

    def createMPLCModeSorter(self):
        pass

   # ------- Define getter and setter functions -------

    def getSimParams(self):
        return self.simParams

    def getXYCoords(self):
        return self.simX, self.simY

    def getInOutModes(self):
        return self.inModes, self.outModes

    def updateInOutModes(self, inModes, outModes):
        self.inModes = inModes
        self.outModes = outModes
        return 0
