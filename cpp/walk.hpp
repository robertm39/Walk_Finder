#pragma once

#include <map>
#include <set>

#include "constants.hpp"
#include "point.hpp"

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
        int size() const {return nodes_.size();}
        bool has_node(int n) const {return nodes_.find(n) != nodes_.end();}
        void add_node(int, const Point&);
        void remove_node(int);

        const Point& coords(int) const;

        set<int>::iterator begin() {return nodes_.begin();}
        set<int>::iterator end() {return nodes_.end();}

        set<int>::const_iterator cbegin() const {return nodes_.cbegin();}
        set<int>::const_iterator cend() const {return nodes_.cend();}
};