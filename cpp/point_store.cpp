#include <cmath>
#include <string>
#include <iostream>
#include <unordered_map>
#include <utility>
//#include <stdio.h>

#include "point_store.hpp"

using std::unordered_map;
using std::vector;
using std::sqrt;
using std::string;
using std::stringstream;
using std::strncpy;
using std::make_pair;

// for testing
using std::cout;
using std::endl;

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

//Don't change the vectors once they're calculated
unordered_map<int, vector<PointStoreKey>> UNIT_CELL_CACHE;

//const int MARGIN_MULT = 10;

vector<Point> get_corner_disps(const b_float &width, bool strict=false)
{
    if(strict)
    {
        vector<Point> corner_disps = {Point(0,       0      ),
                                      Point(0,       width/2),
                                      Point(0,       width  ),
                                      Point(width/2, width  ),
                                      Point(width,   width  ),
                                      Point(width,   width/2),
                                      Point(width,   0      ),
                                      Point(width/2, 0      )};
        return corner_disps;
    }
    else //this one doesn't quite go out to the edges
    {
        //simulating subcells to see how many cells it would cut
        b_float margin = width * (b_float(99) / 200);
        vector<Point> corner_disps = {Point(margin,         margin        ),
                                      Point(margin,         width/2       ),
                                      Point(margin,         width - margin),
                                      Point(width/2,        width - margin),
                                      Point(width - margin, width - margin),
                                      Point(width - margin, width/2       ),
                                      Point(width - margin, margin        ),
                                      Point(width/2,        margin        )};
        return corner_disps;
    }
}

vector<PointStoreKey> get_unit_cells(int num_decimals, bool strict=true)
{
    //Retrieve the value, and if it's empty, calculate
    vector<PointStoreKey> result = UNIT_CELL_CACHE[num_decimals];
    if (result.size() > 0)
    {
        return result;
    }

    //How wide a single cell is
    b_float width = pow(b_float(10), -num_decimals);

    //How many cells wide a 1x1 square is
    int num_cells_wide = pow(10, num_decimals); //this one should just be an integer

    //The diagonal length of a cell
    b_float diag = width * sqrt(b_float(2));

    //The minimum and maximum distances from the ll corner of one cell to the ll corner of the origin cell
    //in order for it to possibly be in the ring
    b_float min_dist = 1 - diag - EPS;
    b_float max_dist = 1 + diag + EPS;

    //All the displacements from the ll corner of a cell to other corners and the midpoints of edges
    const vector<Point> self_corner_disps = get_corner_disps(width, strict=strict);
    const vector<Point> other_corner_disps = get_corner_disps(width, strict=true);
    
    for(int dx = -num_cells_wide - 1; dx <= num_cells_wide + 1; dx++)
    {
        for(int dy = -num_cells_wide - 1; dy <= num_cells_wide + 1; dy++)
        {
            //Get the coords of the ll corner of the cell
            Point diff(dx*width, dy*width);

            b_float dist_from_origin = diff.norm();
            if(dist_from_origin < min_dist)
            {
                continue;
            }
            if(dist_from_origin > max_dist)
            {
                continue;
            }

            //Now we check the corner combinations
            //If at least one <= 1, and at least one >= 1, (or one is equal to 1 within EPS), we include this cell
            bool ge_one = false;
            bool le_one = false;

            cout.precision(std::numeric_limits<b_float>::max_digits10);  // Ensure all potentially significant bits are output.
            cout.flags(std::ios_base::fmtflags(std::ios_base::scientific)); // Use scientific format.

            for(Point d1: other_corner_disps)
            {
                for(Point d2: self_corner_disps)
                {
                    /*bool at_target = dx == 99 && dy == 0;
                    if(at_target)
                    {
                        cout << endl << "At (99, 0)" << endl;
                    }*/

                    Point corner_to_corner = diff + d1 - d2;

                    /*if(at_target)
                    {
                        cout << "d1: " << endl;
                        cout << d1 << endl;
                        cout << "d2: " << endl;
                        cout << d2 << endl;
                    }*/

                    /*if(at_target)
                    {
                        cout << "corner_to_corner: " << corner_to_corner << endl;
                    }*/

                    b_float overall_dist = corner_to_corner.norm();

                    /*if(at_target)
                    {
                        cout << "overall_dist: " << overall_dist << endl;
                    }*/

                    if(same(overall_dist, 1))
                    {
                        ge_one = true;
                        le_one = true;
                        break;
                    }

                    if(overall_dist < 1.0) // 1
                    {
                        le_one = true;
                    } else if(overall_dist > 1.0) // 1
                    {
                        ge_one = true;
                    }
                }

                // We already know that the cell works, so stop checking
                if(ge_one && le_one)
                {
                    break;
                }
            }

            if(ge_one && le_one)
            {
                //Now we know whether to include this cell
                PointStoreKey cell(dx, dy);

                result.push_back(cell);
            }

        }
    }

    UNIT_CELL_CACHE.insert(make_pair(num_decimals, result));

    return result;
}

