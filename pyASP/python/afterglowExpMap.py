"""
@brief Run gtexpmap for GRB afterglow analysis, using specified submaps
to be run in parallel.

@author J. Chiang <jchiang@slac.stanford.edu>
"""
#
# $Header$
#

import os
from GtApp import GtApp
from combineExpMaps import readExpMapBounds

debug = False

os.chdir(os.environ['OUTPUTDIR'])
bounds = readExpMapBounds()
map_id = int(os.environ["EXPMAP_ID"])

gtexpmap = GtApp('gtexpmap')
gtexpmap['outfile'] = bounds[map_id].filename
gtexpmap['compute_submap'] = 'yes'
gtexpmap['nlongmin'] = bounds[map_id].xmin
gtexpmap['nlongmax'] = bounds[map_id].xmax
gtexpmap['nlatmin'] = bounds[map_id].ymin
gtexpmap['nlatmax'] = bounds[map_id].ymax

if debug:
    print gtexpmap.command()
else:
    gtexpmap.run()