//#pragma once

#include <utility>

#include "walk.hpp"

using std::set;
//using std::map;
using std::make_pair;

Walk::Walk(const Walk &walk)
{
    
    set<int>::const_iterator n_end = walk.cend();

    int n = 0;
    for(set<int>::const_iterator n_begin = walk.cbegin(); n_begin != n_end; n_begin++)
    {
        n = *n_begin;
        add_node(n, walk.coords(n));
    }
}

void Walk::add_node(int n, Point p)
{
    nodes_.insert(n);
    coords_.insert(make_pair(n, p));
}

void Walk::remove_node(int n)
{
    nodes_.erase(n);
    coords_.erase(n);
}

Point Walk::coords(int n) const
{
    return coords_.at(n);
}

bool nodes_same_one_way(const Walk &w1, const Walk &w2)
{
    for(auto i = w1.cbegin(); i != w1.cend(); i++)
    {
        int node = *i;
        if(!w2.has_node(node))
        {
            return false;
        }
    }
    return true;
}

bool coords_same(const Walk &w1, const Walk &w2)
{
    for(auto i = w1.cbegin(); i != w1.cend(); i++)
    {
        int node = *i;
        if(w1.coords(node) != w2.coords(node))
        {
            return false;
        }
    }
    return true;
}

bool operator==(const Walk &w1, const Walk &w2)
{
    if(!(nodes_same_one_way(w1, w2) && nodes_same_one_way(w2, w1)))
    {
        return false;
    }
    return coords_same(w1, w2);
}

bool operator!=(const Walk &w1, const Walk &w2)
{
    return !(w1 == w2);
}