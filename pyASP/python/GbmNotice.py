"""
@brief Encapsulation of information in a GBM notice.
@author J. Chiang <jchiang@slac.stanford.edu>
"""
#
# $Header$
#

import pyASP

_LatFt2File = '/nfs/farm/g/glast/u33/jchiang/DC2/DC2_FT2_v2.fits'

class GbmNotice(object):
    _id = {'BURST Name' : 'Name',
           'BURST Date' : 'Date',
           'BURST Time' : 'Time',
           'BURST RA' : 'RA',
           'BURST DEC' : 'DEC',
           'BURST LOC' : 'LOC_ERR',
           'Standard Intensity' : 'Intensity',
           'Closest detectors' : 'Closest_detectors'}
    def __init__(self, infile):
        notice = open(infile)
        for line in notice:
            self._parseLine(line)
        self.start_time = self._convertMET(self.Date, self.Time)
        self.RA = float(self.RA)
        self.DEC = float(self.DEC)
        self.LOC_ERR = float(self.LOC_ERR)
    def _convertMET(self, date, time):
        year = 2000 + int(date[:2])
        month = int(date[2:4])
        day = int(date[4:6])
        hours = float(time)/3600.
        jd = pyASP.JulianDate(year, month, day, hours)
        return jd.seconds() - pyASP.JulianDate_missionStart().seconds()
    def _parseLine(self, line):
        if line.find('=') != -1:
            fields = line.split()
            self.__dict__[self._id[' '.join(fields[:2])]] = fields[-1]
            if fields[0] == 'Closest':
                self.Closest_detectors = line.split('=')[-1].strip().split()
    def offAxisAngle(self, Ft2File=_LatFt2File):
        import numarray as num
        from FitsNTuple import FitsNTuple
        ft2 = FitsNTuple(Ft2File, 'SC_DATA')
        indx = num.where(ft2.START > self.start_time)
        ii = indx[0][0]
        dir1 = pyASP.SkyDir(ft2.RA_SCZ[ii-1], ft2.DEC_SCZ[ii-1])
        dir2 = pyASP.SkyDir(ft2.RA_SCZ[ii], ft2.DEC_SCZ[ii])
        t1 = ft2.START[ii-1]
        t2 = ft2.START[ii]
        my_dir = pyASP.SkyDir_interpolate(dir1, dir2, t1, t2,
                                            self.start_time)
        return my_dir.difference(pyASP.SkyDir(self.RA, self.DEC))*180./num.pi

if __name__ == '__main__':
    import glob
    files = glob.glob('../Notices/*NOTICE*')
    for item in files:
        notice = GbmNotice(item)
        print notice.Name, notice.RA, notice.DEC, notice.offAxisAngle()
