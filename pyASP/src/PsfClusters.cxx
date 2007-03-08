/**
 * @file PsfClusters.cxx
 * @brief Photon cluster detection algorithm using the PSF
 * @author J. Chiang <jchiang@slac.stanford.edu>
 *
 * $Header$
 */

#include "irfInterface/IrfsFactory.h"
#include "irfInterface/IPsf.h"

#include "irfLoader/Loader.h"

#include "pyASP/PsfClusters.h"
#include "pyASP/ScData.h"

namespace pyASP {

PsfClusters::PsfClusters(const std::vector<Event> & events,
                         const ScData & scData,
                         const std::string & irfs) 
   : EventClusters(events), m_scData(scData) {
   loadIrfs(irfs);
   std::vector<double> wts;
   const Event & largest(findLargestCluster(m_logLikePosition));
   computePsfWts(largest, wts);
   double xhat(0);
   double yhat(0);
   double zhat(0);
   for (std::vector<Event>::const_iterator evt(m_events.begin());
        evt != m_events.end(); ++evt) {
      xhat += evt->dir().dir().x();
      yhat += evt->dir().dir().y();
      zhat += evt->dir().dir().z();
   }
   xhat /= m_events.size();
   yhat /= m_events.size();
   zhat /= m_events.size();
   m_clusterDir = astro::SkyDir(CLHEP::Hep3Vector(xhat, yhat, zhat));
}

double PsfClusters::eventLogLike(const Event & evt) const {
   std::vector<double> wts;
   computePsfWts(evt, wts);
   return eventLogLike(wts);
}

double PsfClusters::eventLogLike(const std::vector<double> & wts) const {
   double logLike(0);
   for (size_t i(0); i < wts.size(); i++) {
      logLike += std::log(wts.at(i));
   }
   return logLike;
}

const Event & PsfClusters::findLargestCluster(double & maxLogLike) const {
   size_t ilargest(0);
   maxLogLike = eventLogLike(m_events.front());
   for (size_t i(1); i < m_events.size(); i++) {
      double currentLogLike(eventLogLike(m_events.at(i)));
      if (currentLogLike > maxLogLike) {
         ilargest = i;
         maxLogLike = currentLogLike;
      }
   }
   return m_events.at(ilargest);
}

void PsfClusters::computePsfWts(const Event & evt, 
                                std::vector<double> & wts) const {
   wts.clear();
   double theta(m_scData.inclination(evt.time(), evt.dir()));
   std::vector<Event>::const_iterator event(m_events.begin());
   for ( ; event != m_events.end(); ++event) {
      double sep(event->sep(evt));
      wts.push_back(m_psfs[evt.eventClass()]->value(sep, event->energy(),
                                                    theta, 0));
   }
}

void PsfClusters::loadIrfs(const std::string & irfs) {
   irfLoader::Loader::go(irfs);
   const std::vector<std::string> & irfNames =
      irfLoader::Loader::respIds().find(irfs)->second;
   m_psfs.resize(irfNames.size());
   for (size_t i(0); i < irfNames.size(); i++) {
      irfInterface::Irfs * irf = 
         irfInterface::IrfsFactory::instance()->create(irfNames.at(i));
      m_psfs.at(irf->irfID()) = irf->psf()->clone();
   }
}

} // namespace pyASP
