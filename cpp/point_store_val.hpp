#pragma once

#include "point.hpp"

class PointStoreVal
{
    private:
        const int node_;
        const Point point_;
    public:
        int node() const {return node_;}
        Point point() const {return point_;}
        PointStoreVal(int n, const Point &p): node_(n), point_(p) {}
};