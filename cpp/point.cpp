#pragma once

#include "constants.hpp"
#include "point.hpp"

/*
Point operator*(const Point &p1, const b_float &s)
{
    return Point(p1.x() * s, p1.y() * s);
}

Point operator*(const b_float &s, const Point &p1)
{
    return Point(p1.x() * s, p1.y() * s);
}

Point operator/(const Point &p1, const b_float &s)
{
    return Point(p1.x() / s, p1.y() / s);
}*/

ostream& operator<< (ostream& os, const Point &p)
{
    //No brackets or commas
    os << p.x() << " " << p.y();
    return os;
}