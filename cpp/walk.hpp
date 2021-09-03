#pragma once

#include <map>
#include <set>

#include "constants.hpp"
#include "point.hpp"
#include "point.cpp" //necessary, it seems

using std::map;
using std::set;

class Walk
{
    private:
        set<int> nodes_;
        map<int, Point> coords_;
    public:
        Walk() {}
        Walk(const Walk&); //Copy constructor instead of an explicit copy method

        void add_node(int, const Point&);
        void remove_node(int);

        const Point& coords(int);
        
};