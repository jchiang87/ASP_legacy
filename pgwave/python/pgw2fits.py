import pyfits,commands,sys
import numarray as num
import os
from readpgw import *
import lc
from HealPix import CountsArray, ExposureArray, SkyDir

def getFlux(ra,dec,counts):
	emapfile='exposure_'+os.environ['DownlinkId']+'.fits'
	#emapfile='exposure_255514800.fits'
	emap = ExposureArray(emapfile)
	flux=num.zeros(len(ra),dtype=num.Float)
	errflux=num.zeros(len(ra),dtype=num.Float)
	for i in range(0,len(ra)):
		exposure_value=(emap[SkyDir(ra[i], dec[i])])
		if exposure_value>0:
			flux[i]=counts[i]/exposure_value
			errflux[i]=num.sqrt(counts[i])/exposure_value
	return flux,errflux

PI=3.14159265358979
conv=PI/180.000000000

def eq2gal(ra,dec):
        a1=62.872*conv
        a3=32.933*conv
        a2=(num.array(ra)*conv - 282.86*conv)
        d=num.array(dec)*conv
        b=num.arcsin(num.sin(d)*num.cos(a1)-num.cos(d)*num.sin(a2)*num.sin(a1))
        s1=(num.sin(d)*num.sin(a1)+num.cos(d)*num.sin(a2)*num.cos(a1))/num.cos(b)
        l=(num.arcsin(s1)+a3)
        for i in range(0,len(l)):
                if l[i]<0.:
                  l[i]+=2*PI

        b=b/conv
        l=l/conv
        return l,b


def pgw2fits(pgwfile,flag):
	pgwfits=pgwfile.replace('.list','_pgw_out.fits')
	filevt=pgwfile.replace('_map.list','.fits')
	name_pgw,ra_pgw,dec_pgw,posErr,signi_pgw=readpgw(pgwfile)
	l_pgw,b_pgw=eq2gal(ra_pgw,dec_pgw)
	#posErr=[]
	count=[]
	chi2=[]
	fla=[]
	print '---Variability check----'
	#filevt=os.path.join(os.environ['INPUTFT1DIR'],os.environ['INPUTFT1FILE'])
	chi=0.
	nbins=6
	radius=3.0
	print "NAME            RA       DEC    SIGNIF  COUNTS  CHI2"
	for i in range(0,len(ra_pgw)):
		if flag==1:
			chi,cou,sd=lc.createLC(filevt,name_pgw[i],ra_pgw[i],dec_pgw[i],radius,nbins)
			count.append(cou)
			if chi>10. and cou/float(nbins)>=5.:
				chi2.append(chi)
				fla.append(1)
				print name_pgw[i],'\t',ra_pgw[i],'\t',dec_pgw[i],'\t',signi_pgw[i],'\t',cou,'\t',chi
			else:
				fla.append(0)
				chi=0.
				chi2.append(0)
				print name_pgw[i],'\t',ra_pgw[i],'\t',dec_pgw[i],'\t',signi_pgw[i],'\t',cou,'\t',chi

		else:
			chi2.append(0)
			count.append(0)
			fla.append(0)
			print name_pgw[i],'\t',ra_pgw[i],'\t',dec_pgw[i],'\t',signi_pgw[i],'\t',chi
		#posErr.append(1.)
	flux,errflux=getFlux(ra_pgw,dec_pgw,count)
	c1=pyfits.Column(name='NAME',format='10A', unit=' ',array=name_pgw)
	c2=pyfits.Column(name='RAJ2000',format='5F',unit='deg', array=num.array(ra_pgw))
	c3=pyfits.Column(name='DECJ2000',format='5F', unit='deg', array=num.array(dec_pgw))
	c4=pyfits.Column(name='Theta95', format='5F', unit='deg ',array=num.array(posErr))
        c5=pyfits.Column(name='L', format='5F', unit='deg',array=l_pgw)        
	c6=pyfits.Column(name='B', format='5F', unit='deg',array=b_pgw)
	c7=pyfits.Column(name='Flux(E>100)', format='6F', unit='ph/cm^2s^-1',array=flux)
	c8=pyfits.Column(name='errFlux', format='6F', unit=' ',array=errflux)

	c9=pyfits.Column(name='CHI_2_VAR', format='5F', unit=' ',array=num.array(chi2))
	c10=pyfits.Column(name='FLARING_FLAG', format='1F', unit=' ',array=num.array(fla))
	x = pyfits.ColDefs([c1,c2,c3,c4,c5,c6,c7,c8,c9,c10])
	tbhdu=pyfits.new_table(x)
	tbhdu.writeto('temp.fits',clobber='yes')
	hd=(pyfits.open(filevt))[0].header   
     # add UCD in header
  	hdulist = pyfits.open('temp.fits')
  	head1 = hdulist[1].header
	head1.update('EXTNAME','PGWCAT',' ')
	head1.update('DATE-OBS',hd['DATE-OBS'],'')
	head1.update('DATE-END',hd['DATE-END'],'')
	head1.update('TBUCD2','POS_EQ_RA_MAIN','')
  	head1.update('TBUCD3','POS_EQ_DEC_MAIN','')
  	head1.update('TBUCD4','ERROR','')
	hdulist.writeto(pgwfits,clobber='yes')
	commands.getoutput('rm test.fits')
	#os.environ['PGWOUTPUTFITSLIST']=pgwfits
	return pgwfits	
if __name__=="__main__":
	pgwfile=sys.argv[1]
	pgw2fits(pgwfile,1)
