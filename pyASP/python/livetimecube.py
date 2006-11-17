"""
@brief Livetime cube calculation.
@author J. Chiang <jchiang@slac.stanford.edu>
@author J. Carson <carson@slac.stanford.edu>
"""
#
# $Header$
#

import os
from GtApp import GtApp
import readXml
import xmlSrcLib
from parfile_parser import Parfile

os.chdir(os.environ['root_output_dir'])

pars = Parfile('drp_pars.txt')

gtlivetimecube = GtApp('gtlivetimecube')

gtlivetimecube['evfile'] = pars['ft1file']
gtlivetimecube['scfile'] = pars['ft2file']
gtlivetimecube['outfile'] ='expCube.fits'
gtlivetimecube.run()

pars['expCubeFile'] = gtlivetimecube['outfile']
pars.write()
