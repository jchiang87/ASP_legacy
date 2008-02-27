"""
@file launchStreams.py

@brief For each downlink emitted by L1Proc, check for the availability
of L1 data for the next scheduled instance of each task and launch
each one if the required data are available.

@author J. Chiang <jchiang@slac.stanford.edu>
"""
#
# $Header$
#
import os
from checkLevelOneFiles import providesCoverage
from PipelineCommand import PipelineCommand, _asp_path
from createGrbStreams import blindSearchStreams
from FileStager import FileStager

_version = os.path.split(os.environ['DRPMONITORINGROOT'])[-1]
_drpRoot = os.path.join(_asp_path, 'ASP', 'drpMonitoring', _version)

def launch_drp(interval, frequency, tstart, tstop, folder, output_dir,
               num_RoIs=30, debug=False):
    os.chdir(output_dir)
    args = {'OUTPUTDIR' : output_dir,
            'logicalPath' : folder,
            'interval' : interval,
            'frequency' : frequency, 
            'TSTART' : tstart,
            'TSTOP' : tstop,
            'num_RoIs' : num_RoIs,
            'DRPMONITORINGROOT' : _drpRoot}
    command = PipelineCommand('DRP_monitoring', args)
    command.run(debug=debug)

_version = os.path.split(os.environ['PGWAVEROOT'])[-1]
_pgwaveRoot = os.path.join(_asp_path, 'ASP', 'pgwave', _version)

def launch_pgwave(interval, tstart, tstop, folder, output_dir, debug=False):
    args = {'logicalPath' : folder,
            'TSTART' : tstart,
            'TSTOP' : tstop,
            'OUTPUTDIR' : output_dir,
            'CATDIR' : '/nfs/farm/g/glast/u33/tosti/october/catdir',
            'PGWAVEROOT' : _pgwaveRoot}
    command = PipelineCommand('PGWave', args)
    command.run(debug=debug)

def get_interval(freq):
    """Read the environment variables set by the AspLauncher task
    for each frequency of source monitoring to get the start and
    stop times and interval number.
    """
    return (int(os.environ[freq + '_interval']), 
            int(os.environ[freq + '_nMetStart']), 
            int(os.environ[freq + '_nMetStop']))

def createSubDir(interval, frequency, root_output_dir):
    subdir = "%05i" % interval
    os.chdir(root_output_dir)
    newdir = os.path.join(root_output_dir, frequency)
    if not os.path.isdir(newdir):
        os.mkdir(newdir)
        os.system('chmod o+w %s ' % newdir)
    newdir = os.path.join(root_output_dir, frequency, subdir)
    if not os.path.isdir(newdir):
        os.mkdir(newdir)
        os.system('chmod o+w %s ' % newdir)
    return newdir    

if __name__ == '__main__':
    folder = os.environ['folder']
    currentDir = os.getcwd()
    min_frac = float(os.environ['minimum_coverage'])
    process_id = os.environ['PIPELINE_PROCESSINSTANCE']

## Use the following for debugging in an accessible local directory.
#    fileStager = FileStager(os.path.join(currentDir,'AspLauncher',process_id),
#                            cleanup=True)
    #
    # Stage to local /scratch area and clean up on exit
    #
    fileStager = FileStager(os.path.join('AspLauncher', process_id),
                            cleanup=True)

    debug = False

    nDownlink = int(os.environ['nDownlink'])
    blindSearchStreams(downlinks=(nDownlink,), logicalPath=folder,
                       grbroot_dir=os.environ['GRBOUTPUTDIR'], debug=debug)

    os.chdir(currentDir)
    interval, tstart, tstop = get_interval('SixHour')
    if providesCoverage(tstart, tstop, min_frac, 
                        'Ft1FileList_6hr', 'Ft2FileList_6hr', 
                        fileStager=fileStager):
        output_dir = createSubDir(interval, 'SixHour',
                                  os.environ['PGWAVEOUTPUTDIR'])
        launch_pgwave(interval, tstart, tstop, folder, output_dir, debug=debug)

    os.chdir(currentDir)
    interval, tstart, tstop = get_interval('Daily')
    if providesCoverage(tstart, tstop, min_frac, 
                        'Ft1FileList_day', 'Ft2FileList_day', 
                        fileStager=fileStager):
        output_dir = createSubDir(interval, 'Daily',
                                  os.environ['DRPOUTPUTDIR'])
        launch_drp(interval, 'daily', tstart, tstop, folder, 
                   output_dir, debug=debug)

    os.chdir(currentDir)
    interval, tstart, tstop = get_interval('Weekly')
    if providesCoverage(tstart, tstop, min_frac, 
                        'Ft1FileList_week', 'Ft2FileList_week', 
                        fileStager=fileStager):
        output_dir = createSubDir(interval, 'Weekly',
                                  os.environ['DRPOUTPUTDIR'])
        launch_drp(interval, 'weekly', tstart, tstop, folder, 
                   output_dir, debug=debug)
