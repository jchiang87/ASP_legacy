import sys, os
sys.path.append('../python')
sys.path.append(os.path.join(os.environ['LIKEGUIROOT'], 'python'))
sys.path.append(os.path.join(os.environ['SANEROOT'], 'python'))
import numarray as num
from BayesBlocks import BayesBlocks, LightCurve
from BayesianBlocks import Exposure, DoubleVector

from distributions import sample

npts = 100
phi = num.arange(npts, type=num.Float)/(npts-1)*2.*num.pi
func = 1. + num.sin(phi)

nsamp = 1000
events = sample(func, nsamp)*2.*num.pi

my_blocks = BayesBlocks(events.tolist(), 4)
lc = LightCurve(my_blocks.computeLightCurve())

(x, y) = lc.dataPoints()

import hippoplotter as plot
hist = plot.histogram(events, 'phi')
plot.scatter(x, y, pointRep='Line', oplot=1, lineStyle='Dot')

