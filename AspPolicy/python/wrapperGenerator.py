"""
@brief Generate bash wrapper scripts to set the environment for
running the ASP subpackage Python scripts.

@author J. Chiang <jchiang@slac.stanford.edu>
"""
#
# $Header$
#

import os
import string
import glob

def packageName():
    input, output = os.popen4('cmt show macro_value package')
    line = output.readlines()
    input.close()
    output.close()
    return line[0].strip()

_ST_path = "${ST_INST}"
_ASP_path = "${ASP_PATH}"
_bindir = os.environ['BINDIR']

_packageName = packageName()
_packageRoot = string.upper(_packageName) + 'ROOT'
_package_version = os.environ[_packageRoot].split(os.path.sep)[-1]
_package_root = os.path.join(_ASP_path, "ASP", _packageName, _package_version)

pipeline_config = lambda x : os.path.join("/afs/slac.stanford.edu/g/glast/ground/PipelineConfig", x)

_ftools_setup= pipeline_config("ASP/headas-config-noric024835.sh")
_asp_python_path = pipeline_config("ASP/python/lib/python2.5/site-packages")
_GPLtools_path = pipeline_config("GPLtools/prod/python")
_LoggerPath = "/afs/slac.stanford.edu/g/glast/isoc/flightOps/rhel4_gcc34/ISOC_PROD/lib/python2.5/site-packages/gov"
_asp_python = "/usr/bin/env python"
_asp_db_config = pipeline_config('ASP/db_config')

def wrapperGenerator(scriptName):
    prefix = scriptName.split(".py")[0]
    pyScript = os.path.join(_package_root, 'python', scriptName)
    outfile = os.path.join(os.environ[_packageRoot], _bindir, prefix + ".sh")
    output = open(outfile, "w")
    output.write("#!/usr/bin/env bash\n")
    output.write("CMTSITE=SLAC_UNIX; export CMTSITE\n")
    output.write("CMTVERSION=v1r16p20040701; export CMTVERSION\n")
    output.write("CMTBASE=/afs/slac.stanford.edu/g/glast/applications/CMT; export CMTBASE\n")
    output.write("CMTROOT=/afs/slac.stanford.edu/g/glast/applications/CMT/v1r16p20040701; export CMTROOT\n")
    output.write("CMTBIN=Linux; export CMTBIN\n")
    output.write("CMTCONFIG=%s; export CMTCONFIG\n" % _bindir)
    output.write("CMTPATH=%s; export CMTPATH\n" %
                 os.pathsep.join((_ST_path, _ASP_path)))
    output.write("source %s\n" % _ftools_setup)
    output.write("GLAST_EXT=/afs/slac.stanford.edu/g/glast/ground/GLAST_EXT/%s; export GLAST_EXT\n" % _bindir)
    output.write("PATH=%s:${PATH}; export PATH\n" % os.path.join(_ST_path, 'bin'))
    output.write("source %s\n" % os.path.join(_package_root, 'cmt','setup.sh'))
    output.write("export ORACLE_HOME=/usr/oracle\n")
    output.write("export LD_LIBRARY_PATH=${ORACLE_HOME}/lib:${LD_LIBRARY_PATH}:%s\n" % pipeline_config('ASP/lib'))
    output.write("export ASP_DB_CONFIG=%s\n" % _asp_db_config)
    output.write("export PYTHONPATH=%s:%s:${PYTHONPATH}:%s\n" 
                 % (_asp_python_path, _GPLtools_path, _LoggerPath))
    output.write('exec %s %s\n' % (_asp_python, pyScript))
    output.close()
    os.system('chmod +x %s' % outfile)

if __name__ == '__main__':
    import sys
    try:
        sys.argv[1:].index('-h')
        print "usage: %s [<Python script name>]" % sys.argv[0]
        sys.exit(1)
    except ValueError:
        if sys.argv[1:]:
            wrapperGenerator(sys.argv[1])
        else:
            scripts = glob.glob('../python/*.py')
            for item in scripts:
                script = os.path.basename(item)
                wrapperGenerator(script)
