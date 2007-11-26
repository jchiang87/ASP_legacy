import os,sys,subprocess

def creaXimageGif(nomefile):

 	f=open("temp.xco","w")
	outgif=nomefile.replace('.fits','_.gif')
 	f.write("read_image %s\nchat 0\ncpd %s/gif\ncct/set vt1\nsmo/real/sigma=1.2\ndisp/lin/nof\nexit\n" % (nomefile,outgif))
	f.close()
	outgif1=nomefile.replace('.fits','.gif')
	comando="ximage @temp.xco" 
	comando1= ("convert %s -crop 575x285+180+165 %s\n" % (outgif,outgif1))
	print comando1
	try:
		os.system(comando)
		os.system(comando1)
		
	except:
		print "@error while trying to create gif"
	
	os.remove(outgif)	
	
if __name__ == '__main__':
	creaXimageGif(sys.argv[1])


