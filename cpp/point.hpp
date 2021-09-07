#pragma once

#include <iostream>
#include <memory>

#include "constants.hpp"
#include "point_impl.hpp"

using std::ostream;
using std::shared_ptr;

//For now, leave it const
class Point
{
    private:
        //const b_float x_;
        //const b_float y_;
        shared_ptr<PointImpl> impl_;
    public:
        Point(const b_float &x, const b_float &y): impl_(new PointImpl(x, y)) {}
        b_float x() const {return impl_->x();}
        b_float y() const {return impl_->y();}
        b_float norm() const {return impl_->norm();}
        Point perp() const {return Point(-y(), x());}
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

bool operator==(const Point&, const Point&);
bool operator!=(const Point&, const Point&);

ostream& operator<<(ostream&, const Point&);