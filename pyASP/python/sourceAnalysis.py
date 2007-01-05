"""
@brief Region-of-intereset source analysis for DRP monitoring.

@author J. Carson <carson@slac.stanford.edu>
@author J. Chiang <jchiang@slac.stanford.edu>
"""
#
# $Header$
#

import os, sys
from GtApp import GtApp
from UnbinnedAnalysis import *
from drpRoiSetup import rootpath, pars, rois, output_dir
from DbEntry import DbEntry

debug = False

id = int(os.environ['ROI_ID']) - 1
name = rois[id].name
os.chdir(name)

ft1file = name + '_events.fits'
srcModel = os.path.join(os.getcwd(), name + '_model.xml')

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
    outputModel = name + '_model_out.xml'
    like.writeXml(outputModel)

#    for srcname in like.model.srcNames:
#        src = like.model[srcname]
#        print src.src.getType()
#        if src.src.getType() != 'Diffuse':
#            spec = src.funcs['Spectrum']
#            integral = spec.getParam('Integral')
#            index = spec.getParam('Index')
#            output = open(os.path.join(output_dir, '..', srcname+'.txt'), 'a')
#            output.write('%i  %i  %e  %e  %e  %e\n' %
#                         (pars['start_time'], pars['stop_time'],
#                          integral.getTrueValue(),
#                          integral.error()*integral.getScale(),
#                          spec.getParam('Index').value(),
#                          spec.getParam('Index').error()))
#            output.close()

    gtselect = GtApp('gtselect')

    class SourceFluxes(dict):
        def __init__(self, name, srcModel):
            self.name = name
            self.srcModel = srcModel
        def update(self, emin, emax, flux, fluxerr):
            variable = "flux_%i_%i" % (emin, emax)
            dbEntry = DbEntry(self.name, variable, pars['start_time'],
                              pars['stop_time'])
            dbEntry.setValues(flux, fluxerr)
            dbEntry.setMetaData("xmlFile", self.srcModel)
            self[(emin, emax)] = (flux, fluxerr, dbEntry)
        def write(self, fileobj, elims):
            fileobj.write('%e  %e  ' % self[elims][:2])

    def fitEnergyBand(emin, emax, sources, srcModel):
        gtselect['infile'] = ft1file
        gtselect['outfile'] = 'events_%i_%i.fits' % (emin, emax)
        gtselect['rad'] = 180
        gtselect['emin'] = emin
        gtselect['emax'] = emax
        gtselect.run()
        obs = UnbinnedObs(gtselect['outfile'], pars['ft2file'],
                          expMap=pars['expMap'],
                          expCube=rootpath(pars['expCube']),
                          irfs=irfs)
        like = UnbinnedAnalysis(obs, srcModel, 'Minuit')

        ptsrcs = []
        for srcname in like.model.srcNames:
            if like.model[srcname].src.getType() == 'Point':
                ptsrcs.append(srcname)

        for srcname in ptsrcs:
            src = like.model[srcname]
#            flux_est = src.flux(emin, emax)
#            integral = src.funcs['Spectrum'].getParam('Integral')
#            integral.parameter.setTrueValue(flux_est)
            lowerLimit = src.funcs['Spectrum'].getParam('LowerLimit')
            lowerLimit.parameter.setValue(emin)
            upperLimit = src.funcs['Spectrum'].getParam('UpperLimit')
            upperLimit.parameter.setValue(emax)

        print like.model
        sys.stdout.flush()

        try:
            like.fit()
        except RuntimeError:
            like.fit()
        print like.model
        sys.stdout.flush()

        for srcname in ptsrcs:
            src = like.model[srcname]
            spec = src.funcs['Spectrum']
            integral = spec.getParam('Integral')
            flux = integral.getTrueValue()
            fluxerr = integral.error()*integral.getScale()
            if srcname not in sources.keys():
                sources[srcname] = SourceFluxes(srcname)
            sources[srcname].update(emin, emax, flux, fluxerr)

    sources = {}
    emins = [100, 300, 1e3, 3e3, 1e4, 100]
    emaxs = [300, 1e3, 3e3, 1e4, 2e5, 2e5]

    for emin, emax in zip(emins, emaxs):
        fitEnergyBand(emin, emax, sources, srcModel)

    for srcname in sources.keys():
        output = open(os.path.join(output_dir, '..', srcname+'.txt'), 'a')
        output.write("%i  %i  " % (pars['start_time'], pars['stop_time']))
        for emin, emax in zip(emins, emaxs):
            sources[srcname].write(output, (emin, emax))
        output.write('\n')
        output.close()

    os.system('chmod 666 *')
