"""
@brief Compute the file information for downlink files.

@author J. Chiang <jchiang@slac.stanford.edu>
"""
#
# $Header$
#

import os
import pyfits

def getObsTimes(ft1File):
    events = pyfits.open(ft1File)["EVENTS"]
    return events["TSTART"], events["TSTOP"]

variables = {}
variables["downlinkDir"] = "/nfs/farm/g/glast/u33/DC2/Downlinks"
variables["downlinkFile"] = "downlink_0000.fits"

tstart, tstop = getObsTimes(variables["downlinkFile"])
variables["tstart"] = "%i" % tstart
variables["tstop"] = "%i" % tstop

summary = open(os.environ["PIPELINE_SUMMARY"], 'a')
for item in variables:
    summary.write("%s : %s" % (item, variables[item]))
summary.close()
