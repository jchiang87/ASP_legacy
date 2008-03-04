import pyfits,commands,sys
import numarray as num
import os
from readpgw import *
import lc

def pgw2fits(pgwfile,flag):
	pgwfits=(pgwfile.split('.'))[0]+'_pgw_out.fits'
	name_pgw,ra_pgw,dec_pgw,signi_pgw=readpgw(pgwfile)
	posErr=[]
	chi2=[]
	print '---Variability check----'
	filevt=os.path.join(os.environ['INPUTFT1DIR'],os.environ['INPUTFT1FILE'])
	print "NAME            RA       DEC    SIGNIF  CHI_2"
	for i in range(0,len(ra_pgw)):
		if flag==1:
			chi=lc.createLC(filevt,name_pgw[i],ra_pgw[i],dec_pgw[i],2.5,6)
			if chi>10.:
				chi2.append(chi)
				print name_pgw[i],'\t',ra_pgw[i],'\t',dec_pgw[i],'\t',signi_pgw[i],'\t',chi
			else:
				chi2.append(0)
		else:
			
			print name_pgw[i],'\t',ra_pgw[i],'\t',dec_pgw[i],'\t',signi_pgw[i],'\t',chi
		posErr.append(1.)
	c1=pyfits.Column(name='NAME',format='10A', unit=' ',array=name_pgw)
	c2=pyfits.Column(name='RAJ2000',format='5F',unit='deg', array=num.array(ra_pgw))
	c3=pyfits.Column(name='DECJ2000',format='5F', unit='deg', array=num.array(dec_pgw))
	c4=pyfits.Column(name='PosErr', format='5F', unit='deg ',array=num.array(posErr))
	c5=pyfits.Column(name='CHI_2_VAR', format='5F', unit=' ',array=num.array(chi2))
	x = pyfits.ColDefs([c1,c2,c3,c4,c5])
	tbhdu=pyfits.new_table(x)
	tbhdu.writeto('temp.fits',clobber='yes')
        # add UCD in header
  	hdulist = pyfits.open('temp.fits')
  	head1 = hdulist[1].header
	head1.update('TBUCD2','POS_EQ_RA_MAIN','')
  	head1.update('TBUCD3','POS_EQ_DEC_MAIN','')
  	head1.update('TBUCD4','ERROR','')
	hdulist.writeto(pgwfits,clobber='yes')
	commands.getoutput('rm test.fits')
	os.environ['PGWOUTPUTFITSLIST']=pgwfits
	
if __name__=="__main__":
	pgwfile=sys.argv[1]
	pgw2fits(pgwfile,1)
