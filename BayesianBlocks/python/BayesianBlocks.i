// -*- mode: c++ -*-
%module BayesianBlocks
%{
#include "BayesianBlocks/BayesianBlocks.h"
#include <vector>
%}
%include stl.i
%include ../BayesianBlocks/BayesianBlocks.h
%template(DoubleVector) std::vector<double>;
