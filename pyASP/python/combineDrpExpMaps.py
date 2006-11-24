"""
@brief Combine gtexpmap submaps for DRP monitoring.

@author J. Chiang <jchiang@slac.stanford.edu>
"""
#
# $Header$
#

import os
from combineExpMaps import combineExpMaps

from drpRoiSetup import rootpath, pars, rois

id = int(os.environ['ROI_ID'])
name, ra, dec, radius, sourcerad = rois[id]

os.chdir(name)

combineExpMaps(outfile=pars['expMap'])

os.system('chmod 666 *')
