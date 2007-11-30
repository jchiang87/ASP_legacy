"""
@brief Generate counts and exposure maps using Healpix arrays.
These will be used to compute light curve estimates comprising data
from consecutive downlink analyses.

@author J. Chiang <jchiang@slac.stanford.edu
"""
#
# $Header$
#

import os
from FitsNTuple import FitsNTuple
from generateMaps import CountsArrayFactory, ExposureArrayFactory

def get_tlims(ft1file):
    gti = FitsNTuple(ft1file, 'GTI')
    return min(gti.START), max(gti.STOP)

if __name__ == '__main__':
    output_dir = os.environ['OUTPUTDIR']
    os.chdir(output_dir)

    downlinkId = os.environ['DownlinkId']

    tmin, tmax = get_tlims('FT1_merged.fits')
    
    cmapFactory = CountsArrayFactory(('Filtered.fits',))
    cmap = cmapFactory.create(tmin, tmax)
    cmapfile = 'counts_%s.fits' % downlinkId
    cmap.write(cmapfile)

    #
    # awful kluge for 55d data: hardwire FT2 file and irfs
    #
    ft2file = '/nfs/farm/g/glast/u44/MC-tasks/Interleave55d-GR-v11r17/prune/FT2_55day_patch.fits'
    irfs = 'P5_v0_source'

    emapFactory = ExposureArrayFactory(ft2file, irfs=irfs)
    emap = emapFactory.create(tmin, tmax, 'FT1_merged.fits')
    emapfile = 'exposure_%s.fits' % downlinkId
    emap.write(emapfile)
    
    os.system('chmod 777 *')
