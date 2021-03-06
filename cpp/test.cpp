#include <iostream>
#include <cmath>
#include <random>
#include <time.h>

#include "constants.hpp"
#include "point.hpp"
#include "walk.hpp"
#include "graph.hpp"
#include "point_store.hpp"
#include "graphs.hpp"
#include "graph_ops.hpp"
#include "save_load.hpp"

using std::cout;
using std::stringstream;
using std::to_string;
using std::endl;
using std::sqrt;
using std::asin;
using std::cos;
using std::sin;
using std::default_random_engine;
using std::uniform_int_distribution;
using std::uniform_real_distribution;
using std::time;

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
    grow_graph(walk, graph);
    grow_graph(walk, graph);
}

void save_load_test()
{
    WalkAndGraph moser_spindle = get_moser_spindle();
    Walk &walk = moser_spindle.walk;
    Graph &graph = moser_spindle.graph;

    cout << "saving" << endl;
    save(walk, graph, "spindle_save_test.txt", true);
    cout << "loading" << endl;
    WalkAndGraph loaded = load("spindle_save_test.txt");
    cout << "loaded" << endl;

    Walk &walk2 = loaded.walk;
    Graph &graph2 = loaded.graph;

    cout << "walk == walk: " << (walk == walk) << endl;
    cout << "graph == graph: " << (graph == graph) << endl;
    cout << "walk == walk2: " << (walk == walk2) << endl;
    cout << "graph == graph2: " << (graph == graph2) << endl;
}

//Repeatedly grow and prune a graph.
//just have all the filenames have a number at the end
//time code borrowed from
//https://stackoverflow.com/questions/997946/how-to-get-current-time-and-date-in-c
void grow_and_prune()
{

    cout.precision(5);  // Ensure all potentially significant bits are output.
    cout.flags(std::ios_base::fmtflags(std::ios_base::fixed)); // Use scientific format.

    cout << "timing growing and pruning" << endl;

    //Time this for optimization
    double total_time = 0;
    int num_samples = 5;

    for(int samples = 0; samples < num_samples; samples++)
    {
        time_t start = time(nullptr);

        //WalkAndGraph wg = get_moser_spindle();
        //WalkAndGraph wg = get_small_triangle();
        WalkAndGraph wg = get_points_on_line();
        //WalkAndGraph wg = get_two_points();
        //WalkAndGraph wg = get_two_square_points();

        Walk &walk = wg.walk;
        Graph &graph = wg.graph;
        cout << "growing and pruning eleven points" << endl;

        //string filename = "square\\square";

        //save(walk, graph, filename + "_0.txt", true);

        //Keep going until it gets too big
        //for(int i = 1; i<2; i++)
        for(int i = 1; walk.size() <= 500; i++) //do one more
        {
            grow_graph(walk, graph);
            //filename += "_b";
            //save(walk, graph, filename + "_" + to_string(i) + "_full.txt", true);

            int prune = 0;
            WalkAndGraph pruned = get_max_pruned_graph(walk, graph, prune);
            walk = pruned.walk;
            graph = pruned.graph;

            //cout << "Pruned to " << prune << " edges per node," << endl;
            cout << walk.size() << " nodes left." << endl;// << endl;
            //filename += "_p" + to_string(prune);
            //save(walk, graph, filename + "_" + to_string(i) + "_p" + to_string(prune) + ".txt", true);
        }
        time_t end = time(nullptr);
        double elapsed_seconds = end-start;
        total_time += elapsed_seconds;
        cout << "growing and pruning took " << elapsed_seconds << " seconds" << endl;
    }

    double average_time = total_time / num_samples;
    cout << endl << "Average time: " << average_time << endl;
}

void graph_stats(const string &filename)
{
    cout.precision(5);  // Ensure all potentially significant bits are output.
    cout.flags(std::ios_base::fmtflags(std::ios_base::fixed)); // Use scientific format.

    WalkAndGraph wg = load(filename);
    const Walk &w = wg.walk;
    const Graph &g = wg.graph;

    cout << w.size() << " nodes," << endl;

    int num_edges = 0;
    for(auto i1 = w.cbegin(); i1 != w.cend(); i1++)
    {
        num_edges += g.num_edges(*i1);
    }
    double edges_per_node = double(num_edges) / w.size();
    num_edges /= 2; //The edges were double-counted
    cout << num_edges << " edges, " << endl;
    cout << edges_per_node << " edges per node on average" << endl;
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

    //it works

    //grow_graph_test();
    //save_load_test();
    
    grow_and_prune();
    //graph_stats("moser_spindle_b_p4_b_p4_b_p6_b_p8_b_p8_b_p10.txt");

    return 0;
}