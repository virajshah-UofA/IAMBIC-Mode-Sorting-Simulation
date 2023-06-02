import numpy as np
import matplotlib.pyplot as plt

class MPLCModeSorter:
    def __init__(self, simX, simY, numPhaseMasks, planeDist):
        self.simX = simX
        self.simY = simY
        self.numPixels = (len(simX), len(simX[0]))

        self.numPhaseMasks = numPhaseMasks
        self.planeDist = planeDist

        self.phaseMasks = None
        self.initializePhaseMasks()

    def getXYCoords(self):
        return self.simX, self.simY

    def getNumPixels(self):
        return self.numPixels

    def getNumPhaseMasks(self):
        return self.numPhaseMasks

    def getPlaneDist(self):
        return self.planeDist

    def initializePhaseMasks(self):
        self.phaseMasks = [np.ones(self.numPixels, dtype=np.cdouble) for _ in range(self.numPhaseMasks)]
        return 0

    def getPhaseMasks(self):
        return self.phaseMasks

    def updatePhaseMasks(self, phaseMasks):
        self.phaseMasks = phaseMasks
        return 0

    def plotPhaseMask(self, phaseMaskIndex, title=None, xlabel=None, ylabel=None):
        plt.figure()
        ax = plt.gca()
        im = plt.imshow(np.angle(self.phaseMasks[phaseMaskIndex]), cmap='magma')
        im.set_extent([np.amin(self.simX), np.amax(self.simX), np.amin(self.simY), np.amax(self.simY)])
        plt.title("Phase Mask {} (count from 0)".format(phaseMaskIndex)) if not title else plt.title(title)
        plt.xlabel("X [m]") if not xlabel else plt.xlabel(xlabel)
        plt.ylabel("Y [m]") if not ylabel else plt.ylabel(ylabel)

        plt.colorbar()
        plt.show(block=False)
        return ax
