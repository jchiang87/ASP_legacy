"""
@brief Refine a GRB position and fit a power-law spectrum using LAT L1
data with initial position and timing from a GBM Notice.

@author J. Chiang <jchiang@slac.stanford.edu>
"""
#
# $Header$
#

import os
from GbmNotice import GbmNotice
from getL1Data import getL1Data
from ft1merge import ft1merge
from refinePosition import refinePosition
from LatGrbSpectrum import LatGrbSpectrum

#os.chdir(os.environ['OUTPUTDIR'])
#GbmFile = os.environ['GBMNOTICE']
os.chdir('/nfs/farm/g/glast/u33/jchiang/ASP/pyASP/v0r1/python/GRB_test/output')
GbmFile = '/nfs/farm/g/glast/u33/jchiang/ASP/GRB/Notices/GLG_NOTICE_080104514.TXT'

duration = 100
ft1Merged = 'FT1_merged.fits'   # temporary file for FT1 data

gbmNotice = GbmNotice(GbmFile)
if gbmNotice.offAxisAngle() < 60 and not gbmNotice.inSAA():
    ft1, ft2 = getL1Data(gbmNotice.start_time - duration,
                         gbmNotice.start_time + duration)
    ft1merge(ft1, ft1Merged)
    gbmNotice = refinePosition(gbmNotice, ft1Input=ft1Merged, tsmap=False,
                               duration=duration)
    like = LatGrbSpectrum(gbmNotice, ft1File=ft1Merged)
else:
    print ("GRB lies outside the nominal LAT FOV "
           + " or triggered during an SAA passage.")
