/**
 * @file BayesianBlocks.cxx
 * @brief 1D Bayesian blocks
 * @author J. Chiang
 *
 * $Header$
 */

#include <cmath>

#include "BayesianBlocks/BayesianBlocks.h"

BayesianBlocks::BayesianBlocks(const std::vector<double> & eventTimes, 
                               double ncpPrior) : m_eventTimes(eventTimes),
                                                  m_ncpPrior(ncpPrior) {
   std::stable_sort(m_eventTimes.begin(), m_eventTimes.end());
   createCells();
}

void BayesianBlocks::computeLightCurve(std::vector<double> & tmins,
                                       std::vector<double> & tmaxs,
                                       std::vector<double> & numEvents) {
   globalOpt();
   tmins.clear();
   tmaxs.clear();
   numEvents.clear();
   for (unsigned int i = 1; i < m_changePoints.size(); i++) {
      unsigned int imin = m_changePoints[i-1];
      unsigned int imax = m_changePoints[i];
      tmins.push_back(m_cells[imin].first);
      tmaxs.push_back(m_cells[imax].second);
      numEvents.push_back(blockContent(imin, imax));
   }
}

void BayesianBlocks::getChangePoints(std::vector<int> & changePoints) const {
   changePoints.resize(m_changePoints.size());
   std::copy(m_changePoints.begin(), m_changePoints.end(), 
             changePoints.begin());
}

void BayesianBlocks::globalOpt() {
   std::vector<double> opt;
   opt.push_back(blockCost(0, 0) - m_ncpPrior);
   std::vector<unsigned int> last;
   last.push_back(0);
   unsigned int npts = m_eventTimes.size();
   for (unsigned int nn = 1; nn < npts; nn++) {
      double max_opt = blockCost(0, nn) - m_ncpPrior;
      unsigned int jmax(0);
      for (unsigned int j = 1; j < nn+1; j++) {
         double my_opt = opt[j-1] + blockCost(j, nn) - m_ncpPrior;
         if (my_opt > max_opt) {
            max_opt = my_opt;
            jmax = j;
         }
      }
      opt.push_back(max_opt);
      last.push_back(jmax);
   }
   m_changePoints.clear();
   unsigned int indx = last[npts-1];
   while (indx > 0) {
      m_changePoints.push_front(indx);
      indx = last[indx-1];
   }
   m_changePoints.push_front(0);
   m_changePoints.push_back(npts-1);
}

void BayesianBlocks::createCells() {
   std::vector<double> cell_boundaries;
   unsigned int npts = m_eventTimes.size();
   cell_boundaries.push_back((3.*m_eventTimes[0] - m_eventTimes[1])/2.);
   for (unsigned int i = 1; i < npts; i++) {
      cell_boundaries.push_back((m_eventTimes[i-1] + m_eventTimes[i])/2.);
   }
   cell_boundaries.push_back((3.*m_eventTimes[npts-1] 
                              - m_eventTimes[npts-2])/2.);
   m_cells.clear();
   for (unsigned int i = 0; i < npts; i++) {
      m_cells.push_back(std::make_pair(cell_boundaries[i], 
                                       cell_boundaries[i+1]));
   }
}

double BayesianBlocks::blockCost(unsigned int imin, unsigned int imax) const {
   double size = blockSize(imin, imax);
   double content = blockContent(imin, imax);
   double arg = size - content;
   if (arg > 0) {
      double my_cost = gammln(content + 1.) + gammln(arg + 1.) 
         - gammln(size + 2.);
      return my_cost;
   }
   return -log(size);
}

double BayesianBlocks::blockSize(unsigned int imin, unsigned int imax) const {
   return m_cells[imax].second - m_cells[imin].first;
}

double BayesianBlocks::blockContent(unsigned int imin, 
                                    unsigned int imax) const {
   return imax - imin + 1.;
}

double BayesianBlocks::gammln(double xx) {
   static double cof[6] = {76.18009172947146, -86.50532032941677,
                           24.01409824083091, -1.231739572450155,
                           0.1208650973866179e-2, -0.5395239384953e-5};
   double y = xx;
   double x = xx;
   double tmp = x + 5.5;
   tmp -= (x + 0.5)*log(tmp);
   double ser = 1.000000000190015;
   for (int j = 0; j < 6; j++) {
      ser += cof[j]/++y;
   }
   return -tmp + log(2.5066282746310005*ser/x);
}
