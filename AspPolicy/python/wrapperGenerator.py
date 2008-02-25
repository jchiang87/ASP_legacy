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

_packageName = packageName()
_packageRoot = string.upper(_packageName) + 'ROOT'

_ftools_setup= "/afs/slac/g/glast/ground/PipelineConfig/ASP/headas-config-noric024835.sh"
_ST_path = "${ST_INST}"
_ASP_path = "${ASP_PATH}"
_asp_python_path = "/afs/slac/g/glast/ground/PipelineConfig/ASP/python/lib/python2.5/site-packages"
_GPLtools_path = "/afs/slac/g/glast/ground/PipelineConfig/GPLtools/L1prod/python"
_LoggerPath = "/afs/slac.stanford.edu/g/glast/isoc/flightOps/rhel4_gcc34/ISOC_PROD/lib/python2.5/site-packages/gov"
_asp_python = "/usr/bin/env python"
_package_version = os.environ[_packageRoot].split(os.path.sep)[-1]
_package_root = os.path.join(_ASP_path, "ASP", _packageName, _package_version)

def wrapperGenerator(scriptName):
    prefix = scriptName.split(".py")[0]
#    pyScript = os.path.abspath(scriptName)
    pyScript = os.path.join(_package_root, 'python', scriptName)
    outfile = os.path.join(os.environ[_packageRoot], os.environ['BINDIR'],
                           prefix + ".sh")
    output = open(outfile, "w")
    output.write("#!/usr/bin/env bash\n")
    output.write("CMTSITE=SLAC_UNIX; export CMTSITE\n")
    output.write("CMTVERSION=v1r16p20040701; export CMTVERSION\n")
    output.write("CMTBASE=/afs/slac.stanford.edu/g/glast/applications/CMT; export CMTBASE\n")
    output.write("CMTROOT=/afs/slac.stanford.edu/g/glast/applications/CMT/v1r16p20040701; export CMTROOT\n")
    output.write("CMTBIN=Linux; export CMTBIN\n")
    output.write("CMTCONFIG=rh9_gcc32; export CMTCONFIG\n")
    output.write("CMTPATH=%s; export CMTPATH\n" %
                 os.pathsep.join((_ST_path, _ASP_path)))
    output.write("source %s\n" % _ftools_setup)
    output.write("GLAST_EXT=/afs/slac/g/glast/ground/GLAST_EXT/rh9_gcc32; export GLAST_EXT\n")
    output.write("PATH=%s:${PATH}; export PATH\n" % os.path.join(_ST_path, 'bin'))
    output.write("source %s\n" % os.path.join(_package_root, 'cmt','setup.sh'))
    output.write("export ORACLE_HOME=/usr/oracle\n")
    output.write("export LD_LIBRARY_PATH=${ORACLE_HOME}/lib:${LD_LIBRARY_PATH}:/afs/slac/g/glast/ground/PipelineConfig/ASP/lib\n")
    output.write("PYTHONPATH=%s:%s:${PYTHONPATH}:%s; export PYTHONPATH\n" 
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
