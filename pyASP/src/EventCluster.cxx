/**
 * @file EventCluster.cxx
 * @brief JPN and JB's photon clustering algorithm
 * @author J. Chiang <jchiang@slac.stanford.edu>
 *
 * $Header$
 */

#include "pyASP/EventClusters.h"

//namespace pyASP {

EventClusters::EventClusters(const std::vector<Event> & events, double radius)
   : m_radius(radius) {
   std::vector<Event>::const_iterator event(events.begin());
   for ( ; event != events.end(); ++event) {
      m_dists[*event] = std::vector<double>;
      for (size_t j(0); j < events.size(); j++) {
         m_dists[*event].push_back(event->sep(events.at(j)));
      }
   }
}

double logLikeTime(double bg_rate) const {
   std::vector<double> times;
   std::map<Event, std::vector<double> >::const_iterator event;
   for (event = m_dists.begin(); event != m_dist.end(); ++event) {
      times.push_back(event->time());
   }

   std::stable_sort(times.begin(), times.end());
   if (bg_rate == 0) {
      bg_rate = times.size()/(times.back() - times.front());
   }
   double logLike(0);
   for (size_t j(1); j < times.size(); j++) {
      double xval(bg_rate*(times.at(j) - times.at(j-1)));
      logLike += std::log(1. - std::exp(-xval));
   }
   return logLike;
}

double EventCluster::logLikePosition() const {

   typedef std::map<Event, std::vector<double> >::const_iterator 
      EventIterator_t;

// Find the largest cluster
   EventIterator event(m_dists.begin());
   const Event & largest(event->first);
   size_t maxSize(clusterSize(event->second));
   for ( ; event != m_dists.end(); ++event) {
      size_t currentSize(clusterSize(event->second));
      if (currentSize > maxSize) {
         largest = event->first;
         maxSize = currentSize;
      }
   }

// Compute the mean dir of this cluster (this needs to be fixed since
// it will fail if the events wrap around ra=360).
   double ra(0);
   double dec(0);
   size_t nevents(0);
   for (EventIterator event(m_dists.begin()); event != m_dists.end();
        ++event) {
      if (largest.sep(event->first) < m_radius) {
         ra += event->first.dir().ra();
         dec += event->first.dir().dec();
         nevents++;
      }
   }
   astro::SkyDir meanDir(ra/nevents, dec/nevents);

// Compute the log-likelihood
   double logLike(0);
   for (EventIterator event(m_dists.begin()); event != m_dists.end();
        ++event) {
      double sep(event->first.dir().difference(meanDir));
      logLike += std::log(1 - std::cos(sep));
   }
   return logLike;
}

size_t clusterSize(const std::vector<double> & dists) const {
   size_t num(0);
   for (size_t j(0); j < dists.size(); j++) {
      if (dists.at(j) < m_radius) {
         num++;
      }
   }
   return num;
}

} // namespace pyASP
