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
from drpRoiSetup import rootpath, pars, rois

debug = False

id = int(os.environ['ROI_ID']) - 1
name = rois[id].name
os.chdir(name)

ft1file = name + '_events.fits'
srcModel = name + '_model.xml'

if debug:
    print "analyzing ", ft1file, srcModel
else:
    irfs = pars['rspfunc']
    if irfs == 'DSS':
        irfs = 'DC2'
    obs = UnbinnedObs(ft1file, pars['ft2file'], expMap=pars['expMap'],
                      expCube=rootpath(pars['expCube']), irfs=irfs)
    like = UnbinnedAnalysis(obs, srcModel, 'Minuit')

    like.fit()

    outputModel = name + '_model_out.xml'
    like.writeXml(outputModel)

    os.system('chmod 666 *')
