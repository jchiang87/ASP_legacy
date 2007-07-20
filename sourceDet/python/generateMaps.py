"""
@brief Generate healpix counts and exposure maps for specified time
intervals.

@author J. Chiang <jchiang@slac.stanford.edu>
"""
#
# $Header$
#

import os
import glob
from GtApp import GtApp
from HealPix import *

gtltcube = GtApp('gtlivetimecube')

class CountsArrayFactory(object):
    def __init__(self, ft1Files, nside=16):
        self.ft1Files = ft1Files
        self.hp = Healpix(nside, Healpix.NESTED, SkyDir.GALACTIC)
    def create(self, tmin, tmax, emin=100, emax=3e5):
        cmap = CountsArray(self.hp)
        filter = "(TIME >= %i) && (TIME <= %i)" % (tmin, tmax)
        filter += " && (ENERGY >= %.3f) && (ENERGY <= %.3f)" % (emin, emax)
        for ft1File in self.ft1Files:
            cmap.binCounts(ft1File, filter)
        return cmap

class ExposureArrayFactory(object):
    def __init__(self, ft2File, nside=16, irfs="HANDOFF"):
        self.ft2File = ft2File
        self.hp = Healpix(nside, Healpix.NESTED, SkyDir.EQUATORIAL)
        self.irfs = irfs
    def create(self, tmin, tmax, emin=100, emax=3e5):
        emap = ExposureArray(self.hp)
        gtltcube['evfile'] = ''
        gtltcube['scfile'] = self.ft2File
        gtltcube['tmin'] = tmin
        gtltcube['tmax'] = tmax
        gtltcube['outfile'] = 'expCube_%i_%i.fits' % (tmin/8.64e4, tmax/8.64e4)
        gtltcube.run()
        emap.computeExposure(self.irfs, gtltcube['outfile'])
        return emap

if __name__ == '__main__':
    null_dir = '/u/gl/jchiang/u33/GRB_IRFs/custom_irfs/standard_sims'
    ft1Files = glob.glob(os.path.join(null_dir, 'filtered_*.fits'))
    ft2File = os.path.join(null_dir, 'test_scData_0000.fits')

    def generateMaps():
        cmapFactory = CountsArrayFactory(ft1Files)
        emapFactory = ExposureArrayFactory(ft2File)
        days = range(30)
        for day in days[2:]:
            tmin = day*8.64e4
            tmax = tmin + 8.64e4
            cmap = cmapFactory.create(tmin, tmax)
            cmap.write('counts_%03i.fits' % day)
            emap = emapFactory.create(tmin, tmax)
            emap.write('exposure_%03i.fits' % day)

    generateMaps()
