#pragma once

#include <vector>

using std::vector;

struct NodeIterators
{
    vector<int>::const_iterator cbegin;
    vector<int>::const_iterator cend;
    NodeIterators(vector<int>::const_iterator cb, vector<int>::const_iterator ce): cbegin(ce), cend(ce) {}
};