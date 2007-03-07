/**
 * @file EventClusters.h
 * @brief JPN and JB's photon clustering algorithm
 * @author J. Chiang <jchiang@slac.stanford.edu>
 *
 * $Header$
 */

#ifndef pyASP_EventClusters_h
#define pyASP_EventClusters_h

#include <vector>

namespace astro {
   class SkyDir;
}

#include "pyASP/Event.h"

namespace pyASP {

/**
 * @class EventClusters
 */

class EventClusters {

public:

   EventClusters(const std::vector<Event> & events,
                 double radius=17);

   double logLikeTime(double bg_rate=0) const;

   double logLikePosition() const;

   astro::SkyDir clusterDir(double radius=5) const {
      return meanDir(findLargestCluster(radius), radius);
   }

private:

   std::vector<Event> m_events;

   double m_radius;

   const Event & findLargestCluster(double radius=0) const;

   astro::SkyDir meanDir(const Event & event, double radius=0) const;

   size_t clusterSize(const Event & event, double radius=0) const;

};

} // namespace pyASP

#endif // pyASP_EventClusters_h
