import random
import numarray as num
from BayesianBlocks import BayesianBlocks, DoubleVector

class Distribution(object):
    def generateEvents(self, nevents=1000):
        events = []
        for i in xrange(nevents):
            events.append(self.draw())
        return events

class PowerLawSpectrum(Distribution):
    def __init__(self, gamma=2, emin=20., emax=2e5):
        self.gamma = gamma
        self.emin = emin
        self.emax = emax
        self.eminGam = emin**(1. - gamma)
        self.emaxGam = emax**(1. - gamma)
    def draw(self):
        xi = random.random()
        ee = (xi*(self.eminGam - self.emaxGam)
              + self.emaxGam)**(1./(1. - self.gamma))
        return ee
    def __call__(self, ee):
        return ee**(-self.gamma)
    
class GaussianLine(Distribution):
    def __init__(self, mean, sigma):
        self.mean = mean
        self.sigma = sigma
    def draw(self):
        return random.gauss(self.mean, self.sigma)
    def __call__(self, ee):
        return (num.exp(-((ee-self.mean)/2./self.sigma)**2)
                /num.sqrt(2.)/self.sigma)

def detrend(events, func):
    my_events = []
    for evt in events:
        my_events.append(evt*func(evt))
    return my_events

if __name__ == "__main__":
    import string, sys
    import hippoplotter as plot
    gamma = 2
    pl = PowerLawSpectrum(gamma=gamma)
    events = pl.generateEvents(1000)
    gauss = GaussianLine(300., 30.)
    events.extend(gauss.generateEvents(40))

    plot.clear()
    spectrum = plot.histogram(events, 'energy', xlog=1, ylog=1)

    detrended = num.array(detrend(events, pl))
    plot.histogram(detrended, 'detrended energy', ylog=1)
    
    dt = []
    for i in xrange(len(detrended)-1):
        dt.append(abs(detrended[i+1] - detrended[i]))
    detrended /= min(dt)/2.
    detrended = DoubleVector(list(detrended))
    
    if len(sys.argv) == 2:
        ncpPrior = string.atof(sys.argv[1])
    else:
        ncpPrior = 2.

    my_blocks = BayesianBlocks(detrended, ncpPrior)
    tmins = DoubleVector()
    tmaxs = DoubleVector()
    numEvents = DoubleVector()
    my_blocks.computeLightCurve(tmins, tmaxs, numEvents)
    
    energies = []
    dens = []
    for tmin, tmax, numEvts in zip(tmins, tmaxs, numEvents):
        my_dens = numEvts/(tmax - tmin)/(min(dt)/2.)
        if (tmin > 0):
            energies.append(tmin)
            dens.append(my_dens)
        energies.append(tmax)
        dens.append(my_dens)

    energies = num.array(energies)*min(dt)/2.
    plot.scatter(energies, dens, oplot=1, pointRep='Line', color='red')
    
    plot.canvas.selectDisplay(spectrum)

    jacobian = abs(pl(energies) + energies*(-gamma*energies**(-(gamma+1.))))
    dens = num.array(dens)/jacobian
    energies = energies**(1./(1. - gamma))
    plot.scatter(energies, dens, oplot=1, pointRep='Line', color='red')

