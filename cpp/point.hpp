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
        Point perp() const {return Point(-y_, x_);}
};

Point operator+(const Point &p1, const Point &p2) {return Point(p1.x() + p2.x(), p1.y() + p2.y());}
Point operator-(const Point &p1, const Point &p2) {return Point(p1.x() - p2.x(), p1.y() - p2.y());}

//Define scalar multiplication both ways
Point operator*(const Point &p1, const b_float &s) {return Point(p1.x() * s, p1.y() * s);}
Point operator*(const b_float &s, const Point &p1) {return Point(p1.x() * s, p1.y() * s);}

Point operator/(const Point &p1, const b_float &s) {return Point(p1.x() * s, p1.y() / s);}

ostream& operator<<(ostream&, const Point&);