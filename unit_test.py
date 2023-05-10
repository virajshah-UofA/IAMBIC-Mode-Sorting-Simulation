import matplotlib.pyplot as plt
from WFMSimulation import WFMSimulation
from Mode import Mode

if __name__ == "__main__":
    print("------- WFMSimulation Object Tests -------")
    print('')
    simParams = {'wavelength': 1550e-9,
                 'numModes': 5,
                 'numPixels': (4, 4),
                 'pixelSize': 10e-6}
    wfs = WFMSimulation(**simParams)
    print(wfs.getSimParams())
    simX, simY = wfs.getXYCoords()
    print(simX)
    print('')
    print(simY)

    # Everything is pass by value in Python, but I'm just checking memory location
    print(wfs.inModes)

    inModes = wfs.getInOutModes()[0]
    outModes = wfs.getInOutModes()[1]
    print(inModes)

    wfs.updateInOutModes(inModes, outModes)
    print(wfs.inModes)
    print(wfs.getInOutModes()[0])

    print('')
    print("------- Mode Object Tests -------")
    print('')
    modeA = Mode(simX, simY)
    numPixels = modeA.getNumPixels()
    modeAField = modeA.getField()
    print(modeAField)
    ax1 = modeA.plotFieldPhase()
    modeA.plotFieldAmplitude()
    counter = 0
    for x in range(numPixels[0]):
        for y in range(numPixels[1]):
            modeAField[x][y] += complex(counter, (100-counter))
            counter += 1
    print(modeAField)
    ax2 = modeA.plotFieldPhase(title="Updated Field Phase", xlabel="Updated X", ylabel="Updated Y")
    modeA.plotFieldAmplitude(title="Updated Field Amplitude", xlabel="Updated X", ylabel="Updated Y")
    print(modeA)

    print(wfs.getInOutModes()[0])
    wfs.updateInOutModes([modeA] + inModes[1:], outModes)
    print(wfs.getInOutModes()[0])
    plt.show() # keep plotting windows open
