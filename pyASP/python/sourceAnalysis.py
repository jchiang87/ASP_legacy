"""
@brief Region-of-intereset source analysis for DRP monitoring.

@author J. Carson <carson@slac.stanford.edu>
@author J. Chiang <jchiang@slac.stanford.edu>
"""
#
# $Header$
#

from GtApp import GtApp
from drpRoiSetup import rootpath, pars, rois

debug = True

id = int(os.environ['ROI_ID'])
name, ra, dec, radius, sourcerad = rois[id]
os.chdir(name)

ft1file = name + '_events.fits'
srcModel = name + '_model.xml'

if debug:
    print "analyzing ", ft1file, srcModel
else:
    obs = UnbinnedObs(ft1file, pars['ft2file'], expMap=pars['expMap'],
                      expCube=pars['expCube'], irfs=pars['rspfunc'])
    like = UnbinnedAnalysis(obs, srcModel, 'Minuit')

    like.fit()

    outputModel = name + '_model_out.xml'
    like.writeXml(outputModel)

    os.system('chmod 666 *')
