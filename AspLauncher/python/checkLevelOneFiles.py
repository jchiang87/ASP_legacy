"""
@file checkLevelOneFiles.py

@brief Check the coverage of the Level 1 files for a given time
interval and determine if the task(s) associated with that interval
should be launched.

@author J. Chiang <jchiang@slac.stanford.edu>
"""
#
# $Header$
#

import os
import pyfits
from FitsNTuple import FitsNTuple
from getFitsData import getFitsData, getStagedFitsData

def consolidate(intervals):
    "Join consecutive intervals that have matching end points."
    bar = [intervals[0]]
    for xx in intervals[1:]:
        if bar[-1][1] == xx[0]:
            bar[-1][1] = xx[1]
        else:
            bar.append(xx)
    return bar

def check_ft2(gtis, ft2):
    """Ensure that the GTIs are contained within contiguous intervals
    covered by the FT2 files."""
    if not ft2:       # an empty set of files cannot cover the gtis
        raise RuntimeError, "FT2 file list is empty"
    tbounds = []
    for item in ft2:
        foo = pyfits.open(item)
        tbounds.append( (int(foo[0].header['TSTART']),
                         int(foo[0].header['TSTOP'])) )
    tbounds.sort()
    tbounds = consolidate(tbounds)
    for tmin, tmax in zip(gtis.START, gtis.STOP):
        covered = False
        for tbound in tbounds:
            if tbound[0] <= tmin and tmax <= tbound[1]:
                covered = True
        if not covered:
            raise RuntimeError, "FT2 files do not cover the FT1 data"

def providesCoverage(tstart, tstop, min_frac=0.70, ft1List='Ft1FileList',
                     ft2List='Ft1FileList', fileStager=None):
    """Ensure the FT2 files cover the desired GTIs and compute the
    fraction of the elapsed time that is covered by the GTIs.  Return
    False if the desired minumum fractional coverage is not
    achieved."""
    print "cwd = ", os.path.abspath(os.curdir)
    if fileStager is None:
        ft1, ft2 = getFitsData(ft1List, ft2List, copylist=False)
    else:
        ft1, ft2 = getStagedFitsData(ft1List, ft2List, fileStager=fileStager)
    if not ft1 or not ft2:  # at least one file list is empty
        return False
    gtis = FitsNTuple(ft1, 'GTI')
    check_ft2(gtis, ft2)
    print "Requested tstart, tstop: ", tstart, tstop
    print "GTI range: ", min(gtis.START), max(gtis.STOP)
    total = 0
    for tmin, tmax in zip(gtis.START, gtis.STOP):
        total += tmax - tmin
    print "Fractional coverage of FT1 files: ", total/(tstop - tstart)
    if total/(tstop - tstart) > min_frac:
        return True
    return False
