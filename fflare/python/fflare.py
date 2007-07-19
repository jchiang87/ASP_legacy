#!/usr/bin/env python

import readFT,eqtogal
import sys,numpy #pylab
import math

d2r=.01745
sec2day=1./(24.*3600.)
sec2hour=1./3600.

def angdist(ra1,dec1,ra2,dec2):

	co= cos(dec1*.01745)*cos(dec2*.01745)*cos((ra1-ra2)*.01745)+sin(dec1*.01745)*sin(dec2*.01745)
	return acos(co)/0.01745

def getLC(dat,x1,y1,x2,y2):
	nevt=len(dat[0])
	#print x1,y1,x2,y2
	t=[]
	for i in range(0,nevt):
		if (dat[2][i]>=x1 and dat[2][i]<x2) and (dat[3][i]>=y1 and dat[3][i]<y2):
			t.append((dat[0][i]-dat[0][0])/3600.)
	
	return t

def getCount(dat,x1,y1,x2,y2):
	nevt=len(dat[0])
	#print x1,y1,x2,y2
	t=0
	for i in range(0,nevt):
		if (dat[2][i]>=x1 and dat[2][i]<x2) and (dat[3][i]>=y1 and dat[3][i]<y2):
			t+=1
	
	return t

def ave(a):
	if len(a)>1.:
		return sum(a)/len(a)
	else:
		return 0.

def stdev(a):
	mea=ave(a)
	if mea==0:
		return 0.
	som=0.
	for i in range(0,len(a)):
		som+=(a[i]-mea)*(a[i]-mea)
	h=som/(len(a)-1)
		
	return math.sqrt(h)

def chi2(a):
	mea=ave(a)
	if mea==0:
		return 0.
	som=0.
	for i in range(0,len(a)):
		som+=(a[i]-mea)*(a[i]-mea)/float(mea)
	return som/(float(len(a))-1.)
	
def aitoff(l,b,l0,b0,scale):
	l=l*d2r
	b=b*d2r
	l0=l0*d2r
	b0=b0*d2r
	rho=math.acos(math.cos((b-b0)/2.)*math.cos((l-l0)/2.))
	theta=math.asin(math.cos((b-b0)/2.)*math.sin((l-l0)/2.)/math.sin(rho))
	x= (-4.*scale/d2r)*math.sin(rho/2.)*math.sin(theta)
	if (b-b0)<0:
		y=(2.*scale/d2r)*math.sin(rho/2.)*math.cos(theta)
	else:
		y=(-2.*scale/d2r)*math.sin(rho/2.)*math.cos(theta)
	return x,y

