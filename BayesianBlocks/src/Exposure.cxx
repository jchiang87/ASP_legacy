/**
 * @file Exposure.cxx
 * @brief LAT effective area, integrated over time bins.
 * @author J. Chiang
 *
 * $Header$
 */

#include "latResponse/IrfsFactory.h"

#include "Likelihood/ScData.h"
#include "Likelihood/Util.h"

#include "BayesianBlocks/Exposure.h"

Exposure::Exposure(const std::string & scDataFile,
                   const std::vector<double> & timeBoundaries,
                   double ra, double dec) 
   : m_timeBoundaries(timeBoundaries) {

   int scHdu(2);
   std::vector<std::string> scFiles;
   Likelihood::Util::resolve_fits_files(scDataFile, scFiles)
   std::vector<std::string>::const_iterator scIt = scFiles.begin();
   for ( ; scIt != scFiles.end(); scIt++) {
      Likelihood::Util::file_ok(*scIt);
      Likelihood::ScData::readData(*scIt, scHdu);
   }

   astro::SkyDir srcDir(ra, dec);

   long numIntervals = m_timeBoundaries - 1;
   m_exposureValues.resize(numIntervals);
   for (unsigned int i = 0; i < numIntervals; i++) {
      m_exposureValues[i] = 0;
      std::pair<double, double> wholeInterval;
      wholeInterval.first = m_timeBoundaries[i];
      wholeInterval.second = m_timeBoundaries[i+1];
      std::pair<ScData::Iterator, ScData::Iterator> scData
         = ScData::bracketInterval(wholeInterval);
      for (ScData::Iterator it = scData.first; 
           it != (scData.second-1); ++it) {
         std::pair<double, double> thisInterval;
         thisInterval.first = it->time;
         thisInterval.second = (it+1)->time;
         if (PointSource::overlapInterval(wholeInterval, thisInterval)) {
            m_exposureValues[i] += thisInterval.first

      }
   }
}
   
