import numpy as np

'''
Adapted from Joel Carpenter's Code
'''
def createFreeSpacePropTransferFunc(simX, simY, wavelength):
    numPixels = (len(simX), len(simX[0]))
    Nx = numPixels[1]
    Ny = numPixels[0]

    # K-space coordinates
    fs = Nx/(np.max(simX) - np.min(simX))
    v_x = fs*(np.arange(-Nx/2,Nx/2)/Nx)
    fs = Ny/(np.max(simY) - np.min(simY))
    v_y = fs*(np.arange(-Ny/2,Ny/2)/Ny)
    V_x, V_y = np.meshgrid(v_x, v_y)

    tfCoef1 = -1*complex(0,1)*2*np.pi*np.sqrt(wavelength**-2 - V_x**2 - V_y**2)

    def freeSpaceProp(field, dz, direction=1):
        H0 = np.exp(tfCoef1 * dz)

        if direction==1:
            H = H0
        elif direction==-1:
            H = np.conj(H0)
        F = np.fft.fftshift(np.fft.fft2(np.fft.fftshift(field)))
        F = F * H  # element-wise multiplication
        propagatedField = np.fft.fftshift(np.fft.ifft2(np.fft.fftshift(F)))
        return propagatedField

    return freeSpaceProp

