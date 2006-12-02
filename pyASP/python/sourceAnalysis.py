"""
@brief Region-of-intereset source analysis for DRP monitoring.

@author J. Carson <carson@slac.stanford.edu>
@author J. Chiang <jchiang@slac.stanford.edu>
"""
#
# $Header$
#

import os
from GtApp import GtApp
from UnbinnedAnalysis import *
from drpRoiSetup import rootpath, pars, rois, output_dir

debug = False

id = int(os.environ['ROI_ID']) - 1
name = rois[id].name
os.chdir(name)

ft1file = name + '_events.fits'
srcModel = name + '_model.xml'

if debug:
    print "analyzing ", ft1file, srcModel
else:
#
# run gtdiffresp locally for each region until the full sky
# diffuseResponses process is parallelized
#
    gtdiffresp = GtApp('gtdiffresp')
    gtdiffresp['evfile'] = ft1file
    gtdiffresp['scfile'] = pars['ft2file']
    gtdiffresp['rspfunc'] = pars['rspfunc']
    gtdiffresp['source_model_file'] = rootpath('diffuse_model.xml')
    gtdiffresp.run()

    irfs = pars['rspfunc']
    if irfs == 'DSS':
        irfs = 'DC2'
    obs = UnbinnedObs(ft1file, pars['ft2file'], expMap=pars['expMap'],
                      expCube=rootpath(pars['expCube']), irfs=irfs)
    like = UnbinnedAnalysis(obs, srcModel, 'Minuit')

    try:
        like.fit()
    except RuntimeError:
        like.fit()

    for srcname in like.model.srcNames:
        src = like.model[srcname]
        print src.src.getType()
        if src.src.getType() != 'Diffuse':
            spec = src.funcs['Spectrum']
            integral = spec.getParam('Integral')
            index = spec.getParam('Index')
            output = open(os.path.join(output_dir, '..', srcname+'.txt'), 'a')
            output.write('%i  %i  %e  %e  %e  %e\n' %
                         (pars['start_time'], pars['stop_time'],
                          integral.getTrueValue(),
                          integral.error()*integral.getScale(),
                          spec.getParam('Index').value(),
                          spec.getParam('Index').error()))
            output.close()

    outputModel = name + '_model_out.xml'
    like.writeXml(outputModel)

    os.system('chmod 666 *')
