"""
@brief Use gtfindsrc to refine the burst position based on a GBM Notice
and create a TS map using gttsmap.

@author J. Chiang <jchiang@slac.stanford.edu>
"""
#
# $Header$
#
import numarray as num
from GbmNotice import GbmNotice
from extractLatData import extractLatData, burst_interval
from getApp import GtApp
from errEst import errEst

# defaults for DC2 data
_LatFt1File = '/nfs/farm/g/glast/u33/jchiang/DC2/FT1_merged_gti.fits'
_LatFt2File = '/nfs/farm/g/glast/u33/jchiang/DC2/DC2_FT2_v2.fits'

gtfindsrc = GtApp('gtfindsrc')

def refinePosition(gbm_notice, extracted=False, ft1Input=_LatFt1File,
                   ft2Input=_LatFt2File):
    notice = GbmNotice(gbm_notice)
    if notice.offAxisAngle() > 60:
        raise ValueError, ("Burst off-axis angle (from GBM position) "
                           + "> 60 degrees and so lies outside the "
                           + "nominal LAT FOV.")
    if not extracted:
        ft1_file, lc_file = extractLatData(notice, ft1File=ft1Input)
    else:
        ft1_file = notice.Name + '_LAT_2.fits'
        lc_file = notice.Name + '_LAT_lc_2.fits'

    gtfindsrc['evfile'] = ft1_file
    gtfindsrc['scfile'] = ft2Input
    gtfindsrc['outfile'] = notice.Name + '_findSrc.txt'
    gtfindsrc['rspfunc'] = 'DSS'
    gtfindsrc['use_lb'] = 'no'
    gtfindsrc['lon0'] = notice.RA
    gtfindsrc['lat0'] = notice.DEC
    gtfindsrc['optimizer'] = 'DRMNGB'
    gtfindsrc['chatter'] = 0
    gtfindsrc.run()
    results = open(gtfindsrc['outfile']).readlines()
    fields = results[-1].split()
    ra, dec, ts, pos_error = (float(fields[0]), float(fields[1]),
                              float(fields[2]), float(fields[3]))
    print ra, dec, ts, pos_error

    npix = 20
    mapsize = 4*pos_error
    gttsmap = GtApp('gttsmap')
    gttsmap['evfile'] = gtfindsrc['evfile']
    gttsmap['scfile'] = gtfindsrc['scfile']
    gttsmap['rspfunc'] = gtfindsrc['rspfunc']
    gttsmap['source_model_file'] = 'none'
    gttsmap['outfile'] = notice.Name + '_tsmap.fits'
    gttsmap['use_lb'] = 'no'
    gttsmap['ra_min'] = ra - mapsize
    gttsmap['ra_max'] = ra + mapsize
    gttsmap['dec_min'] = dec - mapsize
    gttsmap['dec_max'] = dec + mapsize
    gttsmap.run()

if __name__ == '__main__':
    refinePosition('../../Notices/GLG_NOTICE_080105885.TXT')
