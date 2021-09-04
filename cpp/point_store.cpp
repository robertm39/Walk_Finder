#include "point_store.hpp"

using std::unordered_map;
using std::vector;

//Make the circle methods
const vector<PointStoreKey> SAME_CELLS {PointStoreKey( 0,  0),
                                        PointStoreKey( 1,  0),
                                        PointStoreKey( 1,  1),
                                        PointStoreKey( 0,  1),
                                        PointStoreKey(-1,  1),
                                        PointStoreKey(-1,  0),
                                        PointStoreKey(-1, -1),
                                        PointStoreKey( 0, -1),
                                        PointStoreKey( 1, -1)};

const unordered_map<int, vector<PointStoreKey>> UNIT_CELL_CACHE;

vector<PointStoreKey> get_unit_cells(int num_decimals)
{
    

    vector<PointStoreKey> result;



    return result;
}

PointStore::PointStore(int n, bool h1, bool h2, bool h3): num_decimals_(n), has_one_away_(h1), has_same_place_(h2), has_within_two_(h3)
{
    //Initialize the various dictionaries
}