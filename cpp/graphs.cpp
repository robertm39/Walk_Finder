#include <cmath>
#include <unordered_map>
#include <utility>
#include <iostream>

#include "graphs.hpp"

using std::sqrt;
using std::unordered_map;
using std::make_pair;
using std::cout;
using std::endl;

Point rotated(const Point &p)
{
    b_float sqrt_11 = sqrt(b_float(11));
    b_float x = 5*p.x() - sqrt_11*p.y();
    b_float y = sqrt_11*p.x() + 5*p.y();
    return Point(x, y) / 6;
}

//Return the Moser Spindle, a graph with seven nodes that cannot be 3-colored.
WalkAndGraph get_moser_spindle()
{
    Walk walk;
    Graph graph;

    //Add the points
    Point a(0, 0);
    walk.add_node(0, a);
    graph.add_node(0);

    b_float sqrt_3 = sqrt(b_float(3));
    b_float sqrt_3_over_2 = sqrt_3/2;
    Point b(sqrt_3_over_2, b_float("-0.5"));
    walk.add_node(1, b);
    graph.add_node(1);

    Point c(sqrt_3_over_2, b_float("0.5"));
    walk.add_node(2, c);
    graph.add_node(2);

    Point d(sqrt_3, 0);
    walk.add_node(3, d);
    graph.add_node(3);

    Point e = rotated(b);
    walk.add_node(4, e);
    graph.add_node(4);

    Point f = rotated(c);
    walk.add_node(5, f);
    graph.add_node(5);

    Point g = rotated(d);
    walk.add_node(6, g);
    graph.add_node(6);

    //cout << a << endl;
    //cout << b << endl;
    //cout << c << endl;
    //cout << d << endl;
    //cout << e << endl;
    //cout << f << endl;
    //cout << g << endl;

    //Now add the edges

    //From A
    graph.add_edge(0, 1);
    graph.add_edge(0, 2);
    graph.add_edge(0, 4);
    graph.add_edge(0, 5);

    //From B
    graph.add_edge(1, 2);
    graph.add_edge(1, 3);

    //From C
    graph.add_edge(2, 3);

    //From D
    graph.add_edge(3, 6);

    //From E
    graph.add_edge(4, 5);
    graph.add_edge(4, 6);

    //From F
    graph.add_edge(5, 6);

    //G is already covered
    //cout << "graph constructed" << endl;

    return WalkAndGraph(walk, graph);
}

//Return an equivalent walk and graph, but with the nodes to start from zero and go upward without breaks.
WalkAndGraph rename_nodes(const WalkAndGraph &wg)
{
    const Walk &walk = wg.walk;
    const Graph &graph = wg.graph;

    Walk new_walk;
    Graph new_graph;

    unordered_map<int, int> old_to_new;
    int new_node = 0;
    for(auto i = walk.cbegin(); i != walk.cend(); i++, new_node++)
    {
        int node = *i;
        old_to_new.insert(make_pair(node, new_node));
        new_walk.add_node(new_node, walk.coords(node));
        new_graph.add_node(new_node);

        //Add the edges where we know the new name of the other node
        auto e_end = graph.edges_cend(node);
        for(auto i2 = graph.edges_cbegin(node); i2 != e_end; i2++)
        {
            int node2 = *i2;
            if(old_to_new.count(node2) >= 1)
            {
                //cout << "getting new name for name" << endl;
                int new_node_2 = old_to_new.at(node2);
                new_graph.add_edge(new_node, new_node_2);
            }
        }
    }

    return WalkAndGraph(new_walk, new_graph);
}