//Don't change the vectors once they're calculated
unordered_map<int, vector<PointStoreKey>> WITHIN_TWO_CELL_CACHE;
vector<PointStoreKey> get_within_two_cells(int num_decimals)
{
    //Retrieve the value, and if it's empty, calculate
    vector<PointStoreKey> result = UNIT_CELL_CACHE[num_decimals];
    if (result.size() > 0)
    {
        return result;
    }

    //How wide a single cell is
    b_float width = pow(b_float(10), -num_decimals);

    //How many cells wide a 1x1 square is
    int num_cells_wide = pow(10, num_decimals); //this one should just be an integer

    //The diagonal length of a cell
    b_float diag = width * sqrt(b_float(2));

    //The maximum distance from the ll corner of one cell to the ll corner of the origin cell
    //in order for it to possibly be in the ring
    b_float max_dist = 2 + diag + EPS;

    const vector<Point> corner_disps = get_corner_disps(width);

        for(int dx = -num_cells_wide - 2; dx <= num_cells_wide + 2; dx++)
    {
        for(int dy = -num_cells_wide - 2; dy <= num_cells_wide + 2; dy++)
        {
            //Get the coords of the ll corner of the cell
            Point diff(dx*width, dy*width);

            if(diff.norm() > max_dist)
            {
                continue;
            }

            //Now we check the corner combinations
            //If at least one <= 1, and at least one >= 1, (or one is equal to 1 within EPS), we include this cell
            bool le_two = false;

            for(Point d1: corner_disps)
            {
                for(Point d2: corner_disps)
                {
                    Point corner_to_corner = diff + d1 - d2;
                    b_float overall_dist = corner_to_corner.norm();

                    if(same(overall_dist, 2))
                    {
                        le_two = true;
                        break;
                    }
                    if(overall_dist <= 2)
                    {
                        le_two = true;
                        break;
                    }
                }

                // We already know that the cell works, so stop checking
                if(le_two)
                {
                    break;
                }
            }

            if(le_two)
            {
                //Now we know whether to include this cell
                PointStoreKey cell(dx, dy);
                result.push_back(cell);
            }

        }
    }
    WITHIN_TWO_CELL_CACHE.insert(make_pair(num_decimals, result));

    return result;
}

//I'll hope this isn't necessary if I'm forcing the digits to be printed in decimal
/*string homogenize(const string &num_s)
{
    //Deal with numbers that don't have a decimal
}*/

