"""
@brief Compute flux estimates for each pixel and update entry in 
trending database.

@author J. Chiang <jchiang@slac.stanford.edu>
"""
#
# $Header$
# 

import os
import glob
import numarray as num
from AspHealPix import *
from DbEntry import DbEntry
from FitsNTuple import FitsNTuple

os.chdir(os.environ['OUTPUTDIR'])

#tstart = float(os.environ['TSTART'])
#tstop = float(os.environ['TSTOP'])

scData = FitsNTuple('FT2_merged.fits')
tstart, tstop = min(scData.START), max(scData.STOP)

cmap = CountsArray(glob.glob('cmap*.fits')[0])
emap = ExposureArray(glob.glob('emap*.fits')[0])

def pixel_id(l, b):
    return "l b = %8.3f %8.3f" % (l, b)

output = open('pixel_fluxes.dat', 'w')
for l, b, cnts, expsr in zip(cmap.glon(), cmap.glat(), 
                             cmap.values(), emap.values()):
    if expsr > 100:
        value = cnts/expsr
        error = num.sqrt(cnts)/expsr
        output.write("%s  %10.3f  %10.3f  %.5e  %.5e\n" % (pixel_id(l, b), l, b, value, error))
#        output.write("%10.3f  %10.3f  %.5e  %.5e\n" % (l, b, value, error))
        dbEntry = DbEntry(pixel_id(l, b), 'flux_100_300000', tstart, tstop, 
                          cadence='downlink')
        dbEntry.setValues(value, error)
        dbEntry.write()
output.close()
