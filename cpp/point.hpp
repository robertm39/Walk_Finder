#pragma once

#include <iostream>

#include "constants.hpp"

using std::ostream;

//For now, leave it const
class Point
{
    private:
        const b_float x_;
        const b_float y_;
    public:
        Point(b_float x, b_float y): x_(x), y_(y) {}
        b_float x() const {return x_;}
        b_float y() const {return y_;}
        b_float norm() const {return sqrt(x_*x_ + y_*y_);}
        Point perp() const {return Point(-y_, x_);}
};

const b_float dist(const Point&, const Point&);

//Whether the two numbers are within EPS
//I didn't want to make an entire file to put this in
bool same(const b_float&, const b_float&);

const Point operator+(const Point&, const Point&);
const Point operator-(const Point&, const Point&);

//Define scalar multiplication both ways
const Point operator*(const Point&, const b_float&);
const Point operator*(const b_float&, const Point&);

const Point operator/(const Point&, const b_float&);

ostream& operator<<(ostream&, const Point&);