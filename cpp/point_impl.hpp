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
        PointImpl(b_float x, b_float y): x_(x), y_(y) {}
        b_float x() const {return x_;}
        b_float y() const {return y_;}
        b_float norm() const {return sqrt(x_*x_ + y_*y_);}
        //Point perp() const {return Point(-y_, x_);}
};

//const b_float dist(const PointImpl&, const PointImpl&);

//Whether the two numbers are within EPS
//I didn't want to make an entire file to put this in
/*
const PointImpl operator+(const PointImpl&, const PointImpl&);
const PointImpl operator-(const PointImpl&, const PointImpl&);

//Define scalar multiplication both ways
const PointImpl operator*(const PointImpl&, const b_float&);
const PointImpl operator*(const b_float&, const PointImpl&);

const PointImpl operator/(const PointImpl&, const b_float&);

bool operator==(const PointImpl&, const PointImpl&);
bool operator!=(const PointImpl&, const PointImpl&);

ostream& operator<<(ostream&, const PointImpl&);*/