"""
@brief Compute Cash statistic for Healpix maps

@author J. Chiang <jchiang@slac.stanford.edu>
"""
#
# $Header$
#

import numarray as num
from AspHealPix import *
import pyASP

def spin(ra):
    if ra > 180:
        return ra - 360
    else:
        return ra

def chidist(x, dof=1):
    return pyASP.ChiProb_gammq(dof/2., x/2.)

def deltaC(counts, model):
    if model == 0:
        return 0
    if counts == 0:
        value = 2.*(model - counts*num.log(model))
    else:
        value = 2.*(model - counts*num.log(model)-counts*(1 - num.log(counts)))
    if value < 0:
        return 0
    return value

def cstatDist(model_map, cmap, emap):
    hp = model_map.healpix()
    values = []
    for pixel in hp:
        skydir = pixel()
        model = model_map[skydir]*emap[skydir]
        counts = cmap[skydir]
        values.append(chidist(deltaC(counts, model)))
    return values

#if __name__ == '__main__':
#    model_map = CountsArray()
#    for day in range(30):
#        tmin = day*8.64e4
#        tmax = tmin + 8.64e4
