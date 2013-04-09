import numpy as np
from make_cmap import *
from pealix import aitoff_proj, healcart_ind
import matplotlib.pyplot as plt
import matplotlib.cm as cm

def mapplot(map, rng=None, title=None, cbar=None, aitoff=None, mask=None, \
                cmap=None, psfile=None, pngfile=None, tsize=None, \
                noerase=None, units=None, usize=None, stretch=None, \
                blackbg=None, figsize=None, full=None, ticks=None):

# -------- set default min and max
    if rng==None:
        stretch  = stretch if stretch else 1.0
        index    = np.where(mask) if mask!=None else np.where(map)
        med      = np.mean(map[index])
        sig      = np.std(map[index])
        immin    = map[index].min()
        immax    = map[index].max()
        min, max = med + np.array([-2.0*sig,10.0*sig])*stretch
        min      = immin if immin > min else min
        max      = immax if immax < max else max
        rng      = [min,max]



# -------- color map and masking
    if cmap!= None:
        if cmap=='cubehelix':
            cmap = make_cmap('cubehelix')
        else:
            cmap = cm.get_cmap(cmap,256)
    else:
        cmap = cm.get_cmap('gist_heat',256)

    if mask!=None:
        map = np.ma.array(map,mask=(mask==0))
        cmap.set_bad(color = '0.25')



# -------- set background color
    pmap = map.clip(min=rng[0], max=rng[1])
    cmap.set_over(color='w')
    cmap.set_under(color='k')


# -------- check for healpix
    if map.ndim==1:
        nside = np.long(np.sqrt(map.size/12l))

        print 'MAPPLOT: Assuming HEALPix with Nside = ', nside

        if aitoff!=None: # check for aitoff
            print 'MAPPLOT:    Projecting to aitoff...'
            sidy = 850.
            sidx = 2*sidy
            pmap = aitoff_proj(pmap, nx=sidx, ny=sidy, blackbg=blackbg)

            if mask!=None:
                pmsk = aitoff_proj(mask, nx=sidx, ny=sidy, blackbg=blackbg)
                pmap = np.ma.array(pmap,mask=np.byte((pmsk < 0.9) & \
                                                         (pmsk >= 0.0)))
        else:
            print 'MAPPLOT:    Projecting to rectangle...'
            cind = healcart_ind(pmap)
            pmap = pmap[cind]



# -------- plot it
    if figsize==None:
        sz    = pmap.shape
        if sz[0] > sz[1]:
            height = 7.5
            width  = height*np.float(sz[1])/np.float(sz[0])*4./3.
        else:
            width  = 7.5
            height = width*np.float(sz[0])/np.float(sz[1])*4./3.
        figsize = [width,height]

    if not noerase:
        plt.figure(figsize=figsize)
    plt.imshow(pmap, cmap=cmap)
    plt.clim(rng)
    plt.axis('off')
    if title: plt.title(title,fontsize=tsize)

    if units: # add colorbar with units
        cb = plt.colorbar(orientation='horizontal', pad=0.05)
        cb.set_label(units, fontsize=usize)
        if ticks!=None: cb.set_ticks(ticks)
    elif cbar: # add colorbar with no units
        cb = plt.colorbar(orientation='horizontal', pad=0.05)
        if ticks!=None: cb.set_ticks(ticks)

    if full:
        plt.subplots_adjust(left=0.0, right=1.0, top=1.0, bottom=0.0)
    else:
        plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)
    plt.show()




# -------- save it
    if psfile: plt.savefig(psfile, bbox_inches='tight')
    if pngfile: plt.savefig(pngfile, bbox_inches='tight')


    return
