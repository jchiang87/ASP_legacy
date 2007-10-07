import os, shutil
from GtApp import GtApp
#from getL1Data import getL1Data
from getFitsData import getFitsData
from ft1merge import ft1merge

debug = False

ft1, ft2 = getFitsData()

output_dir = os.environ['OUTPUTDIR']
os.chdir(output_dir)

start_time = float(os.environ['TSTART'])
stop_time = float(os.environ['TSTOP'])

gtselect = GtApp('gtselect')

print "Using downlink files: ", ft1

ft1Merged ='FT1_merged.fits'
ft1merge(ft1, ft1Merged)

fmerge = GtApp('fmerge')
fmerge['infiles'] = '@Ft2FileList'
fmerge['outfile'] = 'FT2_merged.fits'
fmerge['clobber'] = 'yes'
fmerge['columns'] = '" "'
fmerge['mextname'] = '" "'
fmerge['lastkey'] = '" "'
fmerge.run()

gtselect['infile'] = ft1Merged
gtselect['outfile'] ='time_filtered_events.fits'
gtselect['tmin'] = start_time
gtselect['tmax'] = stop_time
gtselect['ra'] =180.
gtselect['dec'] = 0.
gtselect['rad'] = 180
gtselect['emin'] = 30
gtselect['emax'] = 2e5
gtselect['eventClass'] = -1

if debug:
    print gtselect.command()
else:
    gtselect.run()
os.system('chmod 777 *')