if len(sys.argv)>4:
	evt=readFT.ReadFT1(sys.argv[1])
	ene=evt.GetEnergy()
	time=evt.GetTime()
	ra=evt.GetRa()
	dec=evt.GetDec()
	dat=[time,ene,ra,dec]
	tstart,tstop,tot=evt.GetTotalTime()
	tot*=3600.
	ramin=min(ra)
	ramax=max(ra)
	decmin=min(dec)
	decmax=max(dec)
	#l0=float(sys.argv[4])
	#b0=float(sys.argv[5])
	dx=(ramax-ramin)
	dy=(decmax-decmin)
	chimin=float(sys.argv[4])
	step=float(sys.argv[2])
	tb=int(sys.argv[3])
	nx=int(dx/step+0.5)
	ny=int(dy/step+0.5)
	mappa=numpy.zeros([ny,nx])
	chi=numpy.zeros([ny,nx])
	nlc=nx*ny
	nt=tb
	lc=numpy.zeros([ny,nx,tb])
	map1=numpy.zeros([ny,nx])
	print nx,ny
	print tstart,tstop,tot*sec2hour,(tot/tb)*sec2day
	i=nx-1
	j=ny-1
	np=len(dat[0])
	#print l0,b0,
	for n in range(0,np):
		"""x,y=aitoff(ra[n],dec[n],l0,b0,1./step)
		i=int(x+nx/2-0.5)
		j=int(y+ny/2-0.5)
		mappa[j][i]+=1."""
		l,b=eqtogal.eq_to_gal(ra[n],dec[n])
		if abs(b)>5.:
			i= (nx-1)-int((nx-1)*((ra[n]-ramin)/dx)+0.5)
			j= (ny-1)-int((ny-1)*((dec[n]-decmin)/dy)+0.5)
			k= int((nt-1)*((time[n]-tstart)/(tot))+0.5)
			mappa[j][i]+=1.
			lc[j][i][k]+=1.
	medmap=numpy.mean(numpy.mean(mappa))
	print medmap
	#pylab.subplot(211)
	"""pylab.grid('on')
	pylab.imshow(mappa,interpolation='nearest',extent=[ramax,ramin,decmin,decmax])
	pylab.xlabel('RA (deg)')
	pylab.ylabel('DEC (deg)')
	pylab.title(sys.argv[1])"""
	#pylab.colorbar()
	#print sum(sum(mappa))
	sim=[]
	idi=[]
	for j in range(ny-1,0,-1):
		for i in range(nx-1,0,-1):
			if mappa[j][i]>0:
				sim.append(sum(lc[j][i]))
				idi.append(j+i*ny)
	mmed=numpy.mean(sim)
	mst=numpy.std(sim)
	for j in range(ny-1,0,-1):
		for i in range(nx-1,0,-1):
			if mappa[j][i]>0:
				c=chi2(lc[j][i])
				if c>chimin and (sum(lc[j][i])/5.)>=nt:
					chi[j][i]=c
				#print ramin+i*step-step/2.,decmin+j*step-step/2.,c
	nv=0
	fx=[]
	fy=[]
	box=2 #int(sys.argv[7])
	for j in range(ny-box,box-1,-1):
		for i in range(nx-box,box-1,-1):
			pix=chi[j][i]
			if pix>0.:
				bb=1
				for k in range(j+box-1,j-box-1,-1):
					for l in range(i+box-1,i-box-1,-1):
						if bb==1:
							nei=chi[k][l]
							if nei>pix:
								bb=0
							else:
								if nei==pix:
									if((k!=j) or (l!=i)):
										if (k >= j and l>=i) or (k>j and l<i):
											bb=0
				if bb==1:
					print nv,("%5.2f %5.2f %5.2f" % (ramax-i*step-step/2.,decmax-j*step-step/2.,chi[j][i])),lc[j][i]
					fx.append(ramax-i*step-step/2.)
					fy.append(decmax-j*step-step/2.)
					nv+=1
		
				
	
	f1=open('vsourceh.reg',"w")
	f=open('vsource.reg',"w")
	for i in range(0,len(fx)):
		l,b=eqtogal.eq_to_gal(fx[i],fy[i])
		f1.write("%f %f\n" % (fx[i],fy[i]))
		if abs(b)>5.:
			f.write("%f %f\n" % (fx[i],fy[i]))
	f.close()
	f1.close()
	
	"""pylab.plot(fx,fy,'r+',ms=15)
	pylab.xlim(ramax,ramin)
	pylab.ylim(decmin,decmax)
	for i in range(0,len(fx)):
		s=("%d" % i)
		pylab.text(fx[i],fy[i]+step/2,s)
	pylab.figure()
	#pylab.subplot(212)
	pylab.grid('on')
	pylab.imshow(chi,interpolation='nearest',extent=[ramax,ramin,decmin,decmax])
	pylab.plot(fx,fy,'w+',ms=15)
	pylab.xlim(ramax,ramin)
	pylab.ylim(decmin,decmax)
	pylab.xlabel('RA (deg)')
	pylab.ylabel('DEC (deg)')
	pylab.title('reduced-chi^2 map')
	#pylab.colorbar()
	#pylab.contour(lc)
	#pylab.figure()
	#pylab.plot(idi,sim,'o',ms=3)
	#pylab.xlim(0,nx*ny)
	#pylab.hist(mappa)
	pylab.show()"""
