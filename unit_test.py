from WFMSimulation import WFMSimulation

if __name__ == "__main__":
    simParams = {'wavelength': 1550e-9,
                 'numModes': 5,
                 'numPixels': (4, 4),
                 'pixelSize': 5e-6}
    wfs = WFMSimulation(**simParams)
    print(type(wfs))
    print(wfs.getSimParams())
    print(wfs.simX)
    print('aaaaaaaaaaaaaaa')
    print(wfs.simY)

    updateParams = {'pixelSize': 10e-6, 'numPixels': (3,3)}
    wfs.setSimParams(**updateParams)
    print(wfs.getSimParams())
    print(wfs.simX)
    print('aaaaaaaaaaaaaaa')
    print(wfs.simY)
