import sys
import AspHealPix
from GtApp import GtApp

hp = AspHealPix.Healpix(16, HealPix.Healpix.NESTED, HealPix.SkyDir.GALACTIC)

def makeLivetimeCube(ft1File,ft2File) :
    gtltcube = GtApp('gtltcube')
    gtltcube['evfile'] = ft1File
    gtltcube['scfile'] = ft2File
    gtltcube['outfile'] = 'toto_expCube.fits'
    gtltcube.run()
    return gtltcube['outfile']

def makeHealCountMap(ft1File,cut):
    cmap = AspHealPix.CountsArray(hp)
    cmap.binCounts(ft1File, cut)
    cmap.write('toto_count.fits')
    return cmap

def makeHealExpMap(ltcube):
    emap = AspHealPix.ExposureArray(hp)
    emap.computeExposure('DC2', ltcube)
    emap.write('toto_exp.fits')

    
if __name__=="__main__" :
    cutarg=False
    count=1
    thisfile = sys.argv[0]
    ft1File=None
    ft2FIle=None
    ltcube=None
    if 'ipython' in sys.argv[0]:
        thisfile=sys.argv[1]
        count=2
    #healpix count map
    try :
        ft1File = sys.argv[count]
        cut=""
        try :
            cut = sys.argv[count+1].split('.')[-1]
            if cut.split('.')[-1]!="fits":
            #assume second argument is a cut in FT1
                count+=1
            else :
                cut =""
        except :
            cut = ""
        print "making healpix count map with ft1 %s and cut %s"%(ft1File,cut)
        cmap = makeHealCountMap(ft1File,cut)
    except : 
        print "usage : "+thisfile.split('/')[-1]+" <Ft1 file> [FT1 cut, FT2 file]"
    # healpix exp map
    if len(sys.argv)==count+2 :
        ft2File=sys.argv[count+1]
        print "making livetime cube with ft1 %s and ft2 %s"%(ft1File,ft2File)
        ltcube = makeLivetimeCube(ft1File,ft2File)
        print "making healpix exposure map with livetime cube %s"%(ltcube)
        emap = makeHealExpMap(ltcube)
    print "done"
    
