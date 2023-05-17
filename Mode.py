import numpy as np
import matplotlib.pyplot as plt

class Mode:
    def __init__(self, simX, simY, eField=None):
        self.simX = simX
        self.simY = simY
        self.numPixels = (len(simX), len(simX[0]))
        if not eField:
            self._eField = np.zeros(self.numPixels, dtype=np.cdouble)
        else:
            self._eField = eField

    def getXYCoords(self):
        return self.simX, self.simY

    def getNumPixels(self):
        return self.numPixels

    def getField(self):
        return self._eField

    def updateField(self, eField):
        self._eField = eField
        return 0

    def getFieldPhase(self):
        return np.angle(self._eField)

    def getFieldMagnitude(self):
        return np.absolute(self._eField)

    def normalizeField(self):
        self._eField /= np.amax(self.getFieldMagnitude())

    def plotFieldPhase(self, title=None, xlabel=None, ylabel=None):
        plt.figure()
        ax = plt.gca()
        im = plt.imshow(self.getFieldPhase(), cmap='magma')
        im.set_extent([np.amin(self.simX), np.amax(self.simX), np.amin(self.simY), np.amax(self.simY)])
        plt.title("Field Phase") if not title else plt.title(title)
        plt.xlabel("X [m]") if not xlabel else plt.xlabel(xlabel)
        plt.ylabel("Y [m]") if not ylabel else plt.ylabel(ylabel)

        plt.colorbar()
        plt.show(block=False)
        return ax

    def plotFieldMagnitude(self, title=None, xlabel=None, ylabel=None):
        plt.figure()
        ax = plt.gca()
        im = plt.imshow(self.getFieldMagnitude(), cmap='magma')
        im.set_extent([np.amin(self.simX), np.amax(self.simX), np.amin(self.simY), np.amax(self.simY)])
        plt.title("Field Amplitude") if not title else plt.title(title)
        plt.xlabel("X [m]") if not xlabel else plt.xlabel(xlabel)
        plt.ylabel("Y [m]") if not ylabel else plt.ylabel(ylabel)

        plt.colorbar()
        plt.show(block=False)
        return ax
