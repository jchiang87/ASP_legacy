/**
 * @file Event.h
 * @brief Encapsulation of LAT photon event.
 * @author J. Chiang <jchiang@slac.stanford.edu>
 *
 * $Header$
 */

#ifndef pyASP_Event_h
#define pyASP_Event_h

#include "astro/SkyDir.h"

namespace pyASP {

/**
 * @class Event
 */

class Event {

public:

   Event() {}

   Event(double ra, double dec, double time, double energy, int eventClass) 
      : m_dir(astro::SkyDir(ra, dec)), m_time(time), m_energy(energy),
        m_eventClass(eventClass), m_id(s_id++) {}

//    Event(const Event & other) 
//       : m_time(other.m_time), m_energy(other.m_energy),
//         m_eventClass(other.m_eventClass), m_id(other.m_id) {
//       m_dir = astro::SkyDir(other.m_dir.ra(), other.m_dir.dec());
//    }

   double sep(const Event & event) const {
      return m_dir.difference(event.m_dir)*180./M_PI;
   }

   double time() const {
      return m_time;
   }

   const astro::SkyDir & dir() const {
      return m_dir;
   }

   bool operator==(const Event & event) const {
      return m_id == event.m_id;
   }

   bool operator!=(const Event & event) const {
      return m_id != event.m_id;
   }

private:

   astro::SkyDir m_dir;
   double m_time;
   double m_energy;
   int m_eventClass;
   unsigned int m_id;

   static unsigned int s_id;

};

} // namespace pyASP

#endif // pyASP_Event_h
