import sys,os
import pyfits
import glob
import numpy as num
import astroUtil as ast
from AspHealPix import Healpix,Pixel, SkyDir
import dbmanager as db
import sendFAmail as smail
import datetime as dt
noassocfile='NoAssiated.fits'
index=[]
ddec=[]
rra=[]
sunFlag=0
sunSunId=-1
def loadpgwRow(pgwfits):
	hdulist  = pyfits.open(pgwfits)
	nrows=hdulist[1].header['NAXIS2']
	data1    = hdulist[1].data
	decData = num.array(data1.field('DECJ2000'), dtype=num.float)  
	raData=num.array(data1.field('RAJ2000'), dtype=num.float)
	for i in range(0,nrows):
		index.append('UNIDENTIFIED')
		ddec.append(decData[i])
		rra.append(raData[i])
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
  #decData = num.array(data1.field('DEC_J2000'), dtype=num.float)
  #raData=num.array(data1.field('RA_J2000'), dtype=num.float) 
  if hdulist[1].header['NAXIS2'] > 0 :
    k=0
    for i in range(pgwdata.shape[0]) :
    	for j in range(data1.shape[0]) :
		if(data1.field('@SRC_NAME')[j]==pgwdata.field('NAME')[i]):
			if index[i]=='UNIDENTIFIED':
				index[i]=prefix+'_'+data1.field('@CAT_NAME')[j]
			else:
				index[i]=index[i]+','+prefix+'_'+data1.field('@CAT_NAME')[j]
				if (prefix=='PSR' or prefix=='SNR') and pgwdata.field('FLARING_FLAG')[i]==1.:
					#print index[i], pgwdata.field('NAME')[i]
					pgwdata.field('FLARING_FLAG')[i]=0
			#ddec[i]=decData[j]
			#rra[i]=raData[j]
			#print pgwdata.field('NAME')[i],index[i],rra[i],ddec[i] #data1.field('R')[j]
			break
	
def checkSun(pgwdata,dateinfo):
	#print d        
	sunpos=ast.getSunPos(dateinfo['midjd'])        
	k=0        
	for ra, dec in zip(rra, ddec):                
		dis=sunpos.difference(SkyDir(ra,dec))*180./3.1415   
                if  dis<=1.:   
	            sunFlag=1                        
		    sourceSunId=k   
		    index[k]=("SUN_%i " % dateinfo['tstart'])+index[k]
		    pgwdata.field('NAME')[k]=("SUN_(%s)" % pgwdata.field('NAME')[k])
                    print "Sun Pos close to Source:",pgwdata.field('NAME')[k]                
	k=k+1	
	return sunpos	

def gethealPix():
	id=[]        #checkSun(pgwadata)             
	hp = Healpix(32, Healpix.NESTED, SkyDir.EQUATORIAL)        
	for ra, dec in zip(rra, ddec):                
		pix = Pixel(SkyDir(ra, dec), hp)               
		id.append(pix.index())
	return id

def SaveAssoc(pgwfile,pgwdata,sourceName):
	id=[]        #checkSun(pgwadata)                     
	hp = Healpix(32, Healpix.NESTED, SkyDir.EQUATORIAL)        
	for ra, dec in zip(rra, ddec):                
		pix = Pixel(SkyDir(ra, dec), hp)                
		id.append(pix.index())        

	source={'NAME':sourceName,
		'HEALPIX_ID':id,
		'RAJ2000':pgwdata.field('RAJ2000'),
		'DECJ2000':pgwdata.field('DECJ2000'),
		'Theta95':pgwdata.field('Theta95'),
		'flux':pgwdata.field('Flux(E>100)'),
		'errFlux':pgwdata.field('errFlux'),
		'chi2':pgwdata.field('CHI_2_VAR'),
		'FLARING_FLAG':pgwdata.field('FLARING_FLAG')
		}
	c0=pyfits.Column(name='HEALPIX_ID',format='D', unit=' ',array=num.array(id,dtype=num.int))		
	c1=pyfits.Column(name='NAME',format='30A', unit=' ',array=sourceName)
	c2=pyfits.Column(name='RAJ2000',format='5F',unit='deg', array=pgwdata.field('RAJ2000'))
	c3=pyfits.Column(name='DECJ2000',format='5F', unit='deg', array=pgwdata.field('DECJ2000'))
        c4=pyfits.Column(name='Theta95', format='5F', unit='deg ',array=pgwdata.field('Theta95'))        
	c5=pyfits.Column(name='L', format='5F', unit='deg',array=pgwdata.field('L'))        
	c6=pyfits.Column(name='B', format='5F', unit='deg',array=pgwdata.field('B'))        
	c7=pyfits.Column(name='Flux(E>100)', format='6F', unit='ph/cm^2s^-1',array=pgwdata.field('Flux(E>100)'))
        c8=pyfits.Column(name='errFlux', format='6F', unit=' ',array=pgwdata.field('errFlux'))

        c9=pyfits.Column(name='CHI_2_VAR', format='5F', unit=' ',array=pgwdata.field('CHI_2_VAR'))
        c10=pyfits.Column(name='FLARING_FLAG', format='1F', unit=' ',array=pgwdata.field('FLARING_FLAG'))
	c11=pyfits.Column(name='COUNTERPART', format='100A', unit=' ',array=index)

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
	return source

