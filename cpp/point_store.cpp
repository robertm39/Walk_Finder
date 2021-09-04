#include <cmath>
#include <string>
#include <iostream>
//#include <stdio.h>

#include "point_store.hpp"

using std::unordered_map;
using std::vector;
using std::sqrt;
using std::string;
using std::stringstream;
using std::strncpy;

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

vector<Point> get_corner_disps(b_float width)
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

vector<PointStoreKey> get_unit_cells(int num_decimals)
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
    const vector<Point> corner_disps = get_corner_disps(width);
    
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

            for(const Point &d1: corner_disps)
            {
                for(const Point &d2: corner_disps)
                {
                    Point corner_to_corner = diff + d1 - d2;
                    b_float overall_dist = corner_to_corner.norm();

                    if(same(overall_dist, 1))
                    {
                        ge_one = true;
                        le_one = true;
                        break;
                    }

                    if(overall_dist < 1)
                    {
                        le_one = true;
                    } else if(overall_dist > 1)
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

            b_float dist_from_origin = diff.norm();
            if(dist_from_origin > max_dist)
            {
                continue;
            }

            //Now we check the corner combinations
            //If at least one <= 1, and at least one >= 1, (or one is equal to 1 within EPS), we include this cell
            bool le_two = false;

            for(const Point &d1: corner_disps)
            {
                for(const Point &d2: corner_disps)
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
int get_key(b_float num, int num_decimals)
{
    stringstream ss;  // Read and write std::stringstream.
    ss.precision(std::numeric_limits<b_float>::max_digits10);  // Ensure all potentially significant bits are output.
    ss.flags(std::ios_base::fmtflags(std::ios_base::dec)); // Use scientific format.
    string num_s = ss.str();
    //hope that this forces num_s to be formatted right

    auto decimal_index = num_s.find('.');
    auto needed_size = num_decimals + decimal_index + 1;
    auto size_shortfall = needed_size - num_s.size();
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
    trimmed[decimal_index + num_decimals + 1] ; '\0';

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

PointStoreKey get_full_key(const Point &p, int num_decimals)
{
    int x_key = get_key(p.x(), num_decimals);
    int y_key = get_key(p.y(), num_decimals);

    return PointStoreKey(x_key, y_key);
}

PointStore::PointStore(int n, bool h1, bool h2, bool h3): num_decimals_(n), has_one_away_(h1), has_same_place_(h2), has_within_two_(h3)
{
    //Initialize the cell collections
    if(has_same_place_)
    {
        one_away_cells_ = get_unit_cells(num_decimals_);
    }
    if(has_within_two_)
    {
        within_two_cells_ = get_within_two_cells(num_decimals_);
    }
    
    //The dictionaries are already initialized
}

void PointStore::add_node(int node, const Point &point)
{
}