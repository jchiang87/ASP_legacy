/**
   @page Results Using Bayesian Blocks to Find Spectral Features and AGN Flares in LAT Data

   @section intro Introduction
                  
   As part of an effort to understand it, I implemented Jeff Scargle's
   Bayesian Blocks algorithm for 1D data.  The main reference that I
   used is the article by <a
   href="http://trotsky.arc.nasa.gov/~jeffrey/paper_1d.pdf">Jackson,
   Scargle, et al. 2003</a>.  I also consulted Jeff's longer <a
   href="http://trotsky.arc.nasa.gov/~jeffrey/global.ps">Paper VI</a>
   for more details and the MatLab implementation, and Mike Nowak's <a
   href="http://space.mit.edu/CXC/analysis/SITAR/bb_examp.html">SITAR
   pages</a> for his S-Lang/ISIS version.  I won't describe the
   underlying algorithm in its entirety here, since it is well
   explained in the above references.  However, I am using it in a
   context that differs in an important way from the usual
   applications, so I will need to cover some of the details.

   The basic method is intended to find the optimal partition of the
   interval such that the data in the interval can be described by a
   "piece-wise constant function", i.e., that the density of events in
   the interval can be modeled as a series of step functions.  For 1D
   Bayesian Blocks, each photon event is characterized by a single
   quantity, such as arrival time or measured energy.  For arrival
   times, the method gives an estimate of the light curve while for
   energies, it gives an estimate of the spectrum.  

   Here are some definitions that will be useful for the following
   discussion:
      
   - The initial partitioning of the interval places each event in
     its own cell.  The boundaries of the cells are given by the
     mid-points between adjacent events.

   - A block is defined as a contiguous group of cells.

   - The content, \f$N\f$, of a block is the number of cells or events
     that it comprises.

   - The size, \f$M\f$, of a block is the sum of its individual cell
     sizes.

   - The ends of each block are referred to as change points, since
     they are the locations at which the rate changes from one
     constant value to another.

   - The cost function for each block is 
     \f[
     \log\Gamma(N + 1) + \log\Gamma(M - N + 1) - \log\Gamma(M + 2) 
         - \log\gamma,
     \f]

     where \f$\Gamma\f$ is the usual gamma-function, \f$\Gamma(x+1) =
     x\Gamma(x)\f$, and the total cost function of the partition is
     the sum of the individual block cost functions.  This is based on
     a Poisson model for the expected number of counts in a block
     given a constant rate.  The last term, \f$\log\gamma\f$,
     describes a prior distribution that prefers a smaller number of
     change points.  Since larger values of \f$\log\gamma\f$ tend to
     produce less structured models, the value of \f$\log\gamma\f$ at
     which a given feature is suppressed can be considered as a
     measure of the "significance" of that feature.

   Here is an example of a Bayesian Blocks analysis

   @image html BB_example_0.png

   For this plot, 200 events were drawn from the differential
   distribution

   \f[
   \frac{dN}{dx} = 

   For this plot, 5000 events were drawn from the differential
   distribution
   \f[
   \frac{dN}{d\phi}\mbox{~}{\stackrel{d}{\sim}}\mbox{~}1 + \sin\phi.
   \f]
   The black histogram are these data binned into 50 equal-sized bins
   in \f$\phi\f$, and the red histogram is the Bayesian Block
   estimate of the underlying distribution.

   Even though this analysis does

*/

