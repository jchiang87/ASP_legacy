"""
@brief Class to parse named parameters in a text file as key/value
pairs and return the output as a dict, performing conversions to float
as appropriate.

@author J. Chiang <jchiang@slac.stanford.edu>
"""
#
# $Header$
#

class Parfile(dict):
    def __init__(self, filename):
        self.filename = filename
        self.keylist = []
        try:
            self._readfile()
        except IOError:
            pass
    def _readfile(self):
        for line in open(self.filename).readlines():
            key, value = line.split("=")
            try:
                self[key.strip()] = float(value.strip())
            except ValueError:
                self[key.strip()] = value.strip()
    def __setitem__(self, key, value):
        if self.keylist.count(key) == 0:
            self.keylist.append(key)
        dict.__setitem__(self, key, value)
    def write(self, outfile=None):
        if outfile is not None:
            self.filename = outfile
        output = open(self.filename, 'w')
        for key in self.keylist:
            output.write('%s = %s\n' % (key, `self[key]`))
        output.close()

# retain this for backwards compatibility
def parfile_parser(infile):
    return Parfile(infile)

if __name__ == '__main__':
    pars = Parfile('foo.pars')
    pars['ft1file'] = 'ft1.fits'
    pars['ft2file'] = 'ft2.fits'
    pars['ra'] = 83.57
    pars['dec'] = 22.01
    pars['ft1file'] = 'ft1_file.fits'
    pars.write()
    
    foo = Parfile('foo.pars')
    print foo['ft1file']
    print foo['ft2file']
    print foo['ra']
    print foo['dec']
