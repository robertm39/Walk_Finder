#pragma once

#include <unordered_map>
#include <vector>

#include "constants.hpp"
#include "point.hpp"
#include "point_store_key.hpp"
#include "node_iterators.hpp"

using std::unordered_map;
using std::vector;

class PointStore
{
    private:
        const int num_decimals_;
        const bool has_one_away_;
        const bool has_same_place_;
        const bool has_within_two_;
        vector<PointStoreKey> one_away_cells_;//may not be used
        vector<PointStoreKey> within_two_cells_;//may not be used
        unordered_map<int, vector<int>> one_away_;//may not be used
        unordered_map<int, vector<int>> same_place_;//may not be used
        unordered_map<int, vector<int>> within_two_;//may not be used
    public:
        PointStore(int, bool, bool, bool);

        void add_node(int, const Point&);

        NodeIterators at_one(const Point&);
        NodeIterators same_place(const Point&);
        NodeIterators within_two(const Point&);

        /*vector<int>::const_iterator within_one_cbegin(const Point&);
        vector<int>::const_iterator within_one_cend(const Point&);
        vector<int>::const_iterator same_place_cbegin(const Point&);
        vector<int>::const_iterator same_place_cend(const Point&);
        vector<int>::const_iterator within_two_cbegin(const Point&);
        vector<int>::const_iterator within_two_cend(const Point&);*/
};

int get_key(b_float num, int num_decimals); //temporarily add access for testing
int get_full_key(const Point &p, int num_decimals);