"""
@brief Run this at the end of the afterglow task to clean up everything except
for the GCN Notice draft and *.png files.

@author J. Chiang <jchiang@slac.stanford.edu>
"""
#
# $Header$
#

import os
import glob

os.chdir(os.environ['GRBROOTDIR'])

files = glob.glob('*')

for item in files:
    if item.find('.png') > 0 or item.find('Notice.txt') > 0:
        continue
    os.remove(item)
