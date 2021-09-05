#include <unordered_set>
#include <iostream>

#include "graph_ops.hpp"
#include "graphs.hpp"

using std::unordered_set;
using std::cout;
using std::endl;
using std::stringstream;

//It'll be fine to allocate a new PointStore every time this is called
void grow_graph(Walk &walk, Graph &graph)
{
    PointStore one_and_same_ps(2, true, true, false);
    PointStore within_two_ps(0, false, false, true);

    //Put the nodes into the point stores.
    for(auto begin = walk.cbegin(); begin != walk.cend(); begin++)
    {
        int node = *begin;
        one_and_same_ps.add_node(node, walk.coords(node));
        within_two_ps.add_node(node, walk.coords(node));
    }

    vector<Point> new_points;
    
    //Add the points
    unordered_set<int> checked;
    for(auto i1 = walk.cbegin(); i1 != walk.cend(); i1++)
    {
        int n1 = *i1;
        checked.insert(n1);
        Point p1 = walk.coords(n1);
        //cout << "node: " << n1 << endl;
        NodeIterators its = within_two_ps.within_two(p1);
        for(; its.cbegin != its.cend; its.cbegin++)
        {
            int n2 = *its.cbegin;
            if(checked.count(n2) >= 1)
            {
                continue;
            }
            //cout << n1 << " within two of " << n2 << endl;

            Point p2 = walk.coords(n2);
            Point diff = p2 - p1;
            b_float dist = diff.norm();

            if(same(dist, 2))
            {
                //The two nodes are at distance two apart
                //so the point at unit distance from both is their midpoint
                Point midpoint = p1 + (diff / 2.0);
                new_points.push_back(midpoint);
            } else if (dist <= 2.0) {
                //The two points have a distance of less than two
                //There are two points both at unit distance from them
                Point midpoint = p1 + (diff / 2.0);

                //The normal, perpendicular
                Point q_norm = (diff.perp()) / dist;
                b_float q_len = sqrt(1 - (dist * dist / 4));
                Point q = q_norm * q_len;
                new_points.push_back(midpoint + q);
                new_points.push_back(midpoint - q);
            }
        }
    }

    //Look for connections and duplicates
    //this is also when the new points are assigned to nodes
    int n1 = walk.size(); //This is the first node not already in walk
    int old_size = walk.size();

    int nodes_added = 0;
    int edges_added = 0;
    for(const Point &p: new_points)
    {
        //See if this point is a duplicate of any points, old or already-processed new
        bool is_duplicate = false;
        NodeIterators it = one_and_same_ps.same_place(p);
        for(; it.cbegin != it.cend; it.cbegin++)
        {
            int n2 = *it.cbegin;
            Point p2 = walk.coords(n2);
            if(same(p.x(), p2.x()) && same(p.y(), p2.y()))
            {
                //They're both the same
                //just don't add this one
                //and don't keep checking for other points it could be the same as
                //cout << "found duplicate" << endl;
                is_duplicate = true;
                break;
            }
        }
        if(is_duplicate)
        {
            //Just don't add this point
            continue;
        }
        //The point is not a duplicate, so we'll add it
        walk.add_node(n1, p);
        graph.add_node(n1);
        nodes_added++;

        //Search for nodes it could be a unit distance from
        it = one_and_same_ps.one_away(p);
        for(; it.cbegin != it.cend; it.cbegin++)
        {
            int n2 = *it.cbegin;
            b_float dist = (walk.coords(n2) - p).norm();
            //cout << "dist: " << endl;
            //cout << dist << endl << endl;
            if(same(dist, 1.0))
            {
                //The node is a distance of one away, so put an edge between them
                //when you do this, you only check nodes that have already been put into the point store
                //so it won't double up (this is just a performance concern anyways)
                graph.add_edge(n1, n2);
                edges_added++;
            }
        }
        //Now update the point store and the node number
        //(the within_two point store isn't gonna be used any more, so don't bother to update it)
        one_and_same_ps.add_node(n1, p);

        n1++;
    }

    int edges_each_node = 0; //Count each edge once for each of the new nodes it's in
    for(int i = old_size; i < old_size + nodes_added; i++)
    {
        //cout << "counting edges for " << i << endl;
        edges_each_node += graph.num_edges(i);
    }

    double edges_per_new_node = double(edges_each_node) / nodes_added;
    stringstream edges_per_ss;
    edges_per_ss.precision(5);
    edges_per_ss.flags(std::ios_base::fmtflags(std::ios_base::fixed)); // use fixed format
    edges_per_ss << edges_per_new_node;
    string edges_per_string;
    edges_per_ss >> edges_per_string;

    cout << nodes_added << " new nodes, " << edges_added << " new edges, " << edges_per_string << " edges per new node."<< endl;
}

//Prune the graph until all nodes have at least a certain number of edges.
void prune_graph(Walk &walk, Graph &graph, int min_edges)
{
    bool changed = false;
    do
    {
        changed = false;
        vector<int> to_remove;
        for(auto i1 = walk.cbegin(); i1 != walk.cend(); i1++)
        {
            int node = *i1;
            if(graph.num_edges(node) < min_edges)
            {
                //This node does not have enough edges, so prune it away
                to_remove.push_back(node);
                changed = true;
            }
        }
        for(int node: to_remove)
        {
            walk.remove_node(node);
            graph.remove_node(node);
        }
    } while (changed);
    
}

WalkAndGraph get_max_pruned_graph(Walk &walk, Graph &graph, int &prune)
{
    Walk prev_walk;
    Graph prev_graph;

    for(; walk.size() > 0;prune++)
    {
        prev_walk = walk;
        prev_graph = graph;
        prune_graph(walk, graph, prune);
    }
    prune -= 2; //This number has stepped beyond the correct value by two
    return rename_nodes(WalkAndGraph(prev_walk, prev_graph));
}