//Return the key based on the number
//code borrowed from
//https://www.boost.org/doc/libs/1_77_0/libs/multiprecision/doc/html/boost_multiprecision/tut/input_output.html
int get_key(const b_float &num, int num_decimals)
{
    stringstream ss;
    ss.precision(std::numeric_limits<b_float>::max_digits10);
    ss.flags(std::ios_base::fmtflags(std::ios_base::fixed)); // use fixed format
    ss << num; //I forgot this at first
    string num_s = ss.str();

    int decimal_index = num_s.find('.');
    int needed_size = num_decimals + decimal_index + 1;
    int size_shortfall = needed_size - num_s.size();
    //If num_s doesn't have enough decimal places (not likely), pad with zeroes
    if(size_shortfall > 0)
    {
        num_s = num_s + string('0', size_shortfall);
    }
    //get the first (decimal_index + num_decimals + 1) chars from the string
    char *trimmed = new char[decimal_index + num_decimals + 2]; //add a space for the null terminator
    strncpy(trimmed, num_s.c_str(), decimal_index + num_decimals + 1);

    //Add the null terminator at the end
    //this is necessary because I didn't get the entire source string
    trimmed[decimal_index + num_decimals + 1] = '\0';

    //borrowing from
    //https://stackoverflow.com/questions/5891610/how-to-remove-certain-characters-from-a-string-in-c
    string final_s = string(trimmed);

    final_s.erase(remove(final_s.begin(), final_s.end(), '.'), final_s.end()); //Get rid of the decimal point

    int key ;
    //For this to work, negative keys need to be lower
    if(final_s[0] == '-')
    {
        //These steps look unecessarily complicated, and they probably are
        //But I don't want to stray too much from the python
        final_s.erase(remove(final_s.begin(), final_s.end(), '-'), final_s.end()); //Get rid of the minus sign
        stringstream string_s(final_s);
        string_s >> key;
        key += 1;
        key *= -1; 
    } else {
        stringstream string_s(final_s);
        string_s >> key;
    }

    delete [] trimmed; //At the end

    return key;
}

PointStoreKey get_point_key(Point p, int num_decimals)
{
    int x_key = get_key(p.x(), num_decimals);
    int y_key = get_key(p.y(), num_decimals);
    return PointStoreKey(x_key, y_key);
}

int get_full_key(const PointStoreKey &k)
{
    return (k.x() << 16) ^ (k.y() & 65535);
}

bool PointStore::float_is_stable(const b_float &num)
{
    int key = get_key(num, num_decimals_);
    int upper_key = get_key(num + margin_, num_decimals_);
    int lower_key = get_key(num - margin_, num_decimals_);

    return key == upper_key && key == lower_key;
}

bool PointStore::point_is_stable(Point p)
{
    return float_is_stable(p.x()) && float_is_stable(p.y());
}

PointStore::PointStore(int n, bool h1, bool h2, bool h3): num_decimals_(n), has_one_away_(h1), has_same_place_(h2), has_within_two_(h3)
{
    
    //How wide a single cell is
    width_ = pow(b_float(10), -num_decimals_);
    margin_ = width_ * (b_float(9) / 20); //A slightly larger margin, to be safe
    //Initialize the cell collections
    if(has_same_place_)
    {
        one_away_cells_loose_ = get_unit_cells(num_decimals_, false);
        /*for(auto k: one_away_cells_loose_)
        {
            cout << k << endl;
        }*/
        cout << "loose cells: " << one_away_cells_loose_.size() << endl;

        one_away_cells_strict_ = get_unit_cells(num_decimals_, true);

        cout << "strict cells: " << one_away_cells_strict_.size() << endl;
    }
    if(has_within_two_)
    {
        within_two_cells_ = get_within_two_cells(num_decimals_);
        /*for(const PointStoreKey &k: within_two_cells_)
        {
            cout << k << endl;
        }*/
    }
    
    //The dictionaries are already initialized
}

PointStore::~PointStore()
{
    for(vector<int> *v: vectors_)
    {
        delete v; //delete all the allocated vectors
    }
}

//Add a node to the given map with the given key
void PointStore::add_node_to_map(int key, int node, unordered_map<int, vector<int>*> &m)
{
    //See if the map already has a vector<int>* for that point
    if(m.count(key) == 0)
    {
        vector<int> *v = new vector<int>(); //deallocate in the destructor
        vectors_.push_back(v);
        m.insert(make_pair(key, v));
    }
    //cout << "getting node-vector at key" << endl;
    vector<int> *v = m.at(key);
    v->push_back(node);
}

