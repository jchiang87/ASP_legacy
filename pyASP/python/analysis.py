"""

@brief Perform likelihood analysis on a list of regions of
interest containing the "sources of interest" from the data release
plan.

@author J. Carson <carson@slac.stanford.edu>
"""
#
# $Header$
#

import sys
sys.path.insert(0,'.')
from GtApp import GtApp
from UnbinnedAnalysis import *
from read_data import read_data
from search_Srcs import search_Srcs
from parfile_parser import parfile_parser
import numarray as num
import readXml
import xmlSrcLib
import FuncFactory
import os

gtselect = GtApp('gtselect')
gtdiffresp = GtApp('gtdiffresp')
gtlivetimecube = GtApp('gtlivetimecube')
gtexpmap = GtApp('gtexpmap')
gtdiffresp = GtApp('gtdiffresp')

_LatFt1File = '/nfs/farm/g/glast/u33/jchiang/ASP/testdata/all_events.fits'
_LatFt2File = '/nfs/farm/g/glast/u33/jchiang/ASP/testdata/eg_diffuse_scData_0000.fits'
_SourceModel = '/nfs/farm/g/glast/u33/carson/asp/drp_srcs/source_model.xml'
_RoIfile = '/nfs/farm/g/glast/u33/carson/asp/drp_srcs/rois.txt'
_SourcePars = '/nfs/farm/g/glast/u33/carson/asp/drp_srcs/source_pars.txt'

def getTimeData(tstart, tstop, ft1File, ft2File):

    gtselect['infile'] = ft1File
    gtselect['outfile'] = 'time-filtered_events.fits'
    gtselect['tmin'] = tstart
    gtselect['tmax'] = tstop
    gtselect['rad'] = 180
    gtselect.run()

    return gtselect['outfile'], ft2File


def DiffuseResponse(ft1TimeFile, ft2File, respfunc):
    
    srcModel = readXml.SourceModel()
    GalProp = readXml.Source(xmlSrcLib.GalProp())
    EGDiffuse = readXml.Source(xmlSrcLib.EGDiffuse())
    srcModel['Galactic Diffuse'] = GalProp
    srcModel['Galactic Diffuse'].name = 'Galactic Diffuse'
    srcModel['Galactic Diffuse'].spectrum.Value.free = 1
    srcModel['Extragalactic Diffuse'] = EGDiffuse
    srcModel['Extragalactic Diffuse'].spectrum.Prefactor.free = 1
    srcModel.filename = 'diffuse_model.xml'
    srcModel.writeTo()

    gtdiffresp['evfile'] = ft1TimeFile
    gtdiffresp['scfile'] = ft2File
    gtdiffresp['rspfunc'] = respfunc
    gtdiffresp['source_model_file'] = srcModel.filename
    gtdiffresp.run()

    return gtdiffresp['evfile']


def ExposureCube(ft1TimeFile, ft2File):

    gtlivetimecube['evfile'] = ft1TimeFile
    gtlivetimecube['scfile'] = ft2File
    gtlivetimecube['outfile'] = 'expCube.fits'
    gtlivetimecube.run()

    return gtlivetimecube['outfile']


def sourceData(ft1TimeFile, roirad, line, sourceModel):

    name, ra, dec = GetRoI(_RoIfile, line)
    os.system('mkdir %s' % name)
    os.chdir(name)
    gtselect['infile'] = os.environ['ROOTDIR'] + ft1TimeFile
    gtselect['outfile'] = name + '_events.fits'
    gtselect['ra'] = ra
    gtselect['dec'] = dec
    gtselect['rad'] = roirad
    gtselect.run()

    modelRequest = 'dist((RA,DEC),(%f,%f))<10.' % (ra, dec)
    outputModel = name + '_ptsrcs_model.xml'
    model = search_Srcs(sourceModel, modelRequest, outputModel)

    srcModel = readXml.SourceModel(outputModel)
    GalProp = readXml.Source(xmlSrcLib.GalProp())
    EGDiffuse = readXml.Source(xmlSrcLib.EGDiffuse())
    srcModel['Galactic Diffuse'] = GalProp
    srcModel['Galactic Diffuse'].name = 'Galactic Diffuse'
    srcModel['Galactic Diffuse'].spectrum.Value.free = 1
    srcModel['Extragalactic Diffuse'] = EGDiffuse
    srcModel['Extragalactic Diffuse'].spectrum.Prefactor.free = 1
    srcModel.filename = name + '_model.xml'
    srcModel.writeTo()

    return gtselect['outfile'], srcModel.filename, name


def sourceExpMap(ft1SourceFile, ft2SourceFile, exposureCube, respfunc, sourcerad, name):

    gtexpmap['evfile'] = ft1SourceFile
    gtexpmap['scfile'] = ft2SourceFile
    gtexpmap['exposure_cube_file'] = os.environ['ROOTDIR'] + exposureCube
    gtexpmap['outfile'] = 'expMap.fits'
    gtexpmap['rspfunc'] = respfunc
    gtexpmap['source_region_radius'] = sourcerad
    gtexpmap.run()

    return gtexpmap['outfile']


def sourceAnalysis(ft1SourceFile, ft2SourceFile, sourceModel, exposureCube, expMap, respfunc, name):

    exposureCube = os.environ['ROOTDIR'] + exposureCube
    obs = UnbinnedObs(ft1SourceFile, ft2SourceFile, expMap=expMap,
                      expCube=exposureCube, irfs=respfunc)
    like = UnbinnedAnalysis(obs, sourceModel, 'Minuit')
    like.fit()
    outputModel = name + '_model_out.xml'
    like.writeXml(outputModel)
    return like


def GetRoI(RoIfile, line):
    infile = RoIfile
    reg, ra, dec = read_data(infile)
    reg_num = num.array(reg,type=num.Int)
    name = ['region' + `x` for x in reg_num]
    return name[line], ra[line], dec[line]


def source_pars(infile):
    pars = parfile_parser(infile)
    return pars['roirad'], pars['sourcerad'], pars['respfunc'], pars['tstart'], pars['tstop']


if __name__ == '__main__':

    roirad, sourcerad, respfunc, tstart, tstop = source_pars(_SourcePars)
    ft1TimeFile, ft2File = getTimeData(tstart, tstop, _LatFt1File, _LatFt2File)
    ft1File = DiffuseResponse(ft1TimeFile, ft2File, respfunc)
    exposureCube = ExposureCube(ft1File, ft2File)
    line = int(os.environ['LINE_NUM'])
    ft1SourceFile, mySourceModel, name = sourceData(ft1File, roirad, line, _SourceModel)
    expMap = sourceExpMap(ft1SourceFile, ft2File, exposureCube, respfunc, sourcerad, name)
    like = sourceAnalysis(ft1SourceFile, ft2File, mySourceModel, exposureCube, expMap, respfunc, name)



