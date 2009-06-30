"""
@file launchDrpMonitoring.py

@brief Launch the corresponding DRP_monitoring task for the current 
time interval.

@author J. Chiang <jchiang@slac.stanford.edu>
"""
#
# $Header$
#
import os
from PipelineCommand import PipelineCommand, _asp_path

_version = os.path.split(os.environ['DRPMONITORINGROOT'])[-1]
_drpRoot = os.path.join(_asp_path, 'ASP', 'drpMonitoring', _version)

def launch_drp(interval, frequency, tstart, tstop, folder, output_dir,
               pgwave_processId, num_RoIs=30, debug=False):
    args = {'OUTPUTDIR' : output_dir,
            'logicalPath' : folder,
            'interval' : interval,
            'frequency' : frequency,
            'TSTART' : tstart,
            'TSTOP' : tstop,
            'pgwave_processId' : pgwave_processId,
            'num_RoIs' : num_RoIs,
            'DRPMONITORINGROOT' : _drpRoot}
    command = PipelineCommand('DRP_monitoring', args)
    command.run(debug=debug)

if __name__ == '__main__':
    foo = os.environ['OUTPUTDIR']
    indx = foo.rfind('PGWAVE')
    part1 = foo[0:indx]
    part2 = foo[indx+6:]
    output_dir = 'DRP'.join((part1, part2))

    interval = int(os.environ['interval'])
    frequency = os.environ['frequency']
    logicalPath = os.environ['logicalPath']
    tstart = int(os.environ['TSTART'])
    tstop = int(os.environ['TSTOP'])

    processId = int(os.environ['pgwave_processId'])

    launch_drp(interval, frequency, tstart, tstop, logicalPath,
               output_dir, processId, debug=False)

