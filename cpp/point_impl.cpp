//#pragma once

#include "constants.hpp"
#include "point_impl.hpp"

//This method is mainly for aesthetics
/*
const b_float dist(const PointImpl &p1, const PointImpl &p2)
{
    return (p2 - p1).norm();
}

const PointImpl operator+(const PointImpl &p1, const PointImpl &p2) {return PointImpl(p1.x() + p2.x(), p1.y() + p2.y());}
const PointImpl operator-(const PointImpl &p1, const PointImpl &p2) {return PointImpl(p1.x() - p2.x(), p1.y() - p2.y());}

//Define scalar multiplication both ways
const PointImpl operator*(const PointImpl &p1, const b_float &s) {return PointImpl(p1.x() * s, p1.y() * s);}
const PointImpl operator*(const b_float &s, const PointImpl &p1) {return PointImpl(p1.x() * s, p1.y() * s);}

const PointImpl operator/(const PointImpl &p1, const b_float &s) {return PointImpl(p1.x() / s, p1.y() / s);}

bool operator==(const PointImpl &p1, const PointImpl &p2)
{
    return p1.x() == p2.x() && p1.y() == p2.y();
}

bool operator!=(const PointImpl &p1, const PointImpl &p2)
{
    return p1.x() != p2.x() || p1.y() != p2.y();
}

ostream& operator<< (ostream& os, const PointImpl &p)
{
    //No brackets or commas
    os << p.x() << " " << p.y();
    return os;
}*/