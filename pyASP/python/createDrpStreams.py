"""
@brief Create streams for DRP monitoring task.

@author J. Chiang
"""
#
# $Header$
#

import os
from PipelineCommand import PipelineCommand, _outputDir

# import this to ensure it is available for the various streams
import pyASP

#_startTime = 220838400.   # for DC2 data
_startTime = 0.            # for testdata

def drpStreams(daynum=1, output_dir=_outputDir, RoI_file='rois.txt',
               startTime=_startTime, debug=False):
    start_time = (daynum-1)*8.64e4 + startTime
    stop_time = start_time + 8.64e4
    os.chdir(output_dir)
    args = {'output_dir' : output_dir,
            'start_time' : start_time,
            'stop_time' : stop_time,
            'RoI_file' : RoI_file}
    command = PipelineCommand('DRP_monitoring', args)
    command.run(debug=debug)

if __name__ == '__main__':
    drpStreams(debug=True)
