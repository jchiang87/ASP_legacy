"""
@brief Use psf to construct spatial part of log-likelihood and to
determine cluster locations.

@author J. Chiang <jchiang@sla.stanford.edu>
"""
#
# $Header$
#

import numarray as num
import pyIrfLoader
from ScData import ScData
from blind_search import triggerTimes, convert

_ft2File = '/nfs/farm/g/glast/u33/jchiang/DC2/DC2_FT2_v2.fits'
_scData = ScData(_ft2File)

pyIrfLoader.Loader_go()
_irfsFactory = pyIrfLoader.IrfsFactory_instance()

_psfs = []
_psfs.append(_irfsFactory.create('DC2::FrontA').psf())
_psfs.append(_irfsFactory.create('DC2::BackA').psf())
_psfs.append(_irfsFactory.create('DC2::FrontB').psf())
_psfs.append(_irfsFactory.create('DC2::BackB').psf())

class PsfClusters(object):
    def __init__(self, events):
        dists = {}
        for evt in events:
            dists[evt] = []
            for other in events:
                dists[evt].append( (evt.sep(other), other) )
        self.dists = dists
    def _clusterSizes(self):
        sizes = {}
        for evt in self.dists:
            sizes[evt] = self._psfLogLike(evt)
        return sizes
    def _psfLogLike(self, evt):
        logLike = 0
        psf_wts = {}
        theta = _scData.inclination(evt.time, evt.dir)
        for sep, other in self.dists[evt]:
            psf = _psfs[evt.evt_class]
            psf_wts[other] = psf.value(sep, other.energy, theta, 0)
            logLike += num.log(psf_wts[other])
        return logLike, psf_wts
    def largestCluster(self, radius=None):
        sizes = self._clusterSizes()
        maxval = sizes[sizes.keys()[0]]
        for evt in sizes:
            if maxval[0] < sizes[evt][0]:
                largest = evt
                maxval = sizes[evt]
        return maxval
    def logLike(self, radius=None, bg_rate=None):
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

        max_cluster = self.largestCluster()
        logPdists = max_cluster[0]
        
        return logPdts, logPdists

class BlindSearch(object):
    def __init__(self, events, dn=20, deadtime=1000):
        self.events = events
        nevts = len(events.RA)
        indices = range(0, nevts, dn)
        indices.append(nevts)
        logdts = []
        logdists = []
        times = []
        bg_rate = nevts/(events.TIME[-1] - events.TIME[0])
        for imin, imax in zip(indices[:-1], indices[1:]):
            clusters = PsfClusters(convert(events, imin, imax))
            try:
                logPdts, logPdists = clusters.logLike(bg_rate=bg_rate)
                logdts.append(logPdts)
                logdists.append(logPdists)
                times.append((events.TIME[imin] + events.TIME[imax-1])/2.)
            except ValueError:
                pass
        self.times = num.array(times)
        self.logdts = num.array(logdts)
        self.logdists = num.array(logdists)
        logLike = self.logdts + self.logdists
        self.triggers, self.tpeaks = triggerTimes(times, -logLike,
                                                  deadtime=deadtime)

if __name__ == '__main__':
    from FitsNTuple import FitsNTuple
    import hippoplotter as plot
    
    downlink = '/nfs/farm/g/glast/u33/jchiang/DC2/Downlinks/downlink_0028.fits'
    blindSearch = BlindSearch(FitsNTuple(downlink))
    
    plot.scatter(blindSearch.times, blindSearch.logdts, pointRep='Line')
    plot.scatter(blindSearch.times, blindSearch.logdists, pointRep='Line')
    logLike = blindSearch.logdts - blindSearch.logdists
    plot.scatter(blindSearch.times, logLike, pointRep='Line')
