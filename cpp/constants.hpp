#pragma once

#include <cmath>

#include <boost/multiprecision/cpp_bin_float.hpp>
#include <boost/multiprecision/number.hpp>

using boost::multiprecision::cpp_bin_float;
using boost::multiprecision::cpp_bin_float_double;
using boost::multiprecision::number;

//100 digits of precision, 5 digits of buffer
//to avoid false positives and false negatives

//use an ordinary double for now for speed purposes
typedef cpp_bin_float_double b_float;
//typedef number<cpp_bin_float<105> > b_float;

//eps = 1e-100
//so we have 100 digits of accuracy and 5 digits of buffer

//also use 1e-12 as eps for now
const b_float EPS = pow(b_float(10), b_float(-12));
//const b_float EPS = pow(b_float(10), b_float(-100));