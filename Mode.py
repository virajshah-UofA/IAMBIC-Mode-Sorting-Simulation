import numpy as np
import matplotlib.pyplot as plt

class Mode:
    def __init__(self, simX, simY, eField=None):
        self.simX = simX
        self.simY = simY
        self.numPixels = (len(simX), len(simX[0]))
        if eField is None:
            self._eField = np.zeros(self.numPixels, dtype=np.cdouble)
        else:
            self._eField = eField
            assert eField.shape == simX.shape, "The field provided does not have the same size as the XY coordinates."

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
        self._eField /= np.sqrt(np.sum(np.abs(self.getField())**2))

    def plotFieldPhase(self, title=None, xlabel=None, ylabel=None):
        plt.figure()
        ax = plt.gca()
        im = plt.imshow(self.getFieldPhase(), cmap='magma')
        im.set_extent([np.amin(self.simX), np.amax(self.simX), np.amin(self.simY), np.amax(self.simY)])
        im.set_clim(-np.pi, np.pi)
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

    def plotModeIntensity(self, title=None, xlabel=None, ylabel=None):
        plt.figure()
        ax = plt.gca()
        im = plt.imshow(np.abs(self.getField())**2, cmap='magma')
        im.set_extent([np.amin(self.simX), np.amax(self.simX), np.amin(self.simY), np.amax(self.simY)])
        plt.title("Mode Intensity") if not title else plt.title(title)
        plt.xlabel("X [m]") if not xlabel else plt.xlabel(xlabel)
        plt.ylabel("Y [m]") if not ylabel else plt.ylabel(ylabel)

        plt.colorbar()
        plt.show(block=False)
        return ax
