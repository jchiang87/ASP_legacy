"""
@brief Make source maps.

@author W. Focke <focke@slac.stanford.edu>
"""

import os

from GtApp import GtApp

_ft2File = '/nfs/farm/g/glast/u33/jchiang/ASP/testdata/eg_diffuse_scData_0000.fits'

gtsrcmaps = GtApp('gtsrcmaps')

parfile_basename = os.environ['PIPELINE_TASK'] + '.txt'
pars = Parfile(parfile_basename)

gtsrcmaps['scfile'] = pars['ft2file']
gtsrcmaps['exposure_cube_file'] = pars['expCube']
gtsrcmaps['counts_map_file'] = pars['countMap']
gtsrcmaps['source_model_file'] = pars['model_file']
gtsrcmaps['binned_exposure_map'] = 'binned_exposure.fits'
gtsrcmaps['outfile'] = 'sourceMap.fits'

pars['source_map'] = gtsrcmaps['outfile']
pars.write()

if debug:
    print gtsrcmaps.command()
else:
    gtsrcmaps.run()
