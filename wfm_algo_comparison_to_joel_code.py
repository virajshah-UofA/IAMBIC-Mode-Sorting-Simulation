from WFMSimulation import WFMSimulation
import ModeFieldGenerator as mfg
from Mode import Mode
import matplotlib.pyplot as plt

simParams = {'wavelength': 1550e-9,
             'numModes': 2,
             'numPixels': (128, 256),
             'pixelSize': 10e-6,
             'numPhaseMasks': 3,
             'planeDist': 25.4e-3,
             'numIterations': 50}
wfs = WFMSimulation(**simParams)

print("# Creating the Hadamard Modes #")
hModeField1, hModeField2 = mfg.createHadamardModeFields((wfs.getNumPixels()))

print("# Creating the Gaussian Modes #")
fwhm = 10*wfs.getPixelSize()
k = 50
centerPoint1 = [-k*wfs.getPixelSize(), k*wfs.getPixelSize()]
centerPoint2 = [k*wfs.getPixelSize(), -k*wfs.getPixelSize()]
simX, simY = wfs.getXYCoords()
gModeField1 = mfg.createGaussianModeField(centerPoint1, simX, simY, fwhm)
gModeField2 = mfg.createGaussianModeField(centerPoint2, simX, simY, fwhm)

print("# Placing the Generated Fields into Mode Objects #")
hMode1 = Mode(simX, simY, hModeField1)
hMode2 = Mode(simX, simY, hModeField2)
gMode1 = Mode(simX, simY, gModeField1)
gMode2 = Mode(simX, simY, gModeField2)

# Optional to normalize. Fields called are already normalized to intensity 1.
# hMode1.normalizeField()

print("# Visualizing the Field Intensities #")
if True:
    hMode1.plotFieldPhase()
    hMode2.plotFieldPhase()
    gMode1.plotModeIntensity()
    gMode2.plotModeIntensity()
    plt.show()
    plt.show(block=False)

print("# Loading Mode Objects into Simulation #")
wfs.updateInOutModes(inModes=[hMode1, hMode2],
                     outModes=[gMode1, gMode2])

print("# Running Simulation #")
wfs.runWFMAlgo()
print("The Coupling Matrix:")
print(wfs.getCouplingMatrix())