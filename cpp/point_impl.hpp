#pragma once

#include <iostream>

#include "constants.hpp"
//#include "point.hpp"

using std::ostream;

//For now, leave it const
class PointImpl
{
    private:
        const b_float x_;
        const b_float y_;
    public:
        PointImpl(const b_float &x, const b_float &y): x_(x), y_(y) {}
        b_float x() const {return x_;}
        b_float y() const {return y_;}
        b_float norm() const {return sqrt(x_*x_ + y_*y_);}
};