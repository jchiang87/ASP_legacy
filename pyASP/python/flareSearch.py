"""
@brief Find flaring sources by comparing countsmap with modelmap.

Currently incompatible with other steps because it ignores energy.

@author W. Focke <focke@slac.stanford.edu>
"""

import os

import numarray as num
import pyfits

from parfile_parser import Parfile
import cStat

cThreshhold = 2.0 # utterly bogus value


pars = Parfile(os.environ['PIPELINE_TASK'] + '.txt')
countMapFile = pars['count_map']
modelMapFile = pars['model_map']
raPars = eval(pars['ra_pars']) # should be a tuple of numbers ##security
decPars = eval(pars['dec_pars']) # should be a tuple of numbers ##security

counts = pyfits.open(countMapFile)[0].data
model = pyfits.open(modelMapFile)[0].data

# likelyhood for each pixel
cBins = cStat.deltaC(counts, model)

hotDec, hotRa = num.where((cBins > cThreshhold) & (counts > model))
hotVals = cBins[hotDec, hotRa]

# map from bin numbers to ra, dec
## need to write binCenters
## and
## write raPars, decPars to parfile during setup
hotRa = binCenters(hotRa, raPars)
hotDec = binCenters(hotDec, decPars)

# write out list of hotspots
## TBD
