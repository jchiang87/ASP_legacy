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

#include "pyASP/Event.h"

namespace astro {
   class SkyDir;
}

namespace pyASP {

/**
 * @class EventClusters
 */

class EventClusters {

public:

   EventClusters(const std::vector<Event> & events,
                 double radius=17);

   virtual ~EventClusters() {}

   virtual double logLikeTime(double bg_rate=0) const;

   virtual double logLikePosition() const;

   virtual astro::SkyDir clusterDir(double radius=5) const {
      return meanDir(findLargestCluster(radius), radius);
   }

protected:

   std::vector<Event> m_events;

private:

   double m_radius;

   const Event & findLargestCluster(double radius=0) const;

   astro::SkyDir meanDir(const Event & event, double radius=0) const;

   size_t clusterSize(const Event & event, double radius=0) const;

};

} // namespace pyASP

#endif // pyASP_EventClusters_h
