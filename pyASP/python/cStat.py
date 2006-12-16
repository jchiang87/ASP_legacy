"""
@brief Calculate Cash's C-stat.

@author W. Focke <focke@slac.stanford.edu>
"""

import numarray as num

logNFactorial = []
def getLogNFactorial(maxN):
    logNFactorial = num.add.accumulate(num.log(num.arange(maxN)))
    return logNFactorial

def deltaC(counts, model):
    """Calculate contribution to C-stat for each pixel.
    Not done."""
    global logNFactorial
    maxN = num.maximum.reduce(counts)
    if maxN > len(logNFactorial):
        logNFactorial = getLogNFactorial(maxN)
        pass
    deltaC = model * counts * num.log(model) / logNFactorial[counts]
    return deltaC
