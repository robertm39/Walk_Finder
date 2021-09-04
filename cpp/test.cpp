#include <iostream>
#include <cmath>

#include "constants.hpp"
#include "point.hpp"
#include "walk.hpp"
#include "graph.hpp"
#include "point_store.hpp"

using std::cout;
using std::stringstream;
using std::endl;
using std::sqrt;
using std::asin;
using std::cos;
using std::sin;

//code adapted from
//https://www.boost.org/doc/libs/1_77_0/libs/multiprecision/doc/html/boost_multiprecision/tut/input_output.html
bool check_roundtrip(b_float val)
{
    std::stringstream ss;  // Read and write std::stringstream.
    ss.precision(std::numeric_limits<b_float>::max_digits10);  // Ensure all potentially significant bits are output.
    ss.flags(std::ios_base::fmtflags(std::ios_base::scientific)); // Use scientific format.

    ss << val;
    b_float read_val;
    ss >> read_val;
    return val == read_val;
}

void general_test()
{
    //b_float ten = 10;
    //b_float ten_power_ten = pow(ten, 100);
    //b_float eps = b_float(1) / ten_power_ten;
    cout << "Eps: " << EPS << endl;

    /*b_float one = 1;
    b_float three = 3;
    b_float precise_third = one / three;
    cout.precision(110);
    cout << "Precise Third: " << precise_third << endl;*/
    b_float two = 2;
    b_float sqrt_2 = sqrt(two);
    cout << "Sqrt(2): " << sqrt_2 << endl;
    cout << "squared: " << sqrt_2 * sqrt_2 << endl;
    cout << "Size of b_float: " << sizeof(two) << endl;

    cout << "Checking round trips:" << endl;
    cout << "Two: " << check_roundtrip(two) << endl;
    cout << "Sqrt(2): " << check_roundtrip(sqrt_2) << endl;
}

void point_test()
{
    Point p1(b_float(-0.5), b_float(1) / 3);
    cout << "x: " << p1.x() << endl;
    cout << "y: " << p1.y() << endl;
    cout << "p1: " << p1 << endl;

    Point p2(5, 1);
    cout << "p2: " << p2 << endl;
    cout << "p1 + p2: " << p1 + p2 << endl;
    cout << "len of p2: " << p2.norm() << endl;

    b_float neg_third = b_float(-1) / 3;
    cout << "Negative third: " << neg_third << endl;
    cout << "abs of negative third: " << abs(neg_third) << endl;

    cout << "Testing trig:" << endl;
    b_float pi = asin(b_float(1)) * 2;
    cout << "Pi: " << pi << endl;
    b_float theta = pi / 4;
    cout << "Theta: " << theta << endl;

    b_float cos_t = cos(theta);
    b_float sin_t = sin(theta);
    cout << "cos(theta): " << cos_t << endl;
    cout << "sin(theta): " << sin_t << endl;
    cout << "sum of squares: " << (cos_t*cos_t) + (sin_t*sin_t) << endl;
}

void print_nodes(const Walk &w)
{
    set<int>::const_iterator end = w.cend();
    for(set<int>::const_iterator begin = w.cbegin(); begin != end; begin++)
    {
        int node = *begin;
        cout << "Node: " << node << endl;
    }
}

void walk_test()
{
    Walk walk;
    Point p(0.5, 0);
    walk.add_node(0, p);
    cout << "num of nodes: " << walk.size() << endl;
    cout << "coords of node 0: "<< walk.coords(0) << endl;

    walk.add_node(1, Point(1, 2));
    cout << "num of nodes: " << walk.size() << endl;
    walk.add_node(2, Point(-2, 2.5));
    
    cout << "num of nodes: " << walk.size() << endl;
    cout << "coords of node 0: "<< walk.coords(0) << endl;
    cout << "coords of node 1: "<< walk.coords(1) << endl;
    cout << "coords of node 2: "<< walk.coords(2) << endl;

    cout << "Printing nodes: "<< endl;
    print_nodes(walk);

    cout << "has node 1: " << walk.has_node(1) << endl;
    cout << "has node 3: " << walk.has_node(3) << endl;

    cout << "Removing 1" << endl;
    walk.remove_node(1);
    cout << "num of nodes: " << walk.size() << endl;
    cout << "has node 1: " << walk.has_node(1) << endl;
    
    cout << "Printing nodes: "<< endl;
    print_nodes(walk);
    //cout << "coords of node 1: "<< walk.coords(1) << endl;
}

void graph_test()
{
    Graph graph;
    cout << "size: " << graph.size() << endl;

    cout << "Adding node 0" << endl;
    graph.add_node(0);
    cout << "size: " << graph.size() << endl;

    cout << "Has node 1: "<< graph.has_node(1) << endl;
    cout << "Adding node 1" << endl;
    graph.add_node(1);
    cout << "Has node 1: "<< graph.has_node(1) << endl;
    cout << "size: " << graph.size() << endl;

    cout << "Edge between 0 and 1: " << graph.has_edge(0, 1) << endl;

    cout << "Adding edge between 0 and 1: " << endl;
    graph.add_edge(0, 1);
    cout << "Edge between 0 and 1: " << graph.has_edge(0, 1) << endl;

    cout << "Removing node 1" << endl;
    graph.remove_node(1);
    cout << "Has node 1: "<< graph.has_node(1) << endl;
    cout << "size: " << graph.size() << endl;
    cout << "Edge between 0 and 1: " << graph.has_edge(0, 1) << endl;
}

void disp_val_and_key(const b_float &val, int num_decimals)
{
    cout << "Val: " << val << endl;
    int key = get_key(val, num_decimals);
    cout << "Key: " << key << endl << endl;
}

void disp_full_key(const Point &p, int num_decimals)
{   
    cout.flags(std::ios_base::fmtflags(std::ios_base::scientific));
    cout << "point: " << p << endl;
    cout.flags(std::ios_base::fmtflags(std::ios_base::hex));
    cout << "full key: " << get_full_key(p, num_decimals) << endl << endl;
}

void point_store_test()
{
    int num_decimals = 2;

    /*b_float zero(0);
    b_float tenth("0.1");
    b_float tiny("0.00000001");
    b_float neg_tiny("-0.00000001");

    disp_val_and_key(zero, num_decimals);
    disp_val_and_key(tenth, num_decimals); //the key should be 10 (or 9, I guess)
    disp_val_and_key(tiny, num_decimals);
    disp_val_and_key(neg_tiny, num_decimals);
    disp_val_and_key(b_float(-3), num_decimals); //-400
    disp_val_and_key(b_float(5), num_decimals); // 500
    disp_val_and_key(b_float("5.23"), num_decimals); // 523 (0r 522)
    disp_val_and_key(b_float("10.01"), num_decimals); // 1001*/

    //Now test get_full_key
    disp_full_key(Point(0, 0), num_decimals);
    disp_full_key(Point(1, 0), num_decimals);
    disp_full_key(Point(0, 1), num_decimals);
    disp_full_key(Point(1, 1), num_decimals);
}

//with this setup:
//int: 4 bytes
//long: 4 bytes
//long long: 8 bytes

int main()
{
    //These two lines from the boost tutorial for multipleprecision
    cout.precision(std::numeric_limits<b_float>::max_digits10);  // Ensure all potentially significant bits are output.
    cout.flags(std::ios_base::fmtflags(std::ios_base::scientific)); // Use scientific format.

    //point_test();
    //walk_test();
    //graph_test();
    //point_store_test();

    return 0;
}