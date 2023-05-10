import numpy as np

class WFMSimulation:
    def __init__(self, **kwargs):
        self.simParams = kwargs
        self.loadSimParams(**kwargs)
        self.simX = None
        self.simY = None
        self.createSimXYGrid()

        # modes creation + loadNewModes in or out (verify gridsize)
        # modesorter creation + load new modesorter device (verify gridsize), add flags into mode and modesorter that every bit of info is filled in
        # mode and modesorter class - parameters, graphing, etc.
        # later: iterations, wavefront matching algo, simulation complete flag, transfer matrix, SVD (IL and MDL) calcs, graphing

    def loadSimParams(self, **kwargs):
        self.wavelength = kwargs['wavelength']
        self.numModes = kwargs['numModes']
        self.numPixels = kwargs['numPixels']
        self.pixelSize = kwargs['pixelSize']

    def setSimParams(self, **kwargs):
        for key, value in kwargs.items():
            self.simParams[key] = value
        self.loadSimParams(**self.simParams)
        self.createSimXYGrid()
        return 1

    def getSimParams(self):
        return self.simParams

    def createSimXYGrid(self):
        nPixX = self.numPixels[0]
        nPixY = self.numPixels[1]
        X = (np.arange(1, nPixY+1) - (nPixY/2+0.5)) * self.pixelSize
        Y = (np.arange(1, nPixX+1) - (nPixX/2+0.5)) * self.pixelSize
        self.simX, self.simY = np.meshgrid(X, Y)
        return self.simX, self.simY
