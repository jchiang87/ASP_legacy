from math import * 
import sys,string

def hms_deg(h,m,s):
	a=(float(h)+float(m)/60.+float(s)/3600.)*15
	return a
	
def dms_deg(d,m,s):
	sign=1
	a=0
	if d[0]=='-':
		sign=-1	
	a=sign*(float(d[1:])+float(m)/60.+float(s)/3600.)
	return a
	
def eq_to_gal(ra,dec):
	a1=62.6*0.01745
	a2=(ra - 282.25)*0.01745
	b=asin(sin(dec*0.01745)*cos(a1)-cos(dec*0.01745)*sin(a2)*sin(a1))

	s1=(sin(dec*0.01745)*sin(a1)+cos(dec*0.01745)*sin(a2)*cos(a1))/cos(b)
	l=asin(s1)/0.0175+32.93
	if l<0.:
		l+=360.
	b=b/0.01745
	return l,b
	
def eq_to_gal1950(ra,dec):
	a1=27.4*0.01745
	a2=(192.25-ra)*0.01745
	a=sin(a2)
	b=cos(a2)*sin(a1)-tan(dec*0.01745)*cos(a1)
	x=atan2(a,b)
	l=303.-x/0.01745

	s1=(sin(dec*0.01745)*sin(a1)+cos(dec*0.01745)*cos(a2)*cos(a1))
	b=asin(s1)/0.01745
	if l<0.:
		l+=360.
	return l,b
	
