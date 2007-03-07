/**
 * @file EventClusters.cxx
 * @brief JPN and JB's photon clustering algorithm
 * @author J. Chiang <jchiang@slac.stanford.edu>
 *
 * $Header$
 */

#include "CLHEP/Vector/ThreeVector.h"

#include "pyASP/EventClusters.h"

namespace pyASP {

EventClusters::EventClusters(const std::vector<Event> & events, double radius)
   : m_events(events), m_radius(radius) {}

double logLikeTime(double bg_rate) const {
   std::vector<double> times;
   for (std::vector<Event>::const_iterator event = m_events.begin();
        event != m_dist.end(); ++event) {
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
   typedef std::vector<Event>::const_iterator EventIterator_t;

// Find the largest cluster
   EventIterator_t event(m_events.begin());
   const Event & largest(*event);
   size_t maxSize(clusterSize(*event));
   for ( ; event != m_events.end(); ++event) {
      size_t currentSize(clusterSize(*event));
      if (currentSize > maxSize) {
         largest = *event;
         maxSize = currentSize;
      }
   }

// Compute the mean direction of this cluster.
   double xhat(0);
   double yhat(0);
   double zhat(0);
   size_t nevents(0);
   for (EventIterator_t event(m_events.begin());
        event != m_events.end(); ++event) {
      if (largest.sep(event->first) < m_radius) {
         xhat += event->first.dir().dir().x();
         yhat += event->first.dir().dir().y();
         zhat += event->first.dir().dir().z();
         nevents++;
      }
      xhat /= nevents;
      yhat /= nevents;
      zhat /= nevents;
   }
   astro::SkyDir meanDir(CLHEP::Hep3Vector(xhat, yhat, zhat));

// Compute the log-likelihood
   double logLike(0);
   for (EventIterator_t event(m_events.begin()); 
        event != m_events.end(); ++event) {
      double sep(event->dir().difference(meanDir));
      logLike += std::log(1 - std::cos(sep));
   }
   return logLike;
}

size_t clusterSize(const Event & event) const {
   size_t num(0);
   for (size_t j(0); j < m_events.size(); j++) {
      if (event.sep(m_events.at(j)) < m_radius) {
         num++;
      }
   }
   return num;
}

} // namespace pyASP
