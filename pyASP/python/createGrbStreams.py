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

def streamNumber():
    return "%i%02i%02i%02i%02i" % time.localtime()[1:6]

class PipelineError(EnvironmentError):
    "Pipeline stream creation failed"

def refinementStreams(notices=None):
    os.chdir(os.environ['OUTPUTDIR'])
    if notices is None:
        notices = glob.glob('GRB*_Notice.txt')
    if isinstance(notices, str):
        notices = (notices, )

    for notice in notices:
        args = (','.join(("GBM_Notice=%s",
                          "output_dir=%s",
                          "PYASPROOT=%s"))
                % (notice, os.environ['OUTPUTDIR'],
                   '/nfs/farm/g/glast/u33/jchiang/ASP/pyASP/v0r1'))
        command = ('~glast/pipeline-II/pipeline createStream %s %s "%s"'
                   % ('GBM_refinement', streamNumber(), args))
        print command
        rc = os.system(command)
        if rc != 0:
            raise PipelineError
        time.sleep(1)

def afterglowStreams(parfiles=None):
    os.chdir(os.environ['OUTPUTDIR'])
    if parfiles is None:
        parfiles = glob.glob('GRB*_pars.txt')
    if isinstance(parfiles, str):
        parfiles = (parfiles, )

    for parfile in parfiles:
        args = (','.join(("output_dir=%s",
                          "GRB_parfile=%s",
                          "PYASPROOT=%s"))
                % (os.environ['OUTPUTDIR'], parfile,
                   '/nfs/farm/g/glast/u33/jchiang/ASP/pyASP/v0r1'))
        command = ('~glast/pipeline-II/pipeline createStream %s %s "%s"'
                   % ('GRB_afterglow', streamNumber(), args))
        print command
        rc = os.system(command)
        print "pipeline return code: ", rc
        if rc != 0:
            raise PipelineError
        time.sleep(1)
