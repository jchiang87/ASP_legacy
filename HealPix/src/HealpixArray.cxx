/**
 * @file HeapixArray.cxx
 * @brief Implementation for subclass of astro::HealpixArray<float> with
 * FITS I/O member functions.
 *
 * @author J. Chiang <jchiang@slac.stanford.edu>
 *
 * $Header$
 */

#include <stdexcept>

#include "tip/IFileSvc.h"
#include "tip/Header.h"
#include "tip/Table.h"

#include "astro/SkyDir.h"

#include "map_tools/HealpixArrayIO.h"
#include "map_tools/SkyImage.h"

#include "HealPix/HealpixArray.h"

HealpixArray::HealpixArray() : astro::HealpixArray<float>(astro::Healpix()) {
   fillCoordArrays();
}

HealpixArray::HealpixArray(astro::Healpix hp) 
   : astro::HealpixArray<float>(hp) {
   fillCoordArrays();
}

HealpixArray::HealpixArray(const std::string & infile, 
                           const std::string & extname,
                           const std::string & fieldname) {
   const astro::HealpixArray<float> & my_array = 
      map_tools::HealpixArrayIO::instance().read(infile,extname,fieldname);
   
   astro::Healpix my_hp(my_array.healpix().nside(), 
                        my_array.healpix().ord(),
                        coordsys(infile, extname));
   *this = HealpixArray(my_hp);
   for (size_t i(0); i < my_array.size(); i++) {
      at(i) = my_array.at(i);
   }
   fillCoordArrays();
}

HealpixArray::~HealpixArray() {}

void HealpixArray::write(const std::string & outfile, 
                         const std::string & extname,
                         const std::string & fieldname) const {
   std::auto_ptr<tip::Table> table = 
      map_tools::HealpixArrayIO::instance().write(*this, outfile, extname,
                                                  fieldname, true);
   tip::Header & header(table->getHeader());
   header["COORDSYS"].set(static_cast<int>(healpix().coordsys()));
}

void HealpixArray::writeImage(const std::string & outfile,
                              double pixel_size, bool galactic) const {
   astro::SkyDir::CoordSystem coordsys(astro::SkyDir::EQUATORIAL);
   if (galactic) {
      coordsys = astro::SkyDir::GALACTIC;
   }
   double fov;
   int layers;
   std::string proj;
   map_tools::SkyImage image(astro::SkyDir(0, 0, coordsys), outfile,
                             pixel_size, fov=360, layers=1, proj="AIT",
                             galactic);
   image.fill(*this);
}

#undef _DEFINE_BINARY_OPERATOR
#define _DEFINE_BINARY_OPERATOR(_Op, _Name)                             \
HealpixArray HealpixArray::operator _Op(const HealpixArray & x) const { \
   HealpixArray y(healpix());                                           \
   for (size_t i(0); i < size(); i++) {                                 \
      y.at(i) = at(i) _Op x.at(i);                                      \
   }                                                                    \
   return y;                                                            \
}

_DEFINE_BINARY_OPERATOR(+, plus)
_DEFINE_BINARY_OPERATOR(-, minus)
_DEFINE_BINARY_OPERATOR(*, times)
_DEFINE_BINARY_OPERATOR(/, divide)
#undef _DEFINE_BINARY_OPERATOR

#define _DEFINE_BINARY_OPERATOR(_Op, _Name)                             \
HealpixArray HealpixArray::operator _Op(double x) const {               \
   HealpixArray y(healpix());                                           \
   for (size_t i(0); i < size(); i++) {                                 \
      y.at(i) = at(i) _Op x;                                            \
   }                                                                    \
   return y;                                                            \
}

_DEFINE_BINARY_OPERATOR(+, plus)
_DEFINE_BINARY_OPERATOR(-, minus)
_DEFINE_BINARY_OPERATOR(*, times)
_DEFINE_BINARY_OPERATOR(/, divide)
#undef _DEFINE_BINARY_OPERATOR

HealpixArray HealpixArray::operator-() const {
   HealpixArray y(healpix());
   for (size_t i(0); i < size(); i++) {
      y.at(i) = -at(i);
   }
   return y;
}

double HealpixArray::operator()(const astro::SkyDir & dir) const {
   return operator[](dir);
}

astro::Healpix HealpixArray::healpix() const {
   return astro::HealpixArray<float>::healpix();
}

const std::vector<float> & HealpixArray::values() const {
   return *this;
}

const std::vector<float> & HealpixArray::glon() const {
   return m_glon;
}

const std::vector<float> & HealpixArray::glat() const {
   return m_glat;
}

void HealpixArray::writeLayeredImage(const std::vector<HealpixArray> & arrays,
                                     const std::string & outfile,
                                     double pixel_size, bool galactic) {
   astro::SkyDir::CoordSystem coordsys(astro::SkyDir::EQUATORIAL);
   if (galactic) {
      coordsys = astro::SkyDir::GALACTIC;
   }
   double fov;
   int layers;
   std::string proj;
   map_tools::SkyImage image(astro::SkyDir(0, 0, coordsys), outfile,
                             pixel_size, fov=360, layers=arrays.size(), 
                             proj="AIT", galactic);
   for (size_t i(0); i < arrays.size(); i++) {
      image.fill(arrays.at(i), i);
   }
}

void HealpixArray::fillCoordArrays() {
   astro::Healpix hp = healpix();
   m_glon.clear();
   m_glat.clear();
   astro::Healpix::const_iterator pixel(hp.begin());
   for (; pixel != hp.end(); ++pixel) {
      double glon((*pixel)().l());
      if (glon > 180) {
         glon -= 360;
      }
      m_glon.push_back(glon);
      m_glat.push_back((*pixel)().b());
   }
}

astro::SkyDir::CoordSystem 
HealpixArray::coordsys(const std::string & infile,
                       const std::string & extname) const {
   const tip::Table * table(tip::IFileSvc::instance().readTable(infile,
                                                                extname));
   const tip::Header & header(table->getHeader());
   int coordsys_int;
   header["COORDSYS"].get(coordsys_int);
   astro::SkyDir::CoordSystem coordsys(astro::SkyDir::EQUATORIAL);
   if (coordsys_int == 0) {
      coordsys = astro::SkyDir::GALACTIC;
   }
   delete table;
   return coordsys;
}
