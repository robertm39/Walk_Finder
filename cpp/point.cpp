//#pragma once

#include "constants.hpp"
#include "point.hpp"

const Point operator+(const Point &p1, const Point &p2) {return Point(p1.x() + p2.x(), p1.y() + p2.y());}
const Point operator-(const Point &p1, const Point &p2) {return Point(p1.x() - p2.x(), p1.y() - p2.y());}

//Define scalar multiplication both ways
const Point operator*(const Point &p1, const b_float &s) {return Point(p1.x() * s, p1.y() * s);}
const Point operator*(const b_float &s, const Point &p1) {return Point(p1.x() * s, p1.y() * s);}

const Point operator/(const Point &p1, const b_float &s) {return Point(p1.x() * s, p1.y() / s);}

ostream& operator<< (ostream& os, const Point &p)
{
    //No brackets or commas
    os << p.x() << " " << p.y();
    return os;
}