void PointStore::add_node(int node, Point point)
{
    PointStoreKey p_key = get_point_key(point, num_decimals_);
    //cout << "p_key: " << p_key << endl;

    if(has_same_place_)
    {
        for(const PointStoreKey &dp: SAME_CELLS)
        {
            PointStoreKey total_key = p_key + dp;
            int real_key = get_full_key(total_key);
            //I'm not including the points in the values
            //because it takes up way too much memory
            //you can just get the points from the Walk

            add_node_to_map(real_key, node, same_place_);
            //same_place_.insert(make_pair(real_key, node));
        }
    }

    if(has_one_away_)
    {
        if(point_is_stable(point))
        {
            for(const PointStoreKey &dp: one_away_cells_loose_)
            {
                PointStoreKey total_key = p_key + dp;
                int real_key = get_full_key(total_key);

                add_node_to_map(real_key, node, one_away_);
            }
        }
        else
        {
            for(const PointStoreKey &dp: one_away_cells_strict_)
            {
                PointStoreKey total_key = p_key + dp;
                int real_key = get_full_key(total_key);

                add_node_to_map(real_key, node, one_away_);
            }
        }
    }

    if(has_within_two_)
    {
        for(const PointStoreKey &dp: within_two_cells_)
        {
            PointStoreKey total_key = p_key + dp;
            int real_key = get_full_key(total_key);

            add_node_to_map(real_key, node, within_two_);
            //within_two_.insert(make_pair(real_key, node));
        }
    }
}

NodeIterators PointStore::one_away(Point p)
{
    //cout << "getting key" << endl;
    PointStoreKey p_key = get_point_key(p, num_decimals_);
    //cout << p_key << endl;
    int key = get_full_key(p_key);
    vector<int> *nodes;
    if(one_away_.count(key) >= 1) //slightly redundant, but I don't think this will be the slowest part
    {
        //cout << "found a bucket" << endl;
        //cout << "getting nodes one away" << endl;
        nodes = one_away_.at(key);
    } else {
        //cout << "failed at point:" << endl;
        //cout << p << endl;
        //cout << p_key << endl;
        //cout << key << endl;
        //dereferencing the end of a list is an error anyways
        //so this should be fine
        return NodeIterators(static_cast<vector<int>::const_iterator>(nullptr), static_cast<vector<int>::const_iterator>(nullptr));
    }
    //cout << "Found " << nodes->size() << " node(s)" << endl;
    auto begin_it = nodes->cbegin();
    auto end_it = nodes->cend();
    return NodeIterators(begin_it, end_it);
}

NodeIterators PointStore::same_place(Point p)
{
    int key = get_full_key(get_point_key(p, num_decimals_));
    vector<int> *nodes;
    if(same_place_.count(key) >= 1) //slightly redundant, but I don't think this will be the slowest part
    {
        //cout << "getting nodes at some place" << endl;
        nodes = same_place_.at(key);
    } else {
        //dereferencing the end of a list is an error anyways
        //so this should be fine
        return NodeIterators(static_cast<vector<int>::const_iterator>(nullptr), static_cast<vector<int>::const_iterator>(nullptr));
    }
    auto begin_it = nodes->cbegin();
    auto end_it = nodes->cend();
    return NodeIterators(begin_it, end_it);
}

NodeIterators PointStore::within_two(Point p)
{
    int key = get_full_key(get_point_key(p, num_decimals_));
    vector<int> *nodes;
    if(within_two_.count(key) >= 1) //slightly redundant, but I don't think this will be the slowest part
    {
        //cout << "getting nodes within two" << endl;
        nodes = within_two_.at(key);
    } else {
        //dereferencing the end of a list is an error anyways
        //so this should be fine
        return NodeIterators(static_cast<vector<int>::const_iterator>(nullptr), static_cast<vector<int>::const_iterator>(nullptr));
    }
    auto begin_it = nodes->cbegin();
    auto end_it = nodes->cend();
    return NodeIterators(begin_it, end_it);
}