"""
@brief Create HEALPix maps for a given set of FT1 and FT2 files.

@author J. Chiang <jchiang@slac.stanford.edu>
"""
#
# $Header$
#
import os, shutil
from GtApp import GtApp
from generateMaps import CountsArrayFactory, ExposureArrayFactory
from FitsNTuple import FitsNTuple

output_dir = os.environ['OUTPUTDIR']
shutil.copy('Ft1FileList', os.path.join(output_dir, 'Ft1FileList'))
shutil.copy('Ft2FileList', os.path.join(output_dir, 'Ft2FileList'))

os.chdir(output_dir)

ft1 = [x.strip() for x in open('Ft1FileList')]
ft2 = [x for x in open('Ft2FileList')]

#
# sort the FT2 files for merging and overwrite Ft2FileList
#
ft2.sort()
output = open('Ft2FileList', 'w')
for item in ft2:
    output.write(item)
output.close()

fmerge = GtApp('fmerge')
fmerge['infiles'] = '@Ft2FileList'
fmerge['outfile'] = 'FT2_merged.fits'
fmerge['clobber'] = 'yes'
fmerge['columns'] = '" "'
fmerge['mextname'] = '" "'
fmerge['lastkey'] = '" "'
fmerge.run()

scData = FitsNTuple(fmerge['outfile'])
tmin, tmax = min(scData.START), max(scData.STOP)

#
# use rather coarse binning: 4 x 12 = 48 skybins total
#
cmapFactory = CountsArrayFactory(ft1, nside=2)
emapFactory = ExposureArrayFactory(fmerge['outfile'], nside=2,
                                   irfs='P5_v0_transient')

cmap = cmapFactory.create(tmin, tmax)
cmap.write('cmap_%i_%i.fits' % (int(tmin), int(tmax)))

emap = emapFactory.create(tmin, tmax, "@Ft1FileList")
emap.write('emap_%i_%i.fits' % (int(tmin), int(tmax)))
