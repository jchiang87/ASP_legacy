import os
from runpgw import *
from pgw2fits import *
from runsrcid import *

def runPipe():
#	os.chdir(output_dir)
#	infile=os.path.join(os.environ['INPUTFT1DIR'],os.environ['INPUTFT1FILE'])
	runpgw('prime4h.fits')
#	pgw2fits(os.environ['PGWOUTPUTLIST'],1)
#	runsrcid (os.environ['PGWOUTPUTFITSLIST'],0.30)
#	os.system('rm temp.fits')	

