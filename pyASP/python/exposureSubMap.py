"""
@brief Run gtexpmap for specified submaps to be run in parallel.

@author J. Chiang <jchiang@slac.stanford.edu>
"""
#
# $Header$
#

import os
from GtApp import GtApp
from combineExpMaps import readExpMapBounds

def exposureSubMap(outputDir, debug=False):
    os.chdir(outputDir)
    bounds = readExpMapBounds()

# Account for off-by-one error in how jobs can be numbered in P-II xml code.
    map_id = int(os.environ["EXPMAP_ID"]) - 1  

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

    os.system('chmod 666 *')

if __name__ == '__main__':
    pass
## include this code for backwards compatibility    
#    from drpRoiSetup import rootpath, pars, rois
#    id = int(os.environ['ROI_ID']) - 1
#    outputDir = rois[id].name
#    exposureSubMap(outputDir, debug=False)
    
