"""
@brief Common setup for DRP region-of-interest analyses starting from
the directory given in the root_output_dir environment variable.
Importing this at the top of a script will set the cwd to the
root_output_dir and make available the parameters in drp_pars.txt and
the RoI_file data after the getIntervalData.py script has been run.

@author J. Chiang <jchiang@slac.stanford.edu>
"""
#
# $Header$
#

import os
from parfile_parser import Parfile
from read_data import read_data

_roiFile = os.path.join(os.environ['PYASPROOT'], 'data', 'rois.txt')

class RoI(object):
    def __init__(self, region, ra, dec, radius, sourcerad):
        """The region name is constructed using self.name =
        'region%03i' % int(region)
        """
        self.name = 'region%03i' % int(region)
        self.ra, self.dec, self.radius, self.sourcerad = (ra, dec, radius,
                                                          sourcerad)
        
class RoiList(list):
    def __init__(self, roiFile=_roiFile):
        for reg, ra, dec, radius, sourcerad in zip(*read_data(roiFile)):
            self.append(RoI(reg, ra, dec, radius, sourcerad))

root_output_dir = os.environ['root_output_dir']
os.chdir(root_output_dir)

rootpath = lambda x : os.path.join(root_output_dir, x)
pars = Parfile('drp_pars.txt')
rois = RoIs(pars['RoI_file'])
