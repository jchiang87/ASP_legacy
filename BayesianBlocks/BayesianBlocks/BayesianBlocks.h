/**
 * @file BayesianBlocks.h
 * @author J. Chiang
 *
 * $Header$
 */

#ifndef _BayesianBlocks_h
#define _BayesianBlocks_h

#include <deque>
#include <map>
#include <string>
#include <utility>
#include <vector>

/**
 * @class BayesianBlocks
 * @brief Implementation of 1D Bayesian Blocks nominally for
 * time-tagged event data, but should be applicable to spectra,
 * substituting energies for event times.
 *
 * @author J. Chiang
 *
 * $Header$
 */

class BayesianBlocks {
   
public:
  
   BayesianBlocks(const std::vector<double> & eventTimes, double ncpPrior=1.);
   
//    BayesianBlocks(const std::string & filename, double ncpPrior=1.);

   ~BayesianBlocks() throw() {}

   void computeLightCurve(std::vector<double> & tmins,
                          std::vector<double> & tmaxs,
                          std::vector<double> & numEvents);

   void setNcpPrior(double ncpPrior) {m_ncpPrior = ncpPrior;}

   double ncpPrior() const {return m_ncpPrior;}

   static double gammln(double x);

   void createCells();

   void globalOpt();

   double blockCost(unsigned int imin, unsigned int imax) const;

   double blockSize(unsigned int imin, unsigned int imax) const;

   double blockContent(unsigned int imin, unsigned int imax) const;

private:

   std::vector<double> m_eventTimes;

   double m_ncpPrior;

   std::vector< std::pair<double, double> > m_cells;

   std::deque<unsigned int> m_changePoints;

};

#endif //_BayesianBlocks_h
