/**
   @page Results Using Bayesian Blocks to Find Spectral Features and AGN Flares in LAT Data

   @section intro Introduction
                  
   As part of an effort to understand the algorithm, I implemented
   Jeff Scargle's Bayesian Blocks algorithm for 1D data.  The main
   reference that I used is an article by <a
   href="http://trotsky.arc.nasa.gov/~jeffrey/paper_1d.pdf">Jackson,
   Scargle, et al. 2003</a>.  I also consulted Jeff's longer <a
   href="http://trotsky.arc.nasa.gov/~jeffrey/global.ps">Paper VI</a>
   for the MatLab implementation, and Mike Nowak's <a
   href="http://space.mit.edu/CXC/analysis/SITAR/bb_examp.html">SITAR
   pages</a> for his S-Lang/ISIS version.

   I won't describe the details of the underlying algorithm here,
   since it is well explained in the above references.  However, I am
   using it in a context that differs in an important way from the
   usual applications.  The basic method is intended to find the
   optimal partition of the interval such that the data in the
   interval can be described by a "piece-wise constant function",
   i.e., that the density of events (or counts) in the interval can be
   modeled as a series of step functions.  Here is an example:

   @image html BB_example.png

   Here 1000 events were drawn from the differential distribution
   \f[
   \frac{dN}{d\phi}\mbox{~}{\stackrel{d}{\sim}}\mbox{~}1 + \sin\phi.
   \f]
   The solid histogram are these data binned into 50 equal-sized bins
   in \f$\phi\f$, and the dashed histogram is the Bayesian Block
   estimate of the underlying distribution.  There are several things
   worth noting about this example:

   


*/

