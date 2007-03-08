/**
 * @file ScData.h
 * @brief Encapsulation of Spacecraft data
 * @author J. Chiang <jchiang@slac.stanford.edu>
 *
 * $Header$
 */

#ifndef pyASP_ScData_h
#define pyASP_ScData_h

#include <string>

#include "astro/SkyDir.h"

namespace pyASP {

class ScData {

public:
   
   ScData(const std::string & ft2File);

   astro::SkyDir zaxis(double time) const;

   double inclination(double time, const astro::SkyDir & srcDir) const;

};

} // namespace pyASP

#endif // pyASP_ScData_h
