#pragma once

#include <unordered_map>
#include <set>

#include "constants.hpp"
#include "point.hpp"

using std::unordered_map;
using std::set;

//Tested and worked
class Walk
{
    private:
        set<int> nodes_;
        unordered_map<int, Point> coords_; //stores points by value, so it doesn't matter if the originals are destroyed
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

bool operator==(const Walk&, const Walk&);
bool operator!=(const Walk&, const Walk&);