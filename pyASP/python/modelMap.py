"""
@brief Make model maps.

@author W. Focke <focke@slac.stanford.edu>
"""

import os

from GtApp import GtApp

gtmodelmap = GtApp('gtmodelmap')

parfile_basename = os.environ['PIPELINE_TASK'] + '.txt'
pars = Parfile(parfile_basename)

gtmodelmap['srcmaps'] = pars['source_map']
gtmodelmap['source_model_file'] = pars['model_file']
gtmodelmap['outfile'] = 'modelMap.fits'

pars['model_map'] = gtmodelmap['outfile']
pars.write()

if debug:
    print gtmodelmap.command()
else:
    gtmodelmap.run()
