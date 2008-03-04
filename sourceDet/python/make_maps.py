"""
@brief Generate healpix array maps for counts and exposure using
the getL1Data interface to find the input files

@author J. Chiang <jchiang@slac.stanford.edu>
"""
#
# $Header$
#

from GtApp import GtApp

from AspHealPix import SkyDir, Healpix, CountsArray, ExposureArray
from getL1Data import getL1Data

gtlivetimecube = GtApp('gtlivetimecube')

startTime = 220838400.   # for DC2 data

days = range(20, 55)

hp = Healpix(16, Healpix.NESTED, SkyDir.GALACTIC)

for day in days:
    print 'processing day ', day

    tmin = startTime + 8.64e4*day
    tmax = tmin + 8.64e4
    ft1Files, ft2Files = getL1Data(tmin, tmax)
    
    gtlivetimecube['evfile'] = 'eventFiles'
    gtlivetimecube['scfile'] = ft2Files[0]
    gtlivetimecube['outfile'] = 'expCube_%03i.fits' % day
    eventFiles = open(gtlivetimecube['evfile'], 'w')
    for item in ft1Files:
        eventFiles.write(item + '\n')
    eventFiles.close()
    gtlivetimecube.run()
    
    cmap = CountsArray(hp)
    for item in ft1Files:
        cmap.binCounts(item, "ENERGY>=100")
    cmap.write('counts_%03i.fits' % day)

    emap = ExposureArray(hp)
    emap.computeExposure('DC2', gtlivetimecube['outfile'])
    emap.write('exposure_%03i.fits' % day)

    

    
