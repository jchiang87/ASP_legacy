import sys, os
sys.path.append('../python')
sys.path.append(os.path.join(os.environ['LIKEGUIROOT'], 'python'))
sys.path.append(os.path.join(os.environ['SANEROOT'], 'python'))
import numarray as num
import numarray.ma as ma
import celgal
import copy
from FitsNTuple import FitsNTuple
from xml.dom import minidom

from BayesBlocks import BayesBlocks, LightCurve
from BayesianBlocks import Exposure, DoubleVector

import string

def roiCenter(xmlFile):
    (src, ) = minidom.parse(xmlFile).getElementsByTagName('source')
    (dir, ) = src.getElementsByTagName('celestial_dir')
    ra = string.atof(dir.getAttribute('ra'))
    dec = string.atof(dir.getAttribute('dec'))
    return ra, dec

#flare = FitsNTuple('test_events_0000.fits')
#flare = FitsNTuple('test_0.5_events_0000.fits')
#flare = FitsNTuple('test_0.25_events_0000.fits')
#flare = FitsNTuple('broad_flare_events_0000.fits')
flare = FitsNTuple('random_flare_events_0000.fits')
diffuse = FitsNTuple('eg_diffuse_events_0000.fits')

Roi_center = roiCenter('random_flare.xml')
Roi_radius = 10.

def get_times(data, center, radius=20):
    data.dist = celgal.dist(Roi_center, (data.RA, data.DEC))
    tmp = ma.masked_greater(data.dist, Roi_radius)
    times = ma.array(data.TIME, mask=tmp.mask())
    xx = [time for time in times.tolist() if time != times.fill_value()[0]]
    xx.sort()
    return xx

flare_times = get_times(flare, Roi_center, radius=Roi_radius)
diffuse_times = get_times(diffuse, Roi_center, radius=Roi_radius)

evt_times = flare_times + diffuse_times
evt_times.sort()

import hippoplotter as plot
hist = plot.histogram(evt_times)
plot.histogram(flare_times, oplot=1, color='red')

diffuse_blocks = BayesBlocks(evt_times)
lc_data = diffuse_blocks.computeLightCurve()
diffuse_lc = LightCurve(lc_data)

if "-ea" in sys.argv: # use effective Area
#    block_times = list(lc_data[0])
#    block_times.append(lc_data[1][-1])
#    if block_times[0] < 0:
#        block_times[0] = evt_times[0]
    block_times = num.arange(100)/99.*max(lc_data[0]) + evt_times[0]
    block_times = DoubleVector(block_times.tolist())
    my_exposure = Exposure('eg_diffuse_scData_0000.fits', block_times,
                           Roi_center[0], Roi_center[1])
    scaleFactors = DoubleVector()
    for t in evt_times:
        scaleFactors.append(my_exposure.value(t))
else:
    diffuse_only = BayesBlocks(diffuse_times)
    diffuse_only_lc = LightCurve(diffuse_only.computeLightCurve())
    scaleFactors = diffuse_only_lc(evt_times)
    
plot.scatter(evt_times, scaleFactors, pointRep='Line')

flare_blocks = BayesBlocks(evt_times, 4)
flare_blocks.setCellScaling(scaleFactors)

flc_data = flare_blocks.computeLightCurve()
flare_lc = LightCurve(flc_data)
(tt, ff) = flare_lc.dataPoints()
plot.canvas.selectDisplay(hist)
plot.scatter(tt, ff, oplot=1, color='green', pointRep='Line')

#(t0, f0) = diffuse_lc.dataPoints()
#plot.scatter(t0, f0, oplot=1, pointRep='Line', lineStyle='Dot')

#import os
#from read_data import read_data
#inputFile = os.path.join(os.environ["OBSERVATIONSIMROOT"],
#                         'data/pks1622-297_Template.dat')
#input_lc = read_data(inputFile)
#plot.scatter(input_lc[0], input_lc[1], pointRep='Line')

#cells = flare_blocks.cells()
#plot.histogram(cells, ylog=1)

#plot.scatter(tt, ff, xrange=(0, max(tt)/2.), pointRep='Line')

