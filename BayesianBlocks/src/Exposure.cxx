/**
 * @file Exposure.cxx
 * @brief LAT effective area, integrated over time bins.
 * @author J. Chiang
 *
 * $Header$
 */

#include <stdexcept>
#include <utility>

#include "latResponse/IrfsFactory.h"

#include "Likelihood/PointSource.h"
#include "Likelihood/ScData.h"
#include "Likelihood/Util.h"

#include "BayesianBlocks/Exposure.h"

Exposure::Exposure(const std::string & scDataFile,
                   const std::vector<double> & timeBoundaries,
                   double ra, double dec) 
   : m_timeBoundaries(timeBoundaries), m_irfs_front(0), m_irfs_back(0), 
     m_energy(300.) {
   m_srcDir = astro::SkyDir(ra, dec);
   m_irfs_front = latResponse::irfsFactory().create("DC1::Front");
   m_irfs_back = latResponse::irfsFactory().create("DC1::Back");
   readScData(scDataFile);
   integrateExposure();
}

Exposure::~Exposure() throw() {
   delete m_irfs_front;
   delete m_irfs_back;
}
   
double Exposure::value(double time) const {
   int indx = std::upper_bound(m_timeBoundaries.begin(), 
                               m_timeBoundaries.end(), time) 
      - m_timeBoundaries.begin() - 1;
   return m_exposureValues[indx];
}

void Exposure::readScData(const std::string & scDataFile) {
   int scHdu(2);
   std::vector<std::string> scFiles;
   Likelihood::Util::resolve_fits_files(scDataFile, scFiles);
   std::vector<std::string>::const_iterator scIt = scFiles.begin();
   bool clear(true);
   for ( ; scIt != scFiles.end(); scIt++) {
      Likelihood::Util::file_ok(*scIt);
      Likelihood::ScData::readData(*scIt, scHdu, clear);
      clear = false;
   }
}

void Exposure::integrateExposure() {
   unsigned int numIntervals = m_timeBoundaries.size() - 1;
   m_exposureValues.resize(numIntervals);
   for (unsigned int i = 0; i < numIntervals; i++) {
      m_exposureValues[i] = 0;
      std::pair<double, double> wholeInterval;
      wholeInterval.first = m_timeBoundaries[i];
      wholeInterval.second = m_timeBoundaries[i+1];
      std::pair<Likelihood::ScData::Iterator, 
         Likelihood::ScData::Iterator> scData;
      Likelihood::ScData::Iterator firstIt
         = Likelihood::ScData::instance()->vec.begin();
      Likelihood::ScData::Iterator lastIt
         = Likelihood::ScData::instance()->vec.end() - 1;
      try {
         scData = Likelihood::ScData::bracketInterval(wholeInterval);
         if (scData.first - firstIt < 0) scData.first = firstIt;
         if (scData.second - firstIt > lastIt - firstIt) 
            scData.second = lastIt;
      } catch (std::out_of_range &eObj) { // use brute force
         scData = std::make_pair(firstIt, lastIt);
      }
      for (Likelihood::ScData::Iterator it = scData.first; 
           it != (scData.second-1); ++it) {
         std::pair<double, double> thisInterval;
         thisInterval.first = it->time;
         thisInterval.second = (it+1)->time;
         if (Likelihood::PointSource::overlapInterval(wholeInterval, 
                                                      thisInterval)) {
            m_exposureValues[i] += (effArea(thisInterval.first) 
                                    + effArea(thisInterval.second))/2.
               *(thisInterval.second - thisInterval.first);
         }
      }
   }
}

double Exposure::effArea(double time) const {
   Likelihood::ScData * scData = Likelihood::ScData::instance();
   astro::SkyDir zAxis = scData->zAxis(time);
   astro::SkyDir xAxis = scData->xAxis(time);
   
   latResponse::IAeff * aeff_front = m_irfs_front->aeff();
   latResponse::IAeff * aeff_back = m_irfs_back->aeff();
   return aeff_front->value(m_energy, m_srcDir, zAxis, xAxis)
      + aeff_back->value(m_energy, m_srcDir, zAxis, xAxis);
}
