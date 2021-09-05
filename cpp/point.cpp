//#pragma once

#include "constants.hpp"
#include "point.hpp"

//This method is mainly for aesthetics
const b_float dist(const Point &p1, const Point &p2)
{
    return (p2 - p1).norm();
}

bool same(const b_float &b1, const b_float &b2)
{
    b_float diff = b2 - b1;
    return abs(diff) <= EPS; //abs does work with the high-precision values
}

const Point operator+(const Point &p1, const Point &p2) {return Point(p1.x() + p2.x(), p1.y() + p2.y());}
const Point operator-(const Point &p1, const Point &p2) {return Point(p1.x() - p2.x(), p1.y() - p2.y());}

//Define scalar multiplication both ways
const Point operator*(const Point &p1, const b_float &s) {return Point(p1.x() * s, p1.y() * s);}
const Point operator*(const b_float &s, const Point &p1) {return Point(p1.x() * s, p1.y() * s);}

const Point operator/(const Point &p1, const b_float &s) {return Point(p1.x() / s, p1.y() / s);}

bool operator==(const Point &p1, const Point &p2)
{
    return p1.x() == p2.x() && p1.y() == p2.y();
}

bool operator!=(const Point &p1, const Point &p2)
{
    return p1.x() != p2.x() || p1.y() != p2.y();
}

ostream& operator<< (ostream& os, const Point &p)
{
    //No brackets or commas
    os << p.x() << " " << p.y();
    return os;
}