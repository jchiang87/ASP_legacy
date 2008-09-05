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

def resolve_nfs_path(path):
    tokens = path.split(":")
    for i in range(len(tokens)):
        if tokens[i].find('g.glast.'):
            tokens[i] = os.path.join('/nfs/farm/g/glast', 
                                     tokens[i].split('g.glast.')[-1])
    return ":".join(tokens)

_ST_path = resolve_nfs_path(os.environ['ST_INST'])

_bindir = os.environ['BINDIR']
_glast_ext_root = "/afs/slac.stanford.edu/g/glast/ground/GLAST_EXT"

_cmt_version = "v1r18p20061003"
_cmt_base = "/afs/slac.stanford.edu/g/glast/applications/CMT"
_cmt_path = resolve_nfs_path(os.environ['CMTPATH'])

_packageName = packageName()
_packageRoot = string.upper(_packageName) + 'ROOT'
_package_version = os.environ[_packageRoot].split(os.path.sep)[-1]
_package_root = resolve_nfs_path(os.environ[_packageRoot])

pipeline_config = lambda x : os.path.join("/afs/slac.stanford.edu/g/glast/ground/PipelineConfig", x)

_ftools_setup = pipeline_config("ASP/headas-config-noric024835.sh")
_asp_python_path = pipeline_config("ASP/python/lib/python2.5/site-packages")
_GPLtools_path = pipeline_config("GPLtools/asp/python")
_asp_python = "/usr/bin/env python"
_asp_db_config = pipeline_config('ASP/db_config')

def wrapperGenerator(scriptName):
    prefix = scriptName.split(".py")[0]
    pyScript = os.path.join(_package_root, 'python', scriptName)
    outfile = os.path.join(os.environ[_packageRoot], _bindir, prefix + ".sh")
    output = open(outfile, "w")
    output.write("#!/usr/bin/env bash\n")
    output.write("export CMTVERSION=%s\n" % _cmt_version)
    output.write("export CMTBASE=%s\n" % _cmt_base)
    output.write("export CMTROOT=${CMTBASE}/${CMTVERSION}\n")
    output.write("export CMTBIN=Linux\n")
    output.write("export CMTCONFIG=%s\n" % _bindir)
    output.write("export CMTPATH=%s\n" % _cmt_path)
    output.write('export PFILES=".;"\n')
    output.write("source %s\n" % _ftools_setup)
    output.write("export GLAST_EXT=%s/%s\n" % (_glast_ext_root, _bindir))
    output.write("export PATH=%s:${PATH}\n" % os.path.join(_ST_path, 'bin'))
    output.write("source %s\n" % os.path.join(_package_root, 'cmt','setup.sh'))
    output.write("export TNS_ADMIN=/u/gl/glast/oracle/admin\n")
    output.write("export ORACLE_HOME=/afs/slac/package/oracle/d/linux/11.1.0\n")
    output.write("export LD_LIBRARY_PATH=${ORACLE_HOME}/lib:${LD_LIBRARY_PATH}:%s\n" % pipeline_config('ASP/lib'))
    output.write("export ASP_DB_CONFIG=%s\n" % _asp_db_config)
    output.write("export PYTHONPATH=%s:%s:${PYTHONPATH}\n" 
                 % (_asp_python_path, _GPLtools_path))
    output.write('exec %s %s "$@"\n' % (_asp_python, pyScript))
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
