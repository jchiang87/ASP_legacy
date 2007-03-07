/**
 * @file EventClusters.cxx
 * @brief JPN and JB's photon clustering algorithm
 * @author J. Chiang <jchiang@slac.stanford.edu>
 *
 * $Header$
 */

#include <cmath>

#include <algorithm>
#include <iostream>

#include "CLHEP/Vector/ThreeVector.h"

#include "astro/SkyDir.h"

#include "pyASP/EventClusters.h"

namespace pyASP {

EventClusters::EventClusters(const std::vector<Event> & events, double radius)
   : m_events(events), m_radius(radius) {}

double EventClusters::logLikeTime(double bg_rate) const {
   std::vector<double> times;
   for (std::vector<Event>::const_iterator event = m_events.begin();
        event != m_events.end(); ++event) {
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

double EventClusters::logLikePosition() const {
   const Event & largest(findLargestCluster());

   astro::SkyDir clusterDir(meanDir(largest));

   double logLike(0);
   for (std::vector<Event>::const_iterator event(m_events.begin()); 
        event != m_events.end(); ++event) {
      double sep(event->dir().difference(clusterDir));
      logLike += std::log(1 - std::cos(sep));
   }
   return logLike;
}

astro::SkyDir EventClusters::meanDir(const Event & event) const {
   double xhat(0);
   double yhat(0);
   double zhat(0);
   size_t nevents(0);
   for (std::vector<Event>::const_iterator evt(m_events.begin());
        evt != m_events.end(); ++evt) {
      if (event.sep(*evt) < m_radius) {
         xhat += evt->dir().dir().x();
         yhat += evt->dir().dir().y();
         zhat += evt->dir().dir().z();
         nevents++;
      }
      xhat /= nevents;
      yhat /= nevents;
      zhat /= nevents;
   }
   return astro::SkyDir(CLHEP::Hep3Vector(xhat, yhat, zhat));
}

const Event & EventClusters::findLargestCluster() const {
   size_t ilargest(0);
   size_t maxSize(clusterSize(m_events.front()));
   for (size_t i(1); i < m_events.size(); i++) {
      size_t currentSize(clusterSize(m_events.at(i)));
      if (currentSize > maxSize) {
         ilargest = i;
         maxSize = currentSize;
      }
   }
   return m_events.at(ilargest);
}

size_t EventClusters::clusterSize(const Event & event) const {
   size_t num(0);
   for (size_t j(0); j < m_events.size(); j++) {
      if (event.sep(m_events.at(j)) < m_radius) {
         num++;
      }
   }
   return num;
}

} // namespace pyASP
