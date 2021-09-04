#pragma once

#include <vector>

using std::vector;

struct NodeIterators
{
    vector<int>::const_iterator cbegin;
    vector<int>::const_iterator cend;
};