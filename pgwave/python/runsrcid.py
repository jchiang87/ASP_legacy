import sys,os
import pyfits

noassocfile='NoAssiated.fits'

def loadpgwRow(pgwfits):
	hdulist  = pyfits.open(pgwfits)
	nrows=hdulist[1].header['NAXIS2']
	data1    = hdulist[1].data
	return nrows,data1	


def rungtsrcid(srcCat,testCat,outCat,prob):

	cmd = 'gtsrcid ' \
         + ' srcCatName=' + srcCat \
         + ' srcCatPrefix=SRC' \
         + ' srcCatQty=*' \
         + ' cptCatName='+testCat \
         + ' cptCatPrefix=CAT' \
         + ' cptCatQty=*' \
         + ' cptPosError=0.01' \
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
         + ' maxNumCtp=1' \
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
         + ' mode=ql'
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
      		( k, i, data1.field('@SRC_NAME')[i], data1.field(12)[i], data1.field('R')[i],data1.field('RA_J2000')[i], \
      		data1.field('DEC_J2000')[i] ,(data1.field('PROB')[i])*100.  )
  else :
    print "No counterpart found"
    
def GetNoAssociated(pgwdata,catf):
  hdulist  = pyfits.open(catf)
  data1    = hdulist[1].data
  index=[]
  if hdulist[1].header['NAXIS2'] > 0 :
    k=0
    for i in range(pgwdata.shape[0]) :
    	noass=0
    	for j in range(data1.shape[0]) :
		if(data1.field('@SRC_NAME')[j]==pgwdata.field('NAME')[i]):
			noass=1
			break
	if noass==0:
		print pgwdata[i]
		index.append(i)
  return index
		

def SaveNoAssos(pgwdata,index):
		
	c1=pyfits.Column(name='NAME',format='10A', unit=' ',array=pgwdata.field('NAME')[index])
	c2=pyfits.Column(name='RAJ2000',format='5F',unit='deg', array=pgwdata.field('RAJ2000')[index])
	c3=pyfits.Column(name='DECJ2000',format='5F', unit='deg', array=pgwdata.field('DECJ2000')[index])
	c4=pyfits.Column(name='PosErr', format='5F', unit='deg ',array=pgwdata.field('PosErr')[index])
	c5=pyfits.Column(name='CHI_2_VAR', format='5F', unit=' ',array=pgwdata.field('CHI_2_VAR')[index])
	x = pyfits.ColDefs([c1,c2,c3,c4,c5])
	tbhdu=pyfits.new_table(x)
	tbhdu.writeto('temp.fits',clobber='yes')
        #UCD 
  	hdulist = pyfits.open('temp.fits')
  	head1 = hdulist[1].header
	head1.update('TBUCD2','POS_EQ_RA_MAIN','')
  	head1.update('TBUCD3','POS_EQ_DEC_MAIN','')
  	head1.update('TBUCD4','ERROR','')
	hdulist.writeto(noassocfile,clobber='yes')
	
def runsrcid(pgwfile,prob):
	catdir=os.environ['GTSRCID_CATALOG']
	egr=os.path.join(catdir,'3EG.fits')
	nrows,pgwdata=loadpgwRow(pgwfile)
	rungtsrcid(pgwfile,egr,'assoc3g.fits',prob)
	index=GetNoAssociated(pgwdata,'assoc3g.fits')
	if(len(index)>0):
		SaveNoAssos(pgwdata,index)
		"""rungtsrcid(noassocfile,'catdir/BZCAT.fits','assocBz.fits',prob)
		nrows,pgwdata=loadpgwRow(noassocfile)
		index=GetNoAssociated(pgwdata,'assocBz.fits')"""


if __name__=="__main__":
	catdir=os.environ['GTSRCID_CATALOG']
	prob=sys.argv[2]
	nrows,pgwdata=loadpgwRow(pgwfile)
	rungtsrcid(pgwfile,'catdir/3EG.fits','assoc3g.fits',prob)
	index=GetNoAssociated(pgwdata,'assoc3g.fits')
	if(len(index)>0):
		SaveNoAssos(pgwdata,index)
		rungtsrcid(noassocfile,'catdir/BZCAT.fits','assocBz.fits',prob)
		nrows,pgwdata=loadpgwRow(noassocfile)
		index=GetNoAssociated(pgwdata,'assocBz.fits')
	 
