#pragma once

#include <cmath>

#include <boost/multiprecision/cpp_bin_float.hpp>
#include <boost/multiprecision/number.hpp>

using boost::multiprecision::cpp_bin_float;
using boost::multiprecision::cpp_bin_float_double;
using boost::multiprecision::number;

//100 digits of precision, 5 digits of buffer
//to avoid false positives and false negatives

typedef number<cpp_bin_float<105> > b_float;

//eps = 1e-100
//so we have 100 digits of accuracy and 5 digits of buffer

const b_float EPS = pow(b_float(10), b_float(-100));