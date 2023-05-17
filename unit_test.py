import matplotlib.pyplot as plt
from WFMSimulation import WFMSimulation

def objectChecks():
    print("------- WFMSimulation Object Tests -------")
    print('')
    simParams = {'wavelength': 1550e-9,
                 'numModes': 5,
                 'numPixels': (4, 4),
                 'pixelSize': 10e-6,
                 'numPhaseMasks': 3,
                 'planeDist': 25.4e-3}
    wfs = WFMSimulation(**simParams)
    print(wfs.getSimParams())
    simX, simY = wfs.getXYCoords()
    print(simX)
    print('')
    print(simY)

    # I'm just checking memory location, but the names are bound to an array. "Pass by object reference."
    # https://robertheaton.com/2014/02/09/pythons-pass-by-object-reference-as-explained-by-philip-k-dick/
    # https://stackoverflow.com/questions/13530998/are-python-variables-pointers-or-else-what-are-they
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
    # modeA = Mode(simX, simY)
    modeA = wfs.getInOutModes()[0][0]
    numPixels = modeA.getNumPixels()
    modeAField = modeA.getField()
    print(modeAField)
    ax1 = modeA.plotFieldPhase()
    modeA.plotFieldMagnitude()
    counter = 0
    for x in range(numPixels[0]):
        for y in range(numPixels[1]):
            modeAField[x][y] += complex(counter, (100-counter))
            counter += 1
    print(modeAField)
    modeA.updateField(modeAField) # unncessary here because array edited in place, but recommended to do to ensure array change has propagated
    ax2 = modeA.plotFieldPhase(title="Updated Field Phase", xlabel="Updated X", ylabel="Updated Y")
    modeA.plotFieldMagnitude(title="Updated Field Amplitude", xlabel="Updated X", ylabel="Updated Y")
    print(modeA)
    print(modeA.getFieldMagnitude())
    print(modeA.getFieldPhase())

    print(wfs.getInOutModes()[0])
    wfs.updateInOutModes([modeA] + inModes[1:], outModes) # again, unncessary here because array edited in place, but recommended to do to ensure array change has propagated
    print(wfs.getInOutModes()[0])

    modeA.normalizeField()
    modeA.plotFieldPhase(title="(Normalized) Field Phase", xlabel="Updated X", ylabel="Updated Y")
    modeA.plotFieldMagnitude(title="Normalized Field Amplitude", xlabel="Updated X", ylabel="Updated Y")
    print(modeA.getField())
    print(modeA.getFieldMagnitude())
    print(modeA.getFieldPhase())

    print('')
    print("------- MPLCModeSorter Object Tests -------")
    print('')
    modeSorter = wfs.getMPLCModeSorter()
    numPixels = modeSorter.getNumPixels()
    phaseMasks = modeSorter.getPhaseMasks()
    print(id(phaseMasks[0]))
    phaseMask1 = phaseMasks[0]
    print(id(phaseMask1))
    print(phaseMask1)
    modeSorter.plotPhaseMask(0, title="Phase Mask 0", xlabel="X", ylabel="Y")
    print(modeSorter.getPhaseMasks()[0])

    for x in range(numPixels[0]):
        for y in range(numPixels[1]):
            phaseMask1[x][y] += 3.14/counter
            counter += 1
    modeSorter.updatePhaseMasks([phaseMask1] + phaseMasks[1:]) # unncessary here because array edited in place, but recommended to do to ensure array change has propagated
    wfs.updateMPLCModeSorter(modeSorter) # unncessary here because array edited in place, but recommended to do to ensure array change has propagated
    print(modeSorter.getPhaseMasks()[0])
    print(modeSorter.getPhaseMasks()[1])

    modeSorter.plotPhaseMask(0, title="Phase Mask 0", xlabel="X", ylabel="Y")
    modeSorter.plotPhaseMask(1, title="Phase Mask 1", xlabel="X", ylabel="Y")

    plt.show() # keep plotting windows open

if __name__ == "__main__":
    objectChecks()