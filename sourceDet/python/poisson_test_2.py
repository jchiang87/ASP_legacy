"""
@brief Use Poisson probablity to determine pixels with significant
variability compared to a mean intensity map

@author J. Chiang <jchiang@slac.stanford.edu>
"""
#
# $Header$
#
import numarray as num
import hippoplotter as plot
from AspHealPix import *

#nt = plot.newNTuple(([],), ('Poisson prob.',))
#plot.Histogram(nt, 'Poisson prob.', ylog=1)
cmap0 = CountsArray('counts_total.fits')
emap0 = ExposureArray('exposure_total.fits')
imap = cmap0/emap0
for i in range(10):
    cmap = CountsArray('counts_%03i.fits' % i)
    emap = ExposureArray('exposure_%03i.fits' % i)
    
    prob = PoissonProb_compute(imap, cmap, emap)
    glon = num.array(prob.glon())
    glat = num.array(prob.glat())
    probs = num.array(prob.values())
#    for value in probs:
#        nt.addRow((value, ))

    indx = num.where(probs < -3.5)
#    plot.scatter(glon[indx], glat[indx], xname='l', yname='b',
#                 title='%03i' % i).setTransform('HammerAito')
    print 'day %i:' % i
    for l, b, prb in zip(glon[indx], glat[indx], probs[indx]):
        print '   %6.3f  %6.3f  %.3e' % (l, b, prb)
