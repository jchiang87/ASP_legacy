"""
@brief Make counts maps.

@author W. Focke <focke@slac.stanford.edu>
"""

import os

import BinnedAnalysis
from parfile_parser import Parfile

pars = Parfile(os.environ['PIPELINE_TASK'] + '.txt')

countMap = pars['count_map']
expCube = pars['expCube']
modelFile = pars['model_file']
fittedModel = 'fittedModel.xml'

obs = BinnedAnalysis.BinnedObs(countMap, expCube)
anal = BinnedAnalysis.BinnedAnalysis(obs, modelFile)
anal.fit()
anal.logLike.writeXml(fittedModel)

pars['fittedModel'] = fittedModel
pars.write()
