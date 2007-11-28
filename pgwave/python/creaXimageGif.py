import os,sys
from pylab import *
import pyfits

def creaXimageGif(nomefile):

 	#f=open("temp.xco","w")
	#outgif=nomefile.replace('.fits','_.gif')
 	#f.write("read_image %s\nchat 0\ncpd %s/gif\ncct/set vt1\nsmo/real/sigma=1.2\ndisp/lin/nof\nexit\n" % (nomefile,outgif))
	#f.close()
	im,hdr=pyfits.getdata(nomefile,header='True')
	im.shape=(hdr['NAXIS2'],hdr['NAXIS1']) 
	w,h=im.shape
	figure(figsize=(h/120, w/120),dpi=120)
	axes((0,0,1,1))
	axis('off')
	imshow(log(im+1),cmap=cm.jet,origin='lower')
	outgif1=nomefile.replace('.fits','.png')
	savefig(outgif1)
	outgif=nomefile.replace('.fits','.gif')
	#comando="ximage @temp.xco" 
	#comando1= ("convert %s -crop 575x285+180+165 %s\n" % (outgif,outgif1))
	comando1= ("convert %s %s\n" % (outgif1,outgif))
	#print comando1
	try:
		#os.system(comando)
		os.system(comando1)
		
	except:
		print "@error while trying to create gif"
	
	#os.remove(outgif)	
	
if __name__ == '__main__':
	creaXimageGif(sys.argv[1])


