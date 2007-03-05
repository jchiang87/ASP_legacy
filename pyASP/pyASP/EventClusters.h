/**
 * @file EventClusters.h
 * @brief JPN and JB's photon clustering algorithm
 * @author J. Chiang <jchiang@slac.stanford.edu>
 *
 * $Header$
 */

#ifndef pyASP_EventClusters_h
#define pyASP_EventClusters_h

#include <map>
#include <vector>

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

private:

   double m_radius;

   std::map<Event, std::vector<double> > m_dists;

};

} // namespace pyASP

#endif // pyASP_EventClusters_h
