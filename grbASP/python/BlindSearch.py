"""
@brief Implementation of Jay and Jerry's GRB blind search algorithm.

@author J. Chiang <jchiang@slac.stanford.edu>
"""
#
# $Header$
#

import numarray as num
from pyASP import SkyDir
from grbASP import Event, EventClusters, PsfClusters, ScData

def convert(events, imin=0, imax=None):
    if imax is None:
        imax = len(events.RA)
    my_events = []
    for evt_tuple in zip(events.RA[imin:imax], events.DEC[imin:imax],
                         events.TIME[imin:imax], events.ENERGY[imin:imax],
                         events.EVENT_CLASS[imin:imax]):
        my_events.append(Event(*evt_tuple))
    return my_events

def triggerTimes(time, logLike, threshold=112, deadtime=0):
    """Find trigger times and peak times based on a time-ordered
    figure-of-merit (FOM), such as Jay and Jerry's -log(likelihood).
    Return the initial time the FOM is above threshold, resetting the
    trigger when the FOM goes back below threshold or after an
    artificial deadtime."""
    triggers = []
    tpeaks = []
    ll_values = []
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
            ll_values.append(lmax)
            lmax = 0
            trigger_is_set = True
    return triggers, tpeaks, ll_values

def downlink_bg_rate(events, imin, imax):
    times = events.TIME
    offset = 0
    localmin = max(0, imin - offset)
    localmax = min(len(times)-1, imax + offset)
    return (localmax - localmin)/(times[localmax] - times[localmin])

class BlindSearch(object):
    def __init__(self, events, clusterAlg, dn=20, deadtime=1000, threshold=92,
                 bg_rate=0):
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
        ras, decs = [], []
        ls, bs = [], []
        mean_bg_rate = nevts/(events.TIME[-1] - events.TIME[0])
        for imin, imax in zip(indices[:-1], indices[1:]):
            try:
                results = clusterAlg.processEvents(convert(events, imin, imax),
                                                   bg_rate)
                (logPdts, logPdists), meanDir = results
                ra, dec = meanDir.ra(), meanDir.dec()
                l, b = meanDir.l(), meanDir.b()
                logdts.append(logPdts)
                logdists.append(logPdists)
                times.append((events.TIME[imin] + events.TIME[imax-1])/2.)
                ras.append(ra)
                decs.append(dec)
                ls.append(l)
                bs.append(b)
            except ValueError:
                pass
        self.times = num.array(times)
        self.logdts = num.array(logdts)
        self.logdists = num.array(logdists)
        self.ras = num.array(ras)
        self.decs = num.array(decs)
        self.glons = num.array(ls)
        self.glats = num.array(bs)
        logLike = self.logdts + self.logdists
        self.triggers, self.tpeaks, self.ll = triggerTimes(times, -logLike,
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
            try:
                results = self.clusterAlg.processEvents(convert(events,
                                                                imin, imax))
                grb_dir = [results[1]]
                grb_dir.append(tpeak)
                grb_dirs.append(grb_dir)
            except:
                pass
 
        return grb_dirs

def read_gtis(ft1files):
    data = FitsNTuple(ft1files, 'GTI')
    gtis = []
    for start, stop in zip(data.START, data.STOP):
        gtis.append((start, stop))
    return gtis

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

    clusterAlg = EventClusters(read_gtis(downlink_file))

    blindSearch = BlindSearch(events, clusterAlg)

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
        grb_dir, tpeak = item
        notice = LatGcnNotice(tpeak, grb_dir.ra(), grb_dir.dec())
        grb_output = os.path.join(grbroot_dir, notice.name)
        try:
            os.mkdir(grb_output)
            os.chmod(grb_output, 0777)
        except OSError:
            if os.path.isdir(grb_output):
                os.chmod(grb_output, 0777)
            else:
                raise OSError, "Error creating directory: " + grb_output
        outfile = os.path.join(grb_output, notice.name + '_Notice.txt')
        notice.write(outfile)
        os.chmod(outfile, 0666)
        print grb_dir.ra(), grb_dir.dec(), tpeak
        
        if makePlots:
            plot.vline(grb_dir.ra())
            plot.hline(grb_dir.dec())
        else:
            pass
            createGrbStreams.refinementStreams(output_dir=grb_output)