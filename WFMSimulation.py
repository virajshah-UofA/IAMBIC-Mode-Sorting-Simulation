import numpy as np
from Mode import Mode
from MPLCModeSorter import MPLCModeSorter
from FreeSpaceProp import createFreeSpacePropTransferFunc

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
        self.numIterations = kwargs['numIterations']

        self.simX = None
        self.simY = None
        self.inModes = None
        self.outModes = None
        self.modeSorter = None

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
        self.modeSorter = MPLCModeSorter(self.simX, self.simY, self.simParams['numPhaseMasks'], self.simParams['planeDist'])

   # ------- Define getter and setter functions -------

    def getSimParams(self):
        return self.simParams

    def getNumPixels(self):
        return self.numPixels

    def getPixelSize(self):
        return self.pixelSize

    def getXYCoords(self):
        return self.simX, self.simY

    def getInOutModes(self):
        return self.inModes, self.outModes

    def updateInOutModes(self, inModes=None, outModes=None):
        if inModes:
            self.inModes = inModes
        if outModes:
            self.outModes = outModes
        return 0

    def getMPLCModeSorter(self):
        return self.modeSorter

    def updateMPLCModeSorter(self, modeSorter):
        self.modeSorter = modeSorter
        return 0

    def getCouplingMatrix(self):
        return self.couplingMatrix

    # ------- Running the wavefront matching algorithm -------

    def runWFMAlgo(self):
        print("------- Running the wavefront matching algorithm -------")
        self.wfmFields = np.zeros((2, self.modeSorter.numPhaseMasks, self.numModes, self.numPixels[0], self.numPixels[1]), dtype=np.cdouble)
        self.fwbwCoupling = np.zeros((self.numIterations, self.numModes))

        self._loadInOutModes()

        self.freeSpaceProp = createFreeSpacePropTransferFunc(self.simX, self.simY, self.wavelength)

        # Initialize the fields at each plane by propagating forward and backwards once
        self._forwardPassThruDevice(updateMask=False)
        self._backwardPassThruDevice(updateMask=False)

        print("------- Starting forward and backward passes -------")
        # Start iterating forward and backward passes while updating the masks on each iteration
        for iterIdx in range(self.numIterations):
            self._forwardPassThruDevice(updateMask=True)
            self._backwardPassThruDevice(updateMask=True)

        # One final pass forward of all the fields through the final phase masks
        self._forwardPassThruDevice(updateMask=False)
        print("Iteration complete.")
        print("------- Starting Analysis -------")

        # Run the final analyses (e.g., coupling matrix, losses)
        self._calculateCouplingMatrix()
        self._calculateLoss()
        print("The insertion loss of the mode sorter: {0:.4f} dB".format(self.insertionLoss))
        print("The mode dependent loss of the mode sorter: {0:.4f} dB".format(self.modeDependentLoss))
        return 0

    def _loadInOutModes(self):
        # Load in the input modes at the first plane, in the forward direction
        # Load in the output modes at the last plane, in the reverse direction
        for modeIdx in range(self.numModes):
            self.wfmFields[0,0,modeIdx,:,:] = self.inModes[modeIdx].getField()
            self.wfmFields[1,-1,modeIdx,:,:] = self.outModes[modeIdx].getField()
        return 0

    def _forwardPassThruDevice(self, updateMask=False):
        # Send the fields through the modesorter in the forward propagation direction
        # Only update the masks when flag is true (i.e., when iterating to find new masks)
        directionIdx = 0 # 0 for forwards, 1 for backwards
        for planeIdx in range(self.modeSorter.numPhaseMasks-1):
            if updateMask:
                self._updateMasks(planeIdx)

            _currentMask = np.exp(complex(0, -1)*np.angle(self.modeSorter.getPhaseMask(planeIdx)))

            for modeIdx in range(self.numModes):
                # Get the field and apply the mask
                field = self.wfmFields[directionIdx,planeIdx,modeIdx,:,:]*_currentMask
                # Propagate the field to the next plane
                field = self.freeSpaceProp(field, self.modeSorter.getPlaneDist(), direction=directionIdx)
                # Store the field result at the next plane
                self.wfmFields[directionIdx,planeIdx+1,modeIdx,:,:] = field
        return 0

    def _backwardPassThruDevice(self, updateMask=False):
        # Send the fields through the modesorter in the backward propagation direction
        # Only update the masks when flag is true (i.e., when iterating to find new masks)
        directionIdx = 1 # 0 for forwards, 1 for backwards
        for planeIdx in range(self.modeSorter.numPhaseMasks-1,0,-1):
            if updateMask:
                self._updateMasks(planeIdx)

            _currentMask = np.exp(complex(0, 1)*np.angle(self.modeSorter.getPhaseMask(planeIdx)))

            for modeIdx in range(self.numModes):
                # Get the field and apply the mask
                field = self.wfmFields[directionIdx,planeIdx,modeIdx,:,:] * _currentMask
                # Propagate the field to the previous plane
                field = self.freeSpaceProp(field, self.modeSorter.getPlaneDist(), direction=directionIdx)
                # Store the field result at the previous plane
                self.wfmFields[directionIdx,planeIdx-1,modeIdx,:,:] = field
        return 0

    def _updateMasks(self, planeIdx):
        _currentMask = np.exp(complex(0, 1)*np.angle(self.modeSorter.getPhaseMask(planeIdx)))
        _updatedMask = 0

        for modeIdx in range(self.numModes):
            fieldFW = self.wfmFields[0,planeIdx,modeIdx,:,:]
            fieldBW = np.conj(self.wfmFields[1,planeIdx,modeIdx,:,:])

            pwrFW = np.sum(np.abs(fieldFW)**2)
            pwrBW = np.sum(np.abs(fieldBW)**2)

            dMask = (fieldFW*fieldBW)/np.sqrt(pwrFW*pwrBW) # element-wise multiplication
            dPhi = np.sum(dMask*np.conj(_currentMask))

            _updatedMask += dMask*np.exp(complex(0,-1)*np.angle(dPhi))

        # Update the mask
        self.modeSorter.updatePhaseMask(planeIdx, _updatedMask)
        return 0

    def _calculateCouplingMatrix(self):
        self.couplingMatrix = np.zeros((self.numModes, self.numModes), dtype=np.cdouble)
        lastMask = np.exp(complex(0, -1) * np.angle(self.modeSorter.getPhaseMask(self.modeSorter.numPhaseMasks-1)))

        for modeIdx in range(self.numModes):
            fieldIn = self.wfmFields[0, -1, modeIdx, :, :]*lastMask
            for modeIdy in range(self.numModes):
                fieldOut = self.wfmFields[1, -1, modeIdy, :, :]
                self.couplingMatrix[modeIdx, modeIdy] = np.sum(np.conj(fieldIn)*fieldOut)
        return 0

    def _calculateLoss(self):
        [U, S, V] = np.linalg.svd(self.couplingMatrix)
        s = S**2
        self.insertionLoss = 10*np.log10(np.mean(s))
        self.modeDependentLoss = 10*np.log10(s[-1]/s[0])
        return 0