"""
@brief Create streams for various top level GRB tasks.

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
import pyIrfLoader
import BayesBlocks

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

def blindSearchStreams(downlinks=None, grbroot_dir=None,
                       output_dir=_outputDir):
    os.chdir(output_dir)
    if downlinks is None:
        raise ValueError, "No downlink files specified"
    if grbroot_dir is None:
        grbroot_dir = os.path.abspath(os.environ['GRBROOTDIR'])
    if isinstance(downlinks, str):
        downlinks = (downlinks, )
    for downlink in downlinks:
        args = argString({'Downlink_file': downlink,
                          'GRBROOTDIR' : grbroot_dir})
        command = pipelineCommand('GRB_blind_search', args)
        print command
        rc = _runCommand(command)
        if rc != 0:
            raise PipelineError, ("pipeline return code: %i" % rc)

def refinementStreams(notices=None, output_dir=_outputDir):
    os.chdir(output_dir)
    if notices is None:
        notices = glob.glob('GRB*_Notice.txt')
    if isinstance(notices, str):
        notices = (notices, )
    for notice in notices:
        args = argString({'GBM_Notice' : notice,
                          'output_dir' : output_dir})
        command = pipelineCommand('GRB_refinement', args)
        print command
        rc = _runCommand(command)
        if rc != 0:
            raise PipelineError, ("pipeline return code: %i" % rc)

def afterglowStreams(parfiles=None, output_dir=_outputDir):
    os.chdir(output_dir)
    if parfiles is None:
        parfiles = glob.glob('GRB*_pars.txt')
    if isinstance(parfiles, str):
        parfiles = (parfiles, )
    for parfile in parfiles:
        args = argString({'GRB_parfile' : parfile,
                          'output_dir' : output_dir})
        command = pipelineCommand('GRB_afterglow', args)
        print command
        rc = _runCommand(command)
        if rc != 0:
            raise PipelineError, ("pipeline return code: %i" % rc)

if __name__ == '__main__':
    pass
#    blindSearchStreams('foo')
#    refinementStreams('bar')
#    afterglowStreams('foobar')
