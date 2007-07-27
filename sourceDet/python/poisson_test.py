"""
@brief Use Poisson probablity to determine pixels with significant
variability from one day to the next

@author J. Chiang <jchiang@slac.stanford.edu>
"""
#
# $Header$
#

import numarray as num
from HealPix import *
import hippoplotter as plot
import celgal
from sexigesimal import sexigesimal
from BayesianBlocks import *

ndays = 53

hotpixels = {}

poissonProbs = []    
cmap_total = CountsArray('counts_000.fits')
emap_total = ExposureArray('exposure_000.fits')
for i in range(ndays):
    print i
    cmap0 = CountsArray('counts_%03i.fits' % i)
    emap0 = ExposureArray('exposure_%03i.fits' % i)
    
    cmap1 = CountsArray('counts_%03i.fits' % (i + 1))
    emap1 = ExposureArray('exposure_%03i.fits' % (i + 1))

    #
    # log of Poisson probabilities that corresponding pixels two
    # consecutive maps differ
    #
    prob = PoissonProb_compute(cmap0, emap0, cmap1, emap1)
    #
    # log of Poisson probabilities that the current map differs from
    # the mean counts map so far
    #
    prob2 = PoissonProb_compute(cmap_total/emap_total, cmap1, emap1)
    
    glon = num.array(prob.glon())
    glat = num.array(prob.glat())
    probs = num.array(prob.values())
    prob2s = num.array(prob2.values())

    #
    # ID as "hot pixels" those that have Poisson probabilities less
    # than 3.1e-3
    #
    indx = num.where(probs < -3.5)
    for j in indx[0]:
        if not hotpixels.has_key(j):
            hotpixels[j] = i + 1
            poissonProbs.append(probs[j])


#     #
#     # ID as "hot pixels" those that have Poisson probabilities less
#     # than 10**(-4.4)
#     #
#    indx2 = num.where(prob2s < -4.4)
#    for j in indx2[0]:
#        if not hotpixels.has_key(j):
#            hotpixels[j] = i + 1
#            poissonProbs.append(prob2s[j])

    print 'day %i:' % (i + 1)
    for l, b in zip(glon[indx], glat[indx]):
        print '   %6.3f  %6.3f' % (l, b)

    #
    # update cumulative maps
    #
    cmap_total += cmap1
    emap_total += emap1

#plot.histogram(poissonProbs, xname='Poisson prob.', ylog=1)
print "hot pixels: ", len(hotpixels.keys())

def build_lightcurve(bb):
    tmin, tmax, numEvents = bb.lightCurve()
    x, y = [], []
    for t0, t1, numEvt in zip(tmin, tmax, numEvents):
        x.append(t0)
        x.append(t1)
        y.append(numEvt/(t1-t0))
        y.append(numEvt/(t1-t0))
    return x, y

def lightcurves(hotpixels):
    ids = hotpixels.keys()
    lcs = {}
    for id in ids:
        lcs[id] = plot.newNTuple(([], [], [], [], []),
                                 ('day', 'flux', 'fluxerr',
                                  'counts', 'exposure'))
    for i in range(ndays):
        cmap = num.array(CountsArray('counts_%03i.fits' % i).values())
        emap = num.array(ExposureArray('exposure_%03i.fits' % i).values())
        flux = cmap/emap
        fluxerr = num.sqrt(cmap)/emap
        for id in ids:
            lcs[id].addRow((i, flux[id], fluxerr[id], cmap[id], emap[id]))
        
    for id in ids:
        ra, dec = celgal.celgal().cel((glon[id], glat[id]))
        title = "%s  %s" % sexigesimal(ra, dec)
        title += " %i" % id
        plot.XYPlot(lcs[id], 'day', 'flux', yerr='fluxerr').setTitle(title)
        plot.vline(hotpixels[id])
        tbounds = [x - 0.5 for x in lcs[id].getColumn('day')]
        tbounds.append(tbounds[-1] + 0.5)
        bb = BayesianBlocks(lcs[id].getColumn('counts'),
                            tbounds,
                            lcs[id].getColumn('exposure'), 1)
        x, y = build_lightcurve(bb)
        plot.scatter(x, y)
#        plot.scatter(x, y, oplot=1, pointRep='Line', color='red')

lightcurves(hotpixels)
