"""
@brief Retrieve RoI-specific data.

@author J. Carson <carson@slac.stanford.edu>
@author J. Chiang <jchiang@slac.stanford.edu>
"""
#
# $Header$
#

import os
from GtApp import GtApp
import readXml
import xmlSrcLib
from combineExpMaps import writeExpMapBounds
from search_Srcs import search_Srcs
from parfile_parser import Parfile

from drpRoiSetup import rootpath, pars, rois

debug = False

id = int(os.environ['ROI_ID']) - 1   # This env var is set in DRP_monitoring.xml
name = rois[id].name
ra = rois[id].ra
dec = rois[id].dec
radius = rois[id].radius
sourcerad = rois[id].sourcerad
    
# Create the region subdirectory and cd to it.

try:
    os.mkdir(name)
except OSError:
    pass
os.system('chmod 777 %s' % name)
os.chdir(name)

# Extract events for this region.

gtselect = GtApp('gtselect')
gtselect['infile'] = rootpath(pars['ft1file'])
gtselect['outfile'] = name + '_events.fits'
gtselect['ra'] = ra
gtselect['dec'] = dec
gtselect['rad'] = radius
if debug:
    print gtselect.command()
else:
    gtselect.run()

# Build the source model xml file based on a 10 degree radius region.
# (Revisit this choice of radius).

# sourceModel needs to be generalized to include sources other than just
# the DRP sources.
sourceModel = os.path.join(os.environ['PYASPROOT'], 'data', 'source_model.xml')
modelRequest = 'dist((RA,DEC),(%f,%f))<10.' % (ra, dec)
outputModel = name + '_ptsrcs_model.xml'
model = search_Srcs(sourceModel, modelRequest, outputModel)

srcModel = readXml.SourceModel(outputModel)
GalProp = readXml.Source(xmlSrcLib.GalProp())
EGDiffuse = readXml.Source(xmlSrcLib.EGDiffuse())
srcModel['Galactic Diffuse'] = GalProp
srcModel['Galactic Diffuse'].name = 'Galactic Diffuse'
srcModel['Galactic Diffuse'].spectrum.Value.free = 0
srcModel['Extragalactic Diffuse'] = EGDiffuse
srcModel['Extragalactic Diffuse'].spectrum.Prefactor.free = 1
srcModel.filename = name + '_model.xml'
srcModel.writeTo()

# Write gtexpmap.par file for subsequent exposureMap.py calculations.

gtexpmap = GtApp('gtexpmap')
gtexpmap['evfile'] = gtselect['outfile']
gtexpmap['scfile'] = pars['ft2file']
gtexpmap['exposure_cube_file'] = rootpath(pars['expCube'])
gtexpmap['outfile'] = 'expMap_' + name + '.fits'
gtexpmap['source_region_radius'] = sourcerad
gtexpmap['rspfunc'] = 'DSS'
gtexpmap.pars.write('gtexpmap.par')

writeExpMapBounds(gtexpmap)

os.system('chmod 666 *')
