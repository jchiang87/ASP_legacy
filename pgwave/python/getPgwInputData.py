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

#
# Perform CTBCLASSLEVEL cut when it is available.  @todo implement to
# use ft1_filter string from SourceMonitoringConfig table
#
foo = FitsNTuple('time_filtered_events.fits', 'EVENTS')
if 'CTBCLASSLEVEL' in foo.names:
    fcopy = GtApp('fcopy')
    fcopy.run(infile='time_filtered_events.fits[EVENTS][CTBCLASSLEVEL>1]',
              outfile='Filtered.fits')
else:
    os.system('ln -s time_filtered_events.fits Filtered.fits')

#
# apply zenith angle cut and energy cut
#
gtselect.run(emin=100, zmax=105, infile='Filtered.fits',
             outfile='Filtered_evt.fits')

start_time = int(os.environ['TSTART'])
stop_time = int(os.environ['TSTOP'])
#
# Insert the current interval into the TIMEINTERVALS table.
#
inum = int(os.environ['interval'])
frequency = os.environ['frequency']
sql = ("insert into TIMEINTERVALS " +
       "(INTERVAL_NUMBER, FREQUENCY, TSTART, TSTOP) values " +
       "(%i, '%s', %i, %i)" % (inum, frequency, start_time, stop_time))

import databaseAccess as dbAccess
try:
    dbAccess.apply(sql)
except dbAccess.cx_Oracle.IntegrityError, message:
    #
    # Check to see if this interval is already in the table. If so,
    # proceed anyways.  This is useful for rollbacks.
    #
    sql = ("select tstart, tstop from TIMEINTERVALS where " +
           "INTERVAL_NUMBER=%i and FREQUENCY='%s'" % (inum, frequency))
    def getTlims(cursor):
        for entry in cursor:
            return entry[0], entry[1]
    tlims = dbAccess.apply(sql, getTlims)
    if tlims[0] != start_time or tlims[1] != stop_time:
        raise dbAccess.cx_Oracle.IntegrityError, message 

os.system('chmod 777 *')
