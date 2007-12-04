import os,sys

os.environ['HOME'] = os.environ['output_dir']

from pylab import *
import numarray.fft as nff
import numarray as num
import pyfits

def ConvFilter(image1, image2, pad=True, MinPad=True, Smooth=False):

	r1,c1  = image1.shape
	r2,c2  = image2.shape

	#Padding to the end. Inserting to the middle would
	#break up the resulted image.
	#The window filled within:

	if MinPad:
		x1 = r1 + r2 -1
		y1 = c1 + c2 -1
	else :
		x1 = 2 * max(r1,r2)
		y1 = 2 * max(c1,c2)

	Fft = nff.fft2d
	iFft = nff.inverse_fft2d

	if pad:
		#round up to the next power of two:
		px2 = int(num.log(x1)/num.log(2.0) + 1.0)
		py2 = int(num.log(y1)/num.log(2.0) + 1.0)
		xOrig = x1
		yOrig = y1
		x1 = 2**px2
		y1 = 2**py2

	if Smooth:
		fftimage = Fft(image1, s=(x1,y1)) * Fft(image2,s=(x1,y1))
	else :
		fftimage = Fft(image1, s=(x1,y1)) * \
				Fft(image2[::-1,::-1],s=(x1,y1))
		Fft(image2, s=(x1,y1)).conjugate()*indx

	if pad:

		return ((iFft(fftimage))[:xOrig,:yOrig]).real

	else :
		#return abs(iFft(fftimage))
		return (iFft(fftimage)).real

def GaussKernel(r=10, width=0, norm=False):

	size = 2*r+1

	if width == 0:
		width = r

	const = -4.0*num.log(2.0)/(width**2)
	kernelcore = num.indices((size,size))
	
	kernel = num.exp(const*((kernelcore[0]-r)**2 +(kernelcore[1]-r)**2))

	if norm:
		#Normalize to 1:
		kernel = kernel/kernel.sum()
	
	return kernel


def creaXimageGif(nomefile):

 	#f=open("temp.xco","w")
	#outgif=nomefile.replace('.fits','_.gif')
 	#f.write("read_image %s\nchat 0\ncpd %s/gif\ncct/set vt1\nsmo/real/sigma=1.2\ndisp/lin/nof\nexit\n" % (nomefile,outgif))
	#f.close()
	im,hdr=pyfits.getdata(nomefile,header='True')
	im.shape=(hdr['NAXIS2'],hdr['NAXIS1']) 
	kernel=GaussKernel(10,2.5,norm=True)
	out=ConvFilter(im, kernel,Smooth=True)
	out=out[12:372,12:732]
	w,h=im.shape
	figure(figsize=(h/72, w/72),dpi=72)
	axes((0,0,1,1))
	axis('off')
	imshow(log(out+1),cmap=cm.jet,origin='lower',interpolation='bilinear')
	outgif1=nomefile.replace('.fits','.png')
	savefig(outgif1,dpi=72)
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


