import numpy as np
import matplotlib.colors as colors
import matplotlib.pyplot as plt

def cubehelix(lam, start=None, nrot=None, hue=None, gamma=None):

    start = start if start else 0.5
    nrot  = nrot if nrot else -1.5
    hue   = hue if hue else 1.0
    gamma = gamma if gamma else 1.0

    phi = 2.0 * np.pi * (start / 3.0 + nrot*lam)
    a   = hue * lam**gamma * (1.0 - lam**gamma)/2.0

    r = lam**gamma + a * (-0.14861 * np.cos(phi) + 1.78277 * np.sin(phi))
    g = lam**gamma + a * (-0.29227 * np.cos(phi) - 0.90649 * np.sin(phi))
    b = lam**gamma + a * ( 1.97294 * np.cos(phi))

    return r,g,b


def make_cmap(type, see=None):

# -------- utilities
    lam = np.arange(256) / 255.0



# -------- generate
    if type=='cubehelix':
        r,g,b = cubehelix(lam)
    else:
        print 'MAKE_CMAP: only cubehelix map is supported'
        return

    rvec = [(0.0,r[0],r[0])]
    bvec = [(0.0,g[0],g[0])]
    gvec = [(0.0,b[0],b[0])]

    for i in range(1,256):
        rvec.append((lam[i],r[i],r[i])) 
        gvec.append((lam[i],g[i],g[i])) 
        bvec.append((lam[i],b[i],b[i])) 

    cdict   = {'red': rvec, 'green': gvec, 'blue':bvec}
    my_cmap = colors.LinearSegmentedColormap('my_colormap',cdict,256)

    if see!=None:
        img = np.arange(400).reshape(20,20) / 400.

        plt.figure()
        plt.imshow(img,cmap=my_cmap)
        plt.colorbar()
        plt.show()

    return my_cmap
