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
        vector< vector<int>* > vectors_; //Store the pointers to the lists so that we can delete them later (??)
        vector<PointStoreKey> one_away_cells_;//may not be used
        vector<PointStoreKey> within_two_cells_;//may not be used
        unordered_map<int, vector<int>*> one_away_;//may not be used
        unordered_map<int, vector<int>*> same_place_;//may not be used
        unordered_map<int, vector<int>*> within_two_;//may not be used

        void add_node_to_map(int key, int n, unordered_map<int, vector<int>*> &m);
    public:
        PointStore(int, bool, bool, bool);
        ~PointStore(); //deallocate the vector<int>* 's

        void add_node(int, const Point&);

        NodeIterators one_away(const Point&);
        NodeIterators same_place(const Point&);
        NodeIterators within_two(const Point&);
};