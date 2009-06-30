import pyfits
import sys,pyASP

def tjd2jd(tjd):
        return (2440000.5+tjd)

def tjd2mjd(tjd):
        return (40000.+tjd)

def getSunPos(jdd):
	jd=pyASP.JulianDate(jdd)
	sun=pyASP.SolarSystem(pyASP.SolarSystem.SUN)
	dd=sun.direction(jd)
	return dd

def getMoonPos(jdd):
	jd=pyASP.JulianDate(jdd)
	moon=pyASP.SolarSystem(pyASP.SolarSystem.MOON)
	dd=moon.direction(jd)
	return dd
def getEventTimeInterval(infile):
	ft1=pyfits.open(infile)
	gti=ft1[2].data
	fthdr=ft1[1].header
	start=gti.field('START')[0]
	stop=gti.field('STOP')[-1]
	dt=stop-start
	dateobs=fthdr['DATE-OBS']
	gr=fthdr['DATE-OBS'].split('T')
	year=gr[0].split('-')
	ut=gr[1].split(':')
	utt=(float(ut[0])+float(ut[1])/60.+float(ut[0])/3600.)
	mstart=pyASP.JulianDate(int(year[0]),int(year[1]),int(year[2]),utt)
	mjdstart=tjd2jd(mstart.tjd())
	mjdstop=mjdstart+(stop-start)/86400.
	midjd=(mjdstart+mjdstop)/2.
	d={"tstart":start,"tstop":stop,"date":dateobs,"jdstart":mjdstart,"jdstop":mjdstop, "tdiff":dt,"midjd":midjd}
	return d

if __name__=='__main__':
	d=getEventTimeInterval(sys.argv[1])
	print d
	sunpos=getSunPos(d["midjd"])
	print sunpos.ra(), sunpos.dec()
	sunpos=getSunPos(d["jdstop"])
        print sunpos.ra(), sunpos.dec()
