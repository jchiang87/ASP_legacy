import numarray as num
import pyASP
import hippoplotter as plot

met0 = 223089703.

met = num.arange(0, 3.155e7, 8.64e4) + met0

sun = pyASP.SolarSystem()

def sun_dir(my_met):
    return sun.direction(pyASP.jd_from_MET(my_met))

nt = plot.newNTuple(([], [], []), ('time', 'RA', 'Dec'))

for t in met:
    sdir = sun_dir(t)
    nt.addRow((t, sdir.ra(), sdir.dec()))

disp = plot.Scatter(nt, 'RA', 'Dec')

