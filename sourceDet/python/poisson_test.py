"""
@brief Use Poisson probablity to determine pixels with significant
variability from one day to the next

@author J. Chiang <jchiang@slac.stanford.edu>
"""
#
# $Header$
#

import numarray as num
import hippoplotter as plot
from HealPix import *
from BayesianBlocks import *
import celgal
from sexigesimal import sexigesimal

ndays = 53

hotpixels = {}

#nt = plot.newNTuple(([],), ('Poisson prob.',))
#plot.Histogram(nt, 'Poisson prob.', ylog=1)
for i in range(ndays):
    cmap0 = CountsArray('counts_%03i.fits' % i)
    emap0 = ExposureArray('exposure_%03i.fits' % i)
    
    cmap1 = CountsArray('counts_%03i.fits' % (i + 1))
    emap1 = ExposureArray('exposure_%03i.fits' % (i + 1))
    
    prob = PoissonProb_compute(cmap0, emap0, cmap1, emap1)
    glon = num.array(prob.glon())
    glat = num.array(prob.glat())
    probs = num.array(prob.values())
#    for value in probs:
#        nt.addRow((value, ))

    #
    # Record the first day where a significant transition occurred.
    #
    indx = num.where(probs < -3.5)
    for j in indx[0]:
        if not hotpixels.has_key(j):
            hotpixels[j] = i
#    plot.scatter(glon[indx], glat[indx], xname='l', yname='b',
#                 title='%03i' % i).setTransform('HammerAito')
    print 'day %i:' % i
    for l, b in zip(glon[indx], glat[indx]):
        print '   %6.3f  %6.3f' % (l, b)

print hotpixels.keys()

def write_nt(nt, filename):
    output = open(filename, 'w')
    counts = nt.getColumn('counts')
    exposure = nt.getColumn('exposure')
    for i, x, y in zip(range(len(counts)), counts, exposure):
        output.write('%i  %e  %e\n' % (i, x, y))
    output.close()

def lightcurves(ids):
    lcs = {}
    for id in ids:
        lcs[id] = plot.newNTuple(([], [], [], [], []),
                                 ('day', 'flux', 'fluxerr', 
                                  'counts', 'exposure'))
    for i in range(ndays):
        cmap = CountsArray('counts_%03i.fits' % i)
        emap = ExposureArray('exposure_%03i.fits' % i)
        for id in ids:
            lcs[id].addRow((i, cmap.values()[id]/emap.values()[id],
                            num.sqrt(cmap.values()[id])/emap.values()[id],
                            cmap.values()[id], emap.values()[id]))
            
    for id in ids:
        ra, dec = celgal.celgal().cel((glon[id], glat[id]))
        title = "%s  %s" % sexigesimal(ra, dec)
        title += " %i" % id
        plot.XYPlot(lcs[id], 'day', 'flux', yerr='fluxerr').setTitle(title)
        plot.vline(hotpixels[id])
        
        times = num.array(lcs[id].getColumn('day')) - 0.5
        times = times.tolist()
        times.append(times[-1] + 0.5)
        counts = lcs[id].getColumn('counts')
        exposure = lcs[id].getColumn('exposure')
        bb = BayesianBlocks(counts, times, exposure, 1)
        x, y = bb.lightCurve()
        plot.scatter(x, y, pointRep='Line', oplot=1)
    return lcs

lcs = lightcurves(hotpixels.keys())
