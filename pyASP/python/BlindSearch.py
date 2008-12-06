"""
@brief Implementation of Jay and Jerry's GRB blind search algorithm.

@author J. Chiang <jchiang@slac.stanford.edu>
"""
#
# $Header$
#

import numarray as num
from pyIrfLoader import SkyDir
from EventClusters import *

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

class BlindSearch(object):
    def __init__(self, events, dn=20, deadtime=1000, threshold=112,
                 clusterAlg=EventClusters):
        """events is a FitsNTuple of an FT1 file(s);
        dn is the number of consecutive events (in time) to consider;
        deadtime is the time in seconds to wait for the current trigger state
           to expire (for long bursts or Solar flares);
        threshold is the trigger threshold in terms of -log-likelihood for
           identifying a burst;
        clusterAlg is the clustering algorithm, either EventClusters to use
           JPN and JB's algorithm or PsfClusters to use the Psf.
        """
        self.clusterAlg = clusterAlg 
        self.events = events
        nevts = len(events.RA)
        indices = range(0, nevts, dn)
        indices.append(nevts)
        logdts = []
        logdists = []
        times = []
        bg_rate = nevts/(events.TIME[-1] - events.TIME[0])
        for imin, imax in zip(indices[:-1], indices[1:]):
            clusters = self.clusterAlg(convert(events, imin, imax))
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
                                                  deadtime=deadtime,
                                                  threshold=threshold)
    def grbDirs(self, radius=5):
        """Go through the list of candidate bursts, and return a list
        of SkyDirs, event (ras, decs), and peak times.
        """
        events = self.events
        grb_dirs = []
        for tpeak in self.tpeaks:
            imin = min(num.where(events.TIME > tpeak-50)[0])
            imax = max(num.where(events.TIME < tpeak+50)[0])
            clusters = self.clusterAlg(convert(events, imin, imax))
            grb_dir = list(clusters.localize())
            grb_dir.append(tpeak)
            grb_dirs.append(grb_dir)
        return grb_dirs

if __name__ == '__main__':
    import os
    import sys
    from FitsNTuple import FitsNTuple
    from LatGcnNotice import LatGcnNotice
    import createGrbStreams

    try:
        sys.argv[1:].index('-p')
        makePlots = True
    except ValueError:
        makePlots = False
    
    grbroot_dir = os.path.abspath(os.environ['GRBROOTDIR'])
    output_dir = os.path.abspath(os.environ['OUTPUTDIR'])
    downlink_file = os.path.abspath(os.environ['DOWNLINKFILE'])

    os.chdir(grbroot_dir)  # test to see if this directory exists
    os.chdir(output_dir)   # move to the working directory

    events = FitsNTuple(downlink_file)

    blindSearch = BlindSearch(events)

    if makePlots:
        import hippoplotter as plot
        plot.scatter(blindSearch.times, blindSearch.logdts, pointRep='Line')
        plot.scatter(blindSearch.times, blindSearch.logdists, pointRep='Line')
        logLike = blindSearch.logdts + blindSearch.logdists
        plot.scatter(blindSearch.times, logLike, pointRep='Line')
        
        for item in blindSearch.tpeaks:
            plot.vline(item, color='red')

        hist = plot.histogram(events.TIME)
        hist.setBinWidth('x', 5)

    grbDirs = blindSearch.grbDirs()
    for item in grbDirs:
        grb_dir, ras, decs, tpeak = item
        notice = LatGcnNotice(tpeak, grb_dir.ra(), grb_dir.dec())
        grb_output = os.path.join(grbroot_dir, notice.name)
        try:
            os.mkdir(grb_output)
            os.system('chmod 777 %s' % grb_output)
        except OSError:
            if os.path.isdir(grb_output):
                os.system('chmod 777 %s' % grb_output)
            else:
                raise OSError, "Error creating directory: " + grb_output
        outfile = os.path.join(grb_output, notice.name + '_Notice.txt')
        notice.write(outfile)
        os.system('chmod 666 %s' %  outfile) 
        print grb_dir.ra(), grb_dir.dec(), tpeak
        
        if makePlots:
            plot.xyhist(ras, decs)
            plot.vline(grb_dir.ra())
            plot.hline(grb_dir.dec())
        else:
            createGrbStreams.refinementStreams(output_dir=grb_output)
