"""
@brief Create streams for various DRP monitoring tasks

@author J. Chiang
"""
#
# $Header$
#

import os
import glob
import time

# import these to ensure they are available for the various streams
import pyASP

def pyASProot():
    version = os.environ['PYASPROOT'].split(os.path.sep)[-1]
    return os.path.join('/nfs/farm/g/glast/u33/jchiang/ASP/pyASP', version)

_pyASProot = pyASProot()
_outputDir = os.environ['OUTPUTDIR']
_bindir = os.environ['BINDIR']

print "Using:\n\nPYASPROOT = %s\nOUTPUTDIR = %s" % (_pyASProot, _outputDir)
print "BINDIR = %s\n" % _bindir

_runCommand = os.system
#_runCommand = lambda x : 0

def argString(argDict):
    """Construct the argument stream for a pipeline task.  Entries in
    the default dictionary can be over-ridden by key-value pairs in
    the argDict.
    """
    defaultDict = {'output_dir' : _outputDir,
                   'PYASPROOT' : _pyASProot,
                   'BINDIR' : _bindir}
    defaultDict.update(argDict)
    arg_string = ""
    for item in defaultDict:
        arg_string += '%s=%s,' % (item, defaultDict[item])
    return arg_string.strip(',')

def streamNumber():
    """Provide a unique stream number for the pipeline based on the
    current date and time.
    """
    time.sleep(1)     # to ensure unique stream numbers
    return "%i%02i%02i%02i%02i" % time.localtime()[1:6]

def pipelineCommand(taskname, args, stream=None):
    "Construct the pipeline II command line submission string."
    command = '~glast/pipeline-II/pipeline createStream %s %s "%s"'
    if stream is None:
        stream = streamNumber()
    return command % (taskname, stream, args)

class PipelineError(EnvironmentError):
    "Pipeline stream creation failed"

def drpStreams(daynum=1, root_output_dir='/nfs/farm/g/glast/u33/jchiang/ASP/output/DRP_monitoring', RoI_file='rois.txt'):
    _startTime = 220838400.
    start_time = (daynum-1)* 8.64e4 + _startTime
    stop_time = start_time + 8.64e4
    os.chdir(root_output_dir)
    args = argString({'root_output_dir' : root_output_dir,
                      'start_time' : start_time,
                      'stop_time' : stop_time,
                      'RoI_file' : RoI_file})
    command = pipelineCommand('DRP_monitoring', args)
    print command
    rc = _runCommand(command)
    if rc != 0:
        raise PipelineError, ("pipeline return code: %i" % rc)

