#include <iostream>
#include <cmath>
#include <random>

#include "constants.hpp"
#include "point.hpp"
#include "walk.hpp"
#include "graph.hpp"
#include "point_store.hpp"
#include "graphs.hpp"
#include "graph_ops.hpp"

using std::cout;
using std::stringstream;
using std::endl;
using std::sqrt;
using std::asin;
using std::cos;
using std::sin;
using std::default_random_engine;
using std::uniform_int_distribution;
using std::uniform_real_distribution;

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

void point_store_test()
{
    int num_decimals = 0;

    //First test same_place and one_away

    //This is the way to get pi
    //I checked it, and it's accurate to all the significant places
    b_float pi = asin(b_float(1)) * 2;

    //Now test a bunch of random pairs of points
    default_random_engine gen;
    uniform_int_distribution<int> int_dist(-1000, 1000);
    uniform_real_distribution<double> fl_dist(0.0, 1.0);

    cout << "testing" << endl;
    //Test a million pairs
    bool succeeded = true;
    PointStore ps (num_decimals, false, false, true);
    for(int i = 1; i < 10000 + 1; i++)
    {
        if(i % 1000 == 0) //output every 10,000 pairs
        {
            cout << i << endl;
        }

        b_float x1 = int_dist(gen) + fl_dist(gen);
        b_float y1 = int_dist(gen) + fl_dist(gen);

        b_float angle = fl_dist(gen) * 2 * pi;
        b_float r = fl_dist(gen) * 2;
        b_float x2 = x1 + r*cos(angle);
        b_float y2 = y1 + r*sin(angle);

        Point p1(x1, y1);
        Point p2(x2, y2);

        ps.add_node(0, p1);

        //NodeIterators same_it = ps.same_place(p1);
        NodeIterators one_it = ps.within_two(p2);
        if(one_it.cend == one_it.cbegin)
        {
            cout << endl;
            cout << "within two failed:" << endl;
            cout << p1 << endl;
            cout << p2 << endl;
            cout << "dist:" << endl;
            cout << (p2-p1).norm() << endl;
            succeeded = false;
            break; //we failed anyways
        }

        /*if(same_it.cend == same_it.cbegin)
        {
            cout << "same place failed:" << endl;
            cout << p1 << endl;
            succeeded = false;
            break; //we failed anyways
        }
        if(one_it.cend == one_it.cbegin)
        {
            cout << endl;
            cout << "one away failed:" << endl;
            cout << p1 << endl;
            cout << p2 << endl;
            cout << "dist:" << endl;
            cout << (p2-p1).norm() << endl;
            succeeded = false;
            break; //we failed anyways
        }*/
    }
    cout << "succeeded: " << succeeded << endl;
    /*cout << "testing: " << endl;
    bool succeeded = true;
    int divisions_of_degree = 10000;
    for(int i = 0; i < 360 * divisions_of_degree; i++)
    {
        //cout << i << " degrees" << endl;
        b_float rad = (i * pi) / 180 / divisions_of_degree;
        b_float x = cos(rad);
        b_float y = sin(rad);
        Point p(x, y);
        //cout << "getting iterators" << endl;
        NodeIterators its = ps.one_away(p);
        //cout << "counting nodes" << endl;
        int num_nodes = its.cend - its.cbegin;
        if(num_nodes != 1)
        {
            //cout << endl;
            //cout << i << " degrees" << endl;
            //cout << p << endl;
            //cout << "Expected 1 node, got " << num_nodes << endl << endl;
            succeeded = false;
            break;
        }
    }
    cout << "succeeded: " << succeeded << endl;*/
}

void grow_graph_test()
{
    WalkAndGraph moser_spindle = get_moser_spindle();
    Walk &walk = moser_spindle.walk;
    Graph &graph = moser_spindle.graph;

    cout << walk.size() << " nodes" << endl << endl;
    // Test the spindle
    /*for(int n1 = 0; n1 < 6; n1++)
    {
        for(int n2 = n1+1; n2 < 7; n2++)
        {
            if(graph.has_edge(n1, n2))
            {
                Point p1 = walk.coords(n1);
                Point p2 = walk.coords(n2);
                b_float dist = (p2 - p1).norm();
                cout << dist << endl;
            }
        }
    }*/

    grow_graph(walk, graph);
    //cout << walk.size() << " nodes" << endl << endl;
    grow_graph(walk, graph);
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

    //About to do the first real calculation with very high precision
    //unleash the digits
    //105 significant digits
    //eps = 1e-100
    //one hundred digits of accuracy
    //let's see whether these edges are real or fake
    //because twelve digits of accuracy wasn't enough

    //so the edges seem real, but I want more digits
    //two hundred digits of accuracy

    //after checking with two hundred digits of accuracy, the edges are still real
    //so this method actually works to find graphs with many edges per node
    //and maybe it'll find a graph that can't be 4-colored
    //or even one that can't be 5-colored

    //but let's add some more digits just for fun
    //I've checked the edges up to 300 digits
    //it is so, so unlikely that they aren't real
    //so I'm basically certain that they are real now

    //let's move the number of significant digits down to a more manageable 105
    //and epsilon to 1e-100

    grow_graph_test();

    return 0;
}