"""
@brief Retrieve the FT1/2 data from the dataCatalog given a time-based 
query made by the PGWave task.
"""
#
# $Header$
#

import os, shutil
from GtApp import GtApp
from getFitsData import getStagedFitsData
from ft1merge import ft1merge, ft2merge
from FitsNTuple import FitsNTuple
from FileStager import FileStager

output_dir = os.environ['OUTPUTDIR']
process_id = os.environ['PIPELINE_PROCESSINSTANCE']
fileStager = FileStager(process_id, stageArea=output_dir)

ft1, ft2 = getStagedFitsData(fileStager=fileStager)

##
## kluge for Interleave55d FT2 file since it violates convention established
## by L1Proc for OktoberTest
##
#ft2 = ('/nfs/farm/g/glast/u44/MC-tasks/Interleave55d-GR-v11r17/prune/FT2_55day_patch.fits',)

os.chdir(output_dir)

start_time = float(os.environ['TSTART'])
stop_time = float(os.environ['TSTOP'])

gtselect = GtApp('gtselect')

print "Using downlink files: ", ft1

ft1Merged ='FT1_merged.fits'
ft1merge(ft1, ft1Merged)

ft2Merged = 'FT2_merged.fits'
ft2merge(ft2, ft2Merged)

gti = FitsNTuple(ft1Merged, 'GTI')

gtselect['infile'] = ft1Merged
gtselect['outfile'] ='time_filtered_events.fits'
gtselect['tmin'] = start_time
gtselect['tmax'] = stop_time
gtselect['ra'] = 180.
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
fcopy.run(infile='time_filtered_events.fits[EVENTS][CTBCLASSLEVEL>1]',
          outfile='Filtered.fits')

#
# apply zenith angle cut and energy cut
#
gtselect.run(emin=100, zmax=105, infile='Filtered.fits',
             outfile='Filtered_evt.fits')

os.system('chmod 777 *')
