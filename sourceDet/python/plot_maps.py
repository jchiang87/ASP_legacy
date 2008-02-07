"""
@brief Plot healpix array tables using hippodraw

@author J. Chiang <jchiang@slac.stanford.edu>
"""
#
# $Header$
#

import numarray as num
from AspHealPix import Healpix, SkyDir, CountsArray, ExposureArray
import hippoplotter as plot

def spin(ra):
    if ra > 180:
        return ra - 360
    else:
        return ra

class HpArrayWrapper(object):
    def __init__(self, healpixArray):
        self.hpArray = healpixArray
        self.hp = healpixArray.healpix()
        self._set_sections()
        self.coordsys = self.hp.coordsys()
    def _set_sections(self):
        nside = self.hp.nside()
        self.section = []
        for i in range(self.hp.npix()/nside/nside):
            self.section.extend(list(i*num.ones(nside*nside)))
    def __call__(self, index, rotate=0, axis=None):
        if rotate and axis is None:
            axis = SkyDir(0, 0, self.coordsys)
        my_dir = SkyDir(self.hp[index]().ra(), self.hp[index]().dec())
        if rotate:
            my_dir = self._rotate(my_dir, axis, rotate)
        if self.coordsys == SkyDir.EQUATORIAL:
            return (spin(my_dir.ra()), my_dir.dec(),
                    self.hpArray[my_dir], self.section[index])
        else:
            return (spin(my_dir.l()), my_dir.b(),
                    self.hpArray[my_dir], self.section[index])
    def _rotate(self, indir, axis, angle):
        return SkyDir(indir().rotate(axis(), angle))
    def __getattr__(self, attrname):
        try:
            return getattr(self.hp, attrname)
        except AttributeError:
            return getattr(self.hpArray, attrname)
    def plot(self, section_cut=False):
        hp_nt = plot.newNTuple(([], [], [], []),
                               ('l', 'b', 'zvalue', 'section'))
        for i in range(self.npix()):
            hp_nt.addRow(self(i))
        disp = plot.XYZPlot(hp_nt, 'l', 'b', 'zvalue')
        disp.setTransform('HammerAito')
        if section_cut:
            sectionCut = plot.hippo.Cut(hp_nt, ('section',))
            sectionCut.addTarget(disp)
            plot.canvas.addDisplay(sectionCut)
            sectionCut.setCutRange(3.5, 4.5, 'x')
        return disp

if __name__ == '__main__':
    for day in range(5):
        cmap = HpArrayWrapper(CountsArray('counts_%03i.fits' % day))
        cmap.plot()
        emap = HpArrayWrapper(ExposureArray('exposure_%03i.fits' % day))
        emap.plot()
