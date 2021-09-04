#pragma once

#include <map>
#include <vector>

#include "constants.hpp"
#include "point.hpp"
#include "point_store_key.hpp"
#include "point_store_val.hpp"

using std::map;
using std::vector;

class PointStore
{
    private:
        const int num_decimals_;
        const bool has_one_away_;
        const bool has_same_place_;
        const bool has_within_two_;
        map<PointStoreKey, vector<PointStoreVal>> one_away_;
        map<PointStoreKey, vector<PointStoreVal>> same_place_;
        map<PointStoreKey, vector<PointStoreVal>> within_two_;
    public:
        PointStore(int n, bool h1, bool h2, bool h3): num_decimals_(n), has_one_away_(h1), has_same_place_(h2), has_within_two_(h3) {}

        void add_node(int, const Point&);
        vector<PointStoreVal> within_one(const Point&);
        vector<PointStoreVal> same_place(const Point&);
        vector<PointStoreVal> within_two(const Point&);
};