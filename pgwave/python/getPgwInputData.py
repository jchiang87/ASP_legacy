import os, shutil
from GtApp import GtApp
#from getL1Data import getL1Data
from getFitsData import getFitsData
from ft1merge import ft1merge
from FitsNTuple import FitsNTuple

ft1, ft2 = getFitsData()

#
# kluge for Interleave55d FT2 file since it violates convention established
# by L1Proc for OktoberTest
#
ft2 = ('/nfs/farm/g/glast/u44/MC-tasks/Interleave55d-GR-v11r17/prune/FT2_55day_patch.fits',)

output_dir = os.environ['OUTPUTDIR']
os.chdir(output_dir)

#start_time = float(os.environ['TSTART'])
#stop_time = float(os.environ['TSTOP'])

gtselect = GtApp('gtselect')

print "Using downlink files: ", ft1

ft1Merged ='FT1_merged.fits'
ft1merge(ft1, ft1Merged)

"""fmerge = GtApp('fmerge')
fmerge['infiles'] = '@Ft2FileList'
fmerge['outfile'] = 'FT2_merged.fits'
fmerge['clobber'] = 'yes'
fmerge['columns'] = '" "'
fmerge['mextname'] = '" "'
fmerge['lastkey'] = '" "'
fmerge.run()"""

gtselect['infile'] = ft1Merged
gtselect['outfile'] ='time_filtered_events.fits'
#gtselect['tmin'] = 0
#gtselect['tmax'] = 0
gti = FitsNTuple(ft1Merged, 'GTI')
gtselect['tmin'] = min(gti.START)
gtselect['tmax'] = max(gti.STOP)
gtselect['ra'] =180.
gtselect['dec'] = 0.
gtselect['rad'] = 180
gtselect['emin'] = 30
gtselect['emax'] = 2e5
gtselect['eventClass'] = -1
gtselect.run()

try:
    os.remove('Filtered.fits')
except OSError:
    pass

fcopy = GtApp('fcopy')
fcopy.run(infile='"time_filtered_events.fits[EVENTS][CTBCLASSLEVEL>1]"',
          outfile='Filtered.fits')

os.system('chmod 777 *')
