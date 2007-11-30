"""
@brief Fill a 'database table' (a cPickled dictionary) with light curves
for all of the HealPixels that have a source detected in them by pgwave.

@author J. Chiang <jchiang@slac.stanford.edu>
"""
#
# $Header$
#

import os
import glob
import cPickle
import numarray as num
from FitsNTuple import FitsNTuple
from HealPix import Pixel, SkyDir, CountsArray, ExposureArray, Healpix
from generateMaps import CountsArrayFactory, ExposureArrayFactory
from read_data import read_data

class LightCurve(object):
    def __init__(self, ra, dec):
        self.ra, self.dec = ra, dec
        self.time = []
        self.counts = []
        self.exposure = []
    def append(self, time, counts, exposure):
        self.time.append(time)
        self.counts.append(counts)
        self.exposure.append(exposure)

def get_tlims(ft1file):
    gti = FitsNTuple(ft1file, 'GTI')
    return min(gti.START), max(gti.STOP)

if __name__ == '__main__':
    pgwave_dir = os.environ['output_dir']
    os.chdir(pgwave_dir)
    
    downlinks = glob.glob(os.path.join(pgwave_dir, '2*'))
    downlinks.sort()

    #
    # kluge: hardwire FT2 file for Interleave55d
    #
    ft2file = '/nfs/farm/g/glast/u44/MC-tasks/Interleave55d-GR-v11r17/prune/FT2_55day_patch.fits'

    hp = Healpix(16, Healpix.NESTED, SkyDir.GALACTIC)
    #
    # Read in current pixel info.
    #
    try:
        lightCurves = cPickle.load(open('lc_data'))
    except IOError:
        lightCurves = {}
    hot_pixels = {}
    for key in lightCurves:
        hot_pixels[key] = Pixel(SkyDir(*hp.pix2coord(key)), hp)

    #
    # Add interesting pixels from current downlink.
    #
    datapath = lambda x : os.path.join(os.environ['OUTPUTDIR'], x)
    pgwave = read_data(datapath('Filtered_evt_map.list'))
    for ra, dec in zip(pgwave[3], pgwave[4]):
        pix = Pixel(SkyDir(ra, dec), hp)
        hot_pixels[pix.index()] = pix
        
    #
    # Rebuild light curves for all pixels:
    #
    for downlink in downlinks:
        datapath = lambda x : os.path.join(downlink, x)
        tmin, tmax = get_tlims(datapath('FT1_merged.fits'))
        
        cmapfile = datapath('counts_%s.fits' % os.path.basename(downlink))
        if not os.path.isfile(cmapfile):
            break
        cmap = CountsArray(cmapfile)

        emapfile = datapath('exposure_%s.fits' % os.path.basename(downlink))
        if not os.path.isfile(emapfile):
            break
        emap = ExposureArray(emapfile)

        time = int(os.path.basename(downlink))
        for pix in hot_pixels:
            my_dir = SkyDir(hot_pixels[pix].ra(), hot_pixels[pix].dec())
            if not lightCurves.has_key(pix):
                lightCurves[pix] = LightCurve(my_dir.ra(), my_dir.dec())
            lightCurves[pix].append(time, cmap[my_dir], emap[my_dir])

    try:
        os.rename('lc_data', 'lc_data_save')
    except OSError:
        pass
    cPickle.dump(lightCurves, open('lc_data', 'w'), protocol=2)
    os.system('chmod 666 lc_data')
    
