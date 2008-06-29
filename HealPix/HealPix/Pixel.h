/**
 * @file Pixel.h
 * @author J. Chiang <jchiang@slac.stanford.edu>
 *
 * $Header$
 */

#ifndef _HealPix_Pixel_h
#define _HealPix_Pixel_h

#include "astro/SkyDir.h"
#include "astro/Healpix.h"

class Pixel : public astro::Healpix::Pixel {

public:
   /// @brief construct a pixel from the index
   Pixel(long index, const astro::Healpix & hp) 
      : astro::Healpix::Pixel(index, hp) {}

   /// @brief create a Pixel from a direction
   Pixel(const astro::SkyDir& dir, const astro::Healpix& hp) 
      : astro::Healpix::Pixel(dir, hp) {}

   Pixel(const astro::Healpix::Pixel & my_pix) 
      : astro::Healpix::Pixel(my_pix) {}

   double area() const {
      return astro::Healpix::Pixel::area();
   }

   astro::SkyDir operator()() const {
      return *this;
   }

   long index() const {
      return astro::Healpix::Pixel::index();
   }

#ifndef SWIG
   class StopIteration : public std::exception {
   public:
      StopIteration() {}
      virtual ~StopIteration() throw() {}
      virtual const char * what() const throw() {return "stop iteration";}
   };
#endif // SWIG
};

#endif // _HealPix_Pixel_h
