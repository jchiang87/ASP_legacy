"""
@brief Compute the distributions of Poisson probabilities for
an input intensity map and exposure map, which are combined to 
from the model prediction, and the observed counts map.  These
distributions can be used to identify pixels with significant
variability and also for forming the null distribution.

@author J. Chiang <jchiang@slac.stanford.edu>
"""
#
# $Header$
#

import numarray as num
from HealPix import *
import pyASP

_log10 = num.log(10)

def chidist(x, dof=1):
    return pyASP.ChiProb_gammq(dof/2., x/2.)

def logPoissonProb(counts, model):
    if model == 0 and counts == 0:
        return 0
    else:
        return counts*num.log(model) - model - pyASP.ChiProb_gammln(counts+1)

def log10PoissonProb(counts, model):
    return logPoissonProb(counts, model)/_log10

def cstat(counts, model):
    """Cash statistic"""
    try:
        value = 0
        for nn, theta in zip(counts, model):
            value += -2.*logPoissonProb(nn, theta)
        return value
    except TypeError:
        return -2.*logPoissonProb(counts, model)

def probDist(imap, cmap, emap):
    hp = imap.healpix()
    values = []
    model_map = imap*emap
    for pixel in hp:
        skydir = pixel()
        model = model_map[skydir]
        counts = cmap[skydir]
        if model != 0:
            log10prob = log10PoissonProb(counts, model)
            values.append(log10prob)
    return values

def probDist2(cmap0, emap0, cmap1, emap1):
    hp = cmap0.healpix()
    values = []
    imap = (cmap0 + cmap1)/(emap0 + emap1)
    model_map0 = imap*emap0
    model_map1 = imap*emap1
    for pixel in hp:
        skydir = pixel()
        model0 = model_map0[skydir]
        model1 = model_map1[skydir]
        counts0 = cmap0[skydir]
        counts1 = cmap1[skydir]
        if model0 != 0 and model1 != 0:
            log10prob0 = log10PoissonProb(counts0, model0)
            log10prob1 = log10PoissonProb(counts1, model1)
        values.append(min(log10prob0, log10prob1))
    return values

if __name__ == '__main__':
    model = 10
    total = 0
    for counts in range(30):
        total += num.exp(logPoissonProb(counts, model))
    print total
