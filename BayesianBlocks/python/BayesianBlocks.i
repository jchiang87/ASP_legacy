// -*- mode: c++ -*-
%module BayesianBlocks
%{
#include "BayesianBlocks/BayesianBlocks.h"
#include "BayesianBlocks/Exposure.h"
#include <vector>
%}
%include stl.i
%include ../BayesianBlocks/BayesianBlocks.h
%include ../BayesianBlocks/Exposure.h
%template(DoubleVector) std::vector<double>;
%template(IntVector) std::vector<int>;
