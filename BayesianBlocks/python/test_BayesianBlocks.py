import sys
import time
import string
import random
import BayesianBlocks
from distributions import *
import numarray as num

evts = []
file = open("../data/events.dat")
for line in file:
    evts.append(string.atof(line.strip()))

my_blocks = BayesianBlocks.BayesianBlocks(evts)

tmins = BayesianBlocks.DoubleVector()
tmaxs = BayesianBlocks.DoubleVector()
numEvents = BayesianBlocks.DoubleVector()

if len(sys.argv) == 2:
    my_blocks.setNcpPrior(string.atof(sys.argv[1]))
t0 = time.time()
my_blocks.computeLightCurve(tmins, tmaxs, numEvents)
t1 = time.time()
print t1 - t0

import hippoplotter as plot

times = []
dens = []

for tmin, tmax, numEvts in zip(tmins, tmaxs, numEvents):
    my_dens = numEvts/(tmax - tmin)
    times.extend([tmin, tmax])
    dens.extend([my_dens, my_dens])

plot.clear()
#plot.histogram(evts, ylog=1)
plot.histogram(evts)
plot.scatter(times, dens, pointRep='Line', oplot=1, color='red')
