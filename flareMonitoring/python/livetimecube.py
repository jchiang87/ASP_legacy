"""
@brief Livetime cube calculation.

@author J. Carson <carson@slac.stanford.edu>
@author J. Chiang <jchiang@slac.stanford.edu>
"""
#
# $Header$
#

import os
from GtApp import GtApp
from parfile_parser import Parfile

debug = False

output_dir = os.environ['output_dir']
os.chdir(output_dir)

pars = Parfile(os.environ['PIPELINE_TASK'] + '.txt')

gtlivetimecube = GtApp('gtlivetimecube')
gtlivetimecube['evfile'] = pars['ft1file']
gtlivetimecube['scfile'] = pars['ft2file']
gtlivetimecube['outfile'] ='expCube.fits'

if debug:
    print gtlivetimecube.command()
else:
    gtlivetimecube.run()

# record output file in local parameter file

pars['expCube'] = gtlivetimecube['outfile']
pars.write()

os.system('chmod 777 *')
