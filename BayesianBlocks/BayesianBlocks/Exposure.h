/**
 * @file Exposure
 * @brief LAT effective area, integrated over time bins, to a specific
 * point on the sky.
 * @author J. Chiang
 *
 * $Header$
 */

#ifndef _Exposure_h
#define _Exposure_h

/**
 * @class Exposure
 * @brief LAT effective area, integrated over time bins, to a specific
 * point on the sky.
 *
 * @author J. Chiang
 *
 * $Header$
 */

class Exposure {

public:

   Exposure(const std::string & scDataFile, 
            const std::vector<double> &timeBoundaries);

   double value(double time) const;

private:

   std::vector<double> m_timeBoundaries;
   std::vector<double> m_exposureValues;

}

#endif // _Exposure_h
