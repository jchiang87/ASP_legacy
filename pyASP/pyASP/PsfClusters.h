/**
 * @file PsfClusters.h
 * @brief Photon cluster detection algorithm using the PSF
 * @author J. Chiang <jchiang@slac.stanford.edu>
 *
 * $Header$
 */

#ifndef pyASP_PsfClusters_h
#define pyASP_PsfClusters_h

#include "pyASP/EventClusters.h"

namespace irfInterface {
   class IPsf;
}

namespace pyASP {

class ScData;

/**
 * @class PsfClusters
 */

class PsfClusters : public EventClusters {

public:

   PsfClusters(const std::vector<Event> & events, 
               const ScData & scData,
               const std::string & irfs="DC2");

   virtual ~PsfClusters() {}

   virtual double logLikePosition() const {
      return m_logLikePosition;
   }

   virtual astro::SkyDir clusterDir() const {
      return m_clusterDir;
   }

private:

   const ScData & m_scData;
   double m_logLikePosition;
   astro::SkyDir m_clusterDir;

   std::vector<irfInterface::IPsf *> m_psfs;

   const Event & findLargestCluster(double & logLike) const;
   void computePsfWts(const Event & evt, std::vector<double> & wts) const;
   double eventLogLike(const Event & evt) const;
   double eventLogLike(const std::vector<double> & wts) const;

   void loadIrfs(const std::string & irfs);

};

} // namespace pyASP

#endif // pyASP_PsfClusters_h
