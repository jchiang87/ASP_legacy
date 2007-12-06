import sys,os
import pyfits
import glob
import numarray as num
from HealPix import Healpix,Pixel, SkyDir
noassocfile='NoAssiated.fits'
index=[]
ddec=[]
rra=[]
def loadpgwRow(pgwfits):
	hdulist  = pyfits.open(pgwfits)
	nrows=hdulist[1].header['NAXIS2']
	data1    = hdulist[1].data
	for i in range(0,nrows):
		index.append('UNIDENTIFIED')
		ddec.append(0.)
		rra.append(0.)
	return nrows,data1	


def rungtsrcid(srcCat,testCat,outCat,prob):

	cmd = 'gtsrcid' \
         + ' srcCatName='+srcCat \
         + ' srcCatPrefix=\"SRC\"' \
         + ' srcPosError=\"1\"' \
         + ' cptCatName='+testCat \
         + ' cptCatPrefix=\"CAT\"' \
         + ' outCatName='+outCat \
         + ' probMethod=\"POSITION\"' \
         + ' probThres=\"0.0001\"' \
         + ' maxNumCpt=\"1\" '


	"""cmd = 'gtsrcid ' \
         + ' srcCatName=' + srcCat \
         + ' srcCatPrefix=SRC' \
         + ' srcCatQty=*' \
         + ' cptCatName='+testCat \
         + ' cptCatPrefix=CAT' \
         + ' cptCatQty=*' \
         + ' cptPosError=1' \
         + ' outCatName='+outCat \
         + ' outCatQty01=\'R=arccos(sin($@SRC_DECJ2000$*2*#pi/360)*sin($@CAT_DEJ2000$*2*#pi/360)+cos($@SRC_DECJ2000$*2*#pi/360)*cos($@CAT_DEJ2000$*2*#pi/360)*cos($@SRC_RAJ2000$*2*#pi/360-$@CAT_RAJ2000$*2*#pi/360))*360/(2*#pi)\''\
         + ' outCatQty03=\"\"' \
         + ' outCatQty04=\"\"' \
         + ' outCatQty05=\"\"' \
         + ' outCatQty06=\"\"' \
         + ' outCatQty07=\"\"' \
         + ' outCatQty08=\"\"' \
         + ' outCatQty09=\"\"' \
         + ' probMethod=POSITION' \
         + ' probThres='+str(prob) \
         + ' maxNumCpt=1' \
         + ' select01=\"\"' \
         + ' select02=\"\"' \
         + ' select03=\"\"' \
         + ' select04=\"\"' \
         + ' select05=\"\"' \
         + ' select06=\"\"' \
         + ' select07=\"\"' \
         + ' select08=\"\"' \
         + ' select09=\"\"' \
         + ' chatter=4' \
         + ' clobber=yes' \
         + ' debug=no' \
         + ' mode=ql'"""
	os.system(cmd)
	
def printCat(catf):
  hdulist  = pyfits.open(catf)
  data1    = hdulist[1].data
  if hdulist[1].header['NAXIS2'] > 0 :
    k=0
    for i in range(data1.shape[0]) :
     	#if data1.field('PROB')[i]>0.40:
		k=k+1
      		print '%d, %d, %s, %s, %5.2f,RA=%5.2f, DEC=%5.2f, 	Prob.=%5.2f' % \
      		( k, i, data1.field('@SRC_NAME')[i], data1.field('@CAT_3EG')[i], data1.field('R')[i],data1.field('RA_J2000')[i], \
      		data1.field('DEC_J2000')[i] ,(data1.field('PROB')[i])*100.  )
  else :
    print "No counterpart found"
    
def GetAssociated(pgwdata,catf,prefix):
  hdulist  = pyfits.open(catf)
  data1    = hdulist[1].data
 
  if hdulist[1].header['NAXIS2'] > 0 :
    k=0
    for i in range(pgwdata.shape[0]) :
    	for j in range(data1.shape[0]) :
		if(data1.field('@SRC_NAME')[j]==pgwdata.field('NAME')[i]):
			if index[i]=='UNIDENTIFIED':
				index[i]=prefix+'_'+data1.field('@CAT_NAME')[j]
			else:
				index[i]=index[i]+','+prefix+'_'+data1.field('@CAT_NAME')[j]
			ddec[i]=data1.field('DEC_J2000')[j]
			rra[i]=data1.field('RA_J2000')[j]
			print pgwdata.field('NAME')[i],index[i],rra[i],ddec[i] #data1.field('R')[j]
			break
	
		
    
		

def SaveAssoc(pgwfile,pgwdata):
	id=[]
	hp = Healpix(16, Healpix.NESTED, SkyDir.GALACTIC)
	for ra, dec in zip(rra, ddec): 
		pix = Pixel(SkyDir(ra, dec), hp)        
		id.append(pix.index())
	c0=pyfits.Column(name='HEALPIX_ID',format='D', unit=' ',array=num.array(id,dtype=num.Int))		
	c1=pyfits.Column(name='NAME',format='10A', unit=' ',array=pgwdata.field('NAME'))
	c2=pyfits.Column(name='RAJ2000',format='5F',unit='deg', array=pgwdata.field('RAJ2000'))
	c3=pyfits.Column(name='DECJ2000',format='5F', unit='deg', array=pgwdata.field('DECJ2000'))
        c4=pyfits.Column(name='Theta95', format='5F', unit='deg ',array=pgwdata.field('Theta95'))        
	c5=pyfits.Column(name='L', format='5F', unit='deg',array=pgwdata.field('L'))        
	c6=pyfits.Column(name='B', format='5F', unit='deg',array=pgwdata.field('B'))        
	c7=pyfits.Column(name='Flux(E>100)', format='6F', unit='ph/cm^2s^-1',array=pgwdata.field('Flux(E>100)'))
        c8=pyfits.Column(name='errFlux', format='6F', unit=' ',array=pgwdata.field('errFlux'))

        c9=pyfits.Column(name='CHI_2_VAR', format='5F', unit=' ',array=pgwdata.field('CHI_2_VAR'))
        c10=pyfits.Column(name='FLARING_FLAG', format='1F', unit=' ',array=pgwdata.field('FLARING_FLAG'))
	c11=pyfits.Column(name='COUNTERPART', format='70A', unit=' ',array=index)

	x = pyfits.ColDefs([c0,c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11])
	tbhdu=pyfits.new_table(x)
	tbhdu.writeto('temp.fits',clobber='yes')
        #UCD 
  	hdulist = pyfits.open('temp.fits')
  	head1 = hdulist[1].header
	head1.update('TBUCD2','POS_EQ_RA_MAIN','')
  	head1.update('TBUCD3','POS_EQ_DEC_MAIN','')
  	head1.update('TBUCD4','ERROR','')
	hdulist.writeto(pgwfile,clobber='yes')
	
	
def runsrcid(pgwfile,prob):

	nrows,pgwdata=loadpgwRow(pgwfile)
	catfiles=loadCatFileName()
	catfiles.sort()
	for i in range(0,len(catfiles)):
		prefix=catfiles[i].split('/')[-1].split('.')[0]
		print prefix
		rungtsrcid(pgwfile,catfiles[i],'assoc.fits',prob)
		GetAssociated(pgwdata,'assoc.fits',prefix)
	SaveAssoc(pgwfile,pgwdata)
	os.system('rm temp.fits assoc.fits')


def loadCatFileName():
	catfile=os.environ['CATDIR']+'/*.fits'
	files=glob.glob(catfile)
	return files

if __name__=="__main__":
	
	pgwfile=sys.argv[1]
	prob=sys.argv[2]
	runsrcid(pgwfile,prob)
