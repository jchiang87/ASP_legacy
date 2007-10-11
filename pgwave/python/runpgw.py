import os,sys
from GtApp import GtApp
import pyfits
import numarray as num
from pgw2fits import *
from runsrcid import *
#Sc2Ft2File=os.environ['INPUTFT2FILE']
#tSc2Data ='nicola5.fits'

gtselect = GtApp('gtselect')
gtbin = GtApp('gtbin')
gtexposure = GtApp('gtexposure')

pgwaveprog=os.path.join(os.environ['PGWAVEROOT'], os.environ['BINDIR'])+'/pgwave2D.exe'
#pgwaveprog='pgwave'

def makeMap(infile,mapPar,outfil):
	gtbin.debug=False
	gtbin['algorithm']='CMAP'
	gtbin['evfile']=infile
	gtbin['outfile']=outfil
	gtbin['scfile']='NONE'
	"""gtbin['numxpix']=mapPar[3]
	gtbin['numypix']=mapPar[4]
	gtbin['proj']=mapPar[2]
	gtbin['xref']=mapPar[0]
	gtbin['yref']=mapPar[1]
	gtbin['pixscale']=mapPar[5]
	"""
	gtbin['nxpix']=mapPar[3]
	gtbin['nypix']=mapPar[4]
	gtbin['proj']=mapPar[2]
	gtbin['xref']=mapPar[0]
	gtbin['yref']=mapPar[1]
	gtbin['binsz']=mapPar[5]
	gtbin.run()

def makeLC(infile,lcPar,outfil):	
	gtbin['algorithm']='LC'
	gtbin['evfile']=infile
	gtbin['outfile']=outfil
	gtbin['scfile']=Sc2Ft2File
	gtbin['timebinalg']='LIN'
	gtbin['tstart']=lcPar[0]
	gtbin['tstop']=lcPar[1]
	gtbin['deltatime']=lcPar[2]
	gtbin.run()

def calcExposure(infile):	
	gtexposure['lcfile']=infile
	gtexposure['scfile']=Sc2Ft2File
	gtexposure['rspfunc']='Pass4_v2'
	gtexposure['spectral_index']=-2.1
	gtexposure.run()

def createMap(infil,mapPar,outf):
	makeMap(infil,mapPar,outf)

def pgwave(filein):
	param='bgk_choise=n circ_square=s N_scale=1 scala=\"3.0\" otpix=\"10\" n_sigma=3 median_box=5 kappa=3 min_pix=2 border_size=4 fitsio_choice=n recursive_choice=n verbose_level=0'
	command=pgwaveprog +' '+filein+' '+param
	print command
	os.system(command)


def runpgw(infile):
	workdir=os.getcwd()
	print 'Running PGWave in dir: ',workdir
	tmp=infile
	cmd='fcopy \"'+infile+'[EVENTS][CTBCLASSLEVEL>1]\"'+' filtered.fits'
	os.system(cmd) 
	sizex=720
	sizey=360
	scale=0.5
	ra=180.
	dec=0.
	infile='filtered.fits'
	mapPar=[ra,dec,'CAR',sizex,sizey,scale]
	inmap1=infile.replace('.fits','_map.fits')  #os.path.join(workdir,((os.environ['INPUTFT1FILE']).split('.')[0]+'_map.fits'))
	if os.path.exists(inmap1)==False:
		createMap(infile,mapPar,inmap1)
#	os.environ['OUTPUTF1MAP']=os.path.abspath(#inmap1)
#	inmap=(os.environ['INPUTFT1FILE']).split('.')[0]+'_map.fits'
#	pgwfile=(inmap.split('.'))[0]+'.list'
#        if os.path.exists(pgwfile)==False:
        pgwave(inmap1)
	outf=inmap1.replace('.fits','.list')
	outfits=pgw2fits(outf,1)
	runsrcid(outfits,.30)
	print 'PGWave FITS output file:',outfits 
	#outf=os.path.abspath(pgwfile)
#	os.environ['PGWOUTPUTLIST']=pgwfile

if __name__=="__main__":
	os.chdir(os.environ['OUTPUTDIR'])
	runpgw('time_filtered_events.fits')
	os.system('chmod 777 *')
		
