"""
@brief Implementation of Jay and Jerry's GRB blind search algorithm.

@author J. Chiang <jchiang@slac.stanford.edu>
"""
#
# $Header$
#

import numarray as num
from pyASP import SkyDir

_eventId = 0
class Event(object):
    def __init__(self, ra, dec, time):
        self.dir = SkyDir(ra, dec)
        self.ra, self.dec = ra, dec
        self.time = time
        global _eventId
        self.id = _eventId
        _eventId += 1
    def sep(self, event):
        return self.dir.difference(event.dir)*180./num.pi
    def __eq__(self, other):
        return self.id == other.id
    def __ne__(self, other):
        return not self==other
    def __repr__(self):
        #return '%.3f %.3f %.3f' % (self.ra, self.dec, self.time)
        return `self.id`

def cluster_dists(cluster):
    """Cluster distances from mean direction in radians"""
    meanDir = cluster[0].dir
    for item in cluster[1:]:
        meanDir += item.dir
    dists = []
    for item in cluster:
        dists.append(item.dir.difference(meanDir))
    return num.array(dists)

class EventClusters(object):
    def __init__(self, events):
        dists = {}
        for evt in events:
            dists[evt] = []
            for other in events:
                dists[evt].append(evt.sep(other))
            dists[evt] = num.array(dists[evt])
        self.dists = dists
    def clusterSizes(self, radius=10):
        sizes = {}
        for evt in self.dists:
            sizes[evt] = len(num.where(self.dists[evt] < radius)[0])
        return sizes
    def findCluster(self, event, radius):
        cluster = []
        for evt in self.dists:
            if evt.sep(event) < radius:
                cluster.append(evt)
        return cluster
    def largestCluster(self, radius):
        sizes = self.clusterSizes(radius)
        maxnum = 0
        for evt in sizes:
            if maxnum < sizes[evt]:
                largest = evt
                maxnum = sizes[evt]
        return self.findCluster(largest, radius)
    def logLike(self, radius=17, bg_rate=None):
        times = []
        for evt in self.dists:
            times.append(evt.time)
        times.sort()
        times = num.array(times)
        dts = times[1:] - times[:-1]
        if bg_rate is None:
            bg_rate = len(times)/(times[-1] - times[0])
        xvals = bg_rate*dts
        logPdts = sum(num.log(1. - num.exp(-xvals)))

        max_cluster = self.largestCluster(radius)
        if len(max_cluster) < 2:
            raise ValueError, 'Largest cluster size < 2'
        dists = cluster_dists(max_cluster)
        logPdists = sum(num.log(1. - num.cos(dists)))

        return logPdts, logPdists

def convert(events, imin=0, imax=None):
    if imax is None:
        imax = len(events.RA)
    my_events = []
    for ra, dec, time in zip(events.RA[imin:imax], events.DEC[imin:imax],
                             events.TIME[imin:imax]):
        my_events.append(Event(ra, dec, time))
    return my_events

def triggerTimes(time, logLike, threshold=112, deadtime=0):
    """Find trigger times and peak times based on a time-ordered
    figure-of-merit (FOM), such as Jay and Jerry's -log(likelihood).
    Return the initial time the FOM is above threshold, resetting the
    trigger when the FOM goes back below threshold or after an
    artificial deadtime."""
    triggers = []
    tpeaks = []
    trigger_is_set = True
    lmax = 0
    tmax = time[0]
    for tt, ll in zip(time, logLike):
        if (trigger_is_set and ll > threshold and
            (len(triggers) == 0 or (tt - triggers[-1]) > deadtime)):
            triggers.append(tt)
            trigger_is_set = False
        if not trigger_is_set:
            if ll > lmax:
                lmax = ll
                tmax = tt
        if not trigger_is_set and ll <= threshold:
            tpeaks.append(tmax)
            lmax = 0
            trigger_is_set = True
    return triggers, tpeaks

if __name__ == '__main__':
    import hippoplotter as plot
    from FitsNTuple import FitsNTuple
    events = FitsNTuple('/nfs/farm/g/glast/u33/jchiang/DC2/Downlinks/downlink_0039.fits')
    nevts = len(events.RA)
    dn = 20
    indices = range(0, nevts, dn)
    indices.append(nevts)
    logdts = []
    logdists = []
    times = []
    bg_rate = nevts/(events.TIME[-1] - events.TIME[0])
    for imin, imax in zip(indices[:-1], indices[1:]):
        clusters = EventClusters(convert(events, imin, imax))
        try:
            logPdts, logPdists = clusters.logLike(bg_rate=bg_rate)
            logdts.append(logPdts)
            logdists.append(logPdists)
            times.append((events.TIME[imin] + events.TIME[imax-1])/2.)
        except ValueError:
            pass
    logdts = num.array(logdts)
    logdists = num.array(logdists)
    plot.scatter(times, logdts, pointRep='Line')
    plot.scatter(times, logdists, pointRep='Line')
    logLike = logdts + logdists
    plot.scatter(times, logLike, pointRep='Line')

    triggers, tpeaks = triggerTimes(times, -logLike, deadtime=1000)
    for item in tpeaks:
        plot.vline(item, color='red')

    hist = plot.histogram(events.TIME)
    hist.setBinWidth('x', 5)
    for item in tpeaks:
        plot.vline(item, color='red')

#    import hippoplotter as plot
#    import random
#
#    disp = plot.scatter([], [], xrange=(0, 360), yrange=(-90, 90))
#    my_events = plot.pickData()
#    events = []
#    time = 0
#    for i in range(my_events.rows):
#        ra, dec, z, px, py = my_events.getRow(i)
#        time += random.random()
#        events.append(Event(ra, dec, time))
#        
#    clusters = EventClusters(events)
#    radius = 17
#    max_cluster = clusters.largestCluster(radius)
#
#    nt = plot.newNTuple(([], []), ('ra', 'dec'))
#    for item in max_cluster:
#        nt.addRow((item.ra, item.dec))
#    plot.canvas.selectDisplay(disp)
#    plot.Scatter(nt, 'ra', 'dec', oplot=1, color='green')
#
#    print clusters.logLike(17)