def checkPointSource(pgwdata,dateinfo):
	idpix=gethealPix()
	mydb=db.dbmanager()
        mydb.getPointSources()
        #mydb.close()
	procid=int(os.environ['PIPELINE_PROCESSINSTANCE'])
	ra=db._PointSourcesFields['RA'][1]
	dec=db._PointSourcesFields['DEC'][1]
	i=0
	source_name=[]
	for r, de in zip(rra, ddec):                
		a=SkyDir(r,de)
		k=0
		flag=0
	        for rr,dd in zip(ra,dec):
		  dis=a.difference(SkyDir(rr,dd))*180./3.1415 
		  #print dis  
	          if  dis<=1.:
			index[i]=(db._PointSourcesFields['SOURCE_TYPE'][1])[k]+'_'+(db._PointSourcesFields['PTSRC_NAME'][1])[k]+','+index[i]
			#print "trovata:",pgwdata.field('NAME')[i],(db._PointSourcesFields['PTSRC_NAME'][1])[k],dis
			source_name.append((db._PointSourcesFields['PTSRC_NAME'][1])[k])
			mydb.insertFlareEvent((db._PointSourcesFields['PTSRC_NAME'][1])[k],dateinfo['tstart'],dateinfo['tstop'],pgwdata.field('Flux(E>100)')[i],pgwdata.field('errFlux')[i],pgwdata.field('CHI_2_VAR')[i],int(pgwdata.field('FLARING_FLAG')[i]),1,procid)
			flag=1
			break
		  k=k+1
		if flag==0:
			name=mydb.insertPointSource(idpix[i],r,de,1.)
			source_name.append(name)
			mydb.insertFlareEvent(name,dateinfo['tstart'],dateinfo['tstop'],pgwdata.field('Flux(E>100)')[i],pgwdata.field('errFlux')[i],pgwdata.field('CHI_2_VAR')[i],int(pgwdata.field('FLARING_FLAG')[i]),1,procid)
		i=i+1

	mydb.close()
	return source_name

def inviaMail(testo):
	_fromaddress="tosti@slac.stanford.edu"
        _toaddress=['tosti@pg.infn.it']
        subject='test FA mail'
        smail.sendFAmail(_fromaddress,_toaddress,subject,testo)

def faMessage(source,sunpos):
        flag=num.array(source['FLARING_FLAG'])
        testo="Flaring Source Pipeline Report\n"
	testo=testo+("UTC DATE:%s\n" % (dt.datetime.utcnow().isoformat()))
	if len(flag)>0:
           for i in range(0,len(flag)):
                if flag[i]>0:
                  testo=testo+"Flaring source found:"+source['NAME'][i]+(" at RA=%f, DEC=%f\n"% (source['RAJ2000'][i],source['DECJ2000'][i]))
	else:
	   testo=testo+'NO FLARING SOURCE DETECTED\n' 	
	ss= ("Sun (RA,DEC): %7.4f,%7.4f \nSun (l,b): %7.4f,%7.4f\n" % (sunpos.ra(), sunpos.dec(),sunpos.l(),sunpos.b()))
	testo=testo+ss+'\nData Products at: http://glast-ground.slac.stanford.edu/ASPDataViewer/\n'
	return (testo)

def runsrcid(pgwfile,prob):
	dateinfo=ast.getEventTimeInterval('Filtered_evt.fits')
	nrows,pgwdata=loadpgwRow(pgwfile)
	catfiles=loadCatFileName()
	catfiles.sort()
	for i in range(0,len(catfiles)):
		prefix=catfiles[i].split('/')[-1].split('.')[0]
		print "Checking for sources in:",prefix
		rungtsrcid(pgwfile,catfiles[i],'assoc.fits',prob)
		GetAssociated(pgwdata,'assoc.fits',prefix)
	sun=checkSun(pgwdata,dateinfo)
	sourceName=checkPointSource(pgwdata,dateinfo)
	source = SaveAssoc(pgwfile,pgwdata,sourceName)
	testo=faMessage(source,sun)
	inviaMail(testo)
	os.system('rm temp.fits assoc.fits')


def loadCatFileName():
	catfile=os.environ['CATDIR']+'/*.fits'
	files=glob.glob(catfile)
	return files

if __name__=="__main__":
	
	pgwfile=sys.argv[1]
	prob=sys.argv[2]
	runsrcid(pgwfile,prob)
