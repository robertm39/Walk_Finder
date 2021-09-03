//#pragma once

#include <utility>

#include "walk.hpp"

using std::set;
using std::map;
using std::make_pair;

Walk::Walk(const Walk &walk)
{
    set<int>::const_iterator n_begin = walk.cbegin();
    set<int>::const_iterator n_end = walk.cend();

    for(int n = *n_begin; n_begin != n_end; n_begin++)
    {
        add_node(n, walk.coords(n));
    }
}

void Walk::add_node(int n, const Point &p)
{
    nodes_.insert(n);
    coords_.insert(make_pair(n, p));
}

void Walk::remove_node(int n)
{
    nodes_.erase(n);
    coords_.erase(n);
}

const Point& Walk::coords(int n) const
{
    return coords_.at(n);
}