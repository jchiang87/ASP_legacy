import sys, os
sys.path.append('../python')
sys.path.append(os.path.join(os.environ['LIKEGUIROOT'], 'python'))
sys.path.append(os.path.join(os.environ['SANEROOT'], 'python'))
import numarray as num
from BayesBlocks import BayesBlocks, LightCurve
from BayesianBlocks import Exposure, DoubleVector

from distributions import sample, stepFunction

nsamp = 200
events = sample(stepFunction(0.5, 0.7, amp=0.5), nsamp)

fine_blocks = BayesBlocks(events.tolist(), 1)
#rough_blocks = BayesBlocks(events.tolist(), 4)

fine_lc = LightCurve(fine_blocks.computeLightCurve())
#rough_lc = LightCurve(rough_blocks.computeLightCurve())

(x, y) = fine_lc.dataPoints()
#(xx, yy) = rough_lc.dataPoints()

import hippoplotter as plot
hist = plot.histogram(events, 'x')
reps = hist.getDataReps()
reps[0].setErrorDisplay('y', 1)
plot.scatter(x, y, pointRep='Line', oplot=1, color='red')

#plot.scatter(xx, yy, pointRep='Line', oplot=1, lineStyle='Dash')

