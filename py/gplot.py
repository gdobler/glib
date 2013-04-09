import matplotlib.pyplot as plt

def gplot(xval, yval, sym=None, xr=None, yr=None, title=None, xlabel=None, \
              ylabel=None, tsize=None, xsize=None, ysize=None, color=None, \
              fnum=None):

# -------- defaults
    if sym==None    : sym='k-'
    if xr==None     : xr = min(xval), max(xval)
    if yr==None     : yr = min(yval), max(yval)
    if title==None  : title=''
    if xlabel==None : xlabel=''
    if ylabel==None : ylabel=''
    if fnum==None   : fnum=0


# -------- make the figure
    if plt.fignum_exists(fnum): plt.close(fnum)

    plt.figure(fnum)
    plt.plot(xval,yval,sym)
    plt.xlim(xr)
    plt.ylim(yr)
    plt.title(title, fontsize=tsize)
    plt.xlabel(xlabel, fontsize=xsize)
    plt.ylabel(ylabel, fontsize=ysize)
    plt.show()
