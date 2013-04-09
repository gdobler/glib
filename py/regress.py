import numpy as np

def regress(templates, data, sigma=None, mask=None, error=None, \
                residual=None, chisq=None, covar=None):

    """
    NAME:
      regress

    PURPOSE:
      Solve the multilinear regression equation Pa=d, where P is the
      template matrix and d is the data vector, for the correlation
      coefficients a.

    CALLING SEQUENCE:
      aa = regress(templates, data, sigma=, mask=, error=, residual=

    INPUTS:

    OPTIONAL INPUTS:

    KEYWORDS:

    OUTPUTS:

    OPTIONAL OUTPUTS:

    EXAMPLES:

    COMMENTS:

    REVISION HISTORY:
      2013/03/13 - Written by Greg Dobler (KITP/UCSB)

    ------------------------------------------------------------
    """

# -------- set utilities and perform some input checks
    if not isinstance(templates, list):
        print "REGRESS: templates can be of any dimension but must be " + \
            "supplied as a list."
        return
    else:
        ntemp = len(templates)
        ndim  = len(templates[0].shape)
        npix  = templates[0].size

        print "REGRESS: fitting {0} templates ".format(ntemp) + \
            "in {0} dimensions".format(ndim)

    if isinstance(data, list):
        print "REGRESS: data must be supplied as an array, not a list."
        return
    else:
        dshp = data.shape

        for itemp in range(ntemp):
            if templates[itemp].shape!=dshp:
                print "REGRESS: template {0} ".format(itemp) + \
                    "is the wrong shape!!!"
                return

    if mask!=None:
        if isinstance(mask,list):
            print "REGRESS: mask must be supplied as an array, not a list."
            return
        if mask.size!=npix:
            print "REGRESS: mask is the wrong size!"
            return
        else:
            ind  = np.where(mask)[0]
            nind = ind.size
    else:
        mask = np.ones(npix,dtype=int)
        ind  = np.where(mask)[0]
        nind = ind.size

    if error==None:
        error = np.ones(dshp)
    else:
        if error.shape!=dshp:
            print "REGRESS: error is the wrong shape!!!"
            return



# -------- create template matrix and data array
    PP = np.zeros([ntemp,nind])

    for itemp in range(ntemp):
        PP[itemp,:] = templates[itemp][ind].reshape(nind) / \
            error[ind].reshape(nind)

    dd = data[ind]/error[ind]



# -------- perform the template matrix inversion
    aa = np.dot(np.dot(dd,PP.T), np.linalg.inv(np.dot(PP,PP.T)))



# -------- make the residual map and pass back through keyword
    if residual==None: residual = np.zeros(npix)

    residual[:] = data

    for itemp in range(ntemp):
        residual -= aa[itemp]*templates[itemp]



# -------- pass chisq back through keyword
    if chisq==None: chisq = np.zeros(1)

    chisq[0] = np.sum((residual[ind]/error[ind])**2)



# -------- return template amplitudes
    return aa
