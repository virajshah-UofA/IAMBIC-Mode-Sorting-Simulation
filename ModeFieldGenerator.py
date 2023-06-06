import numpy as np

def generateGaussianModeFieldSpot(centerPoint, simX, simY, fwhm):
    centerX, centerY = centerPoint
    sigma = fwhm/(2*np.sqrt(2*np.log(2)))
    gaussFunc = lambda x, y : (1/(2 * np.pi * sigma**2)) * np.exp(-1 * ((x - centerX)**2 + (y - centerY)**2) / (2 * sigma**2))

    # Not editing in place. Must return a new array and update upstream accordingly.
    field = gaussFunc(simX, simY).astype(dtype=np.cdouble)
    field /= np.sqrt(np.sum(np.abs(field)**2)) # normalize intensity to 1
    return field

def createHadamardModes(numPixels):
    hMode1 = np.ones(numPixels, dtype=np.cdouble)
    hMode2 = np.ones(numPixels, dtype=np.cdouble)
    Nx = numPixels[0]
    Ny = numPixels[1]
    hMode1[:,:int(Ny/2)] = -1
    hMode2[:int(Nx/2),:] = -1

    # Normalize intensity to 1
    hMode1 /= np.sqrt(np.sum(np.abs(hMode1)**2))
    hMode2 /= np.sqrt(np.sum(np.abs(hMode2)**2))
    return hMode1, hMode2