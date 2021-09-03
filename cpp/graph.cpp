#pragma once

#include <utility>
#include <map>
#include <set>

#include "graph.hpp"

using std::make_pair;
using std::map;
using std::set;

Graph::Graph(const Graph &g)
{
    //Add all the nodes to this graph
    set<int>::const_iterator node_begin = g.nodes_cbegin();
    set<int>::const_iterator node_end = g.nodes_cend();
    for(int n = *node_begin; node_begin!=node_end; node_begin++)
    {
        add_node(n);
    }

    //Add all the edges to this graph
    set<int> checked_nodes;
    set<int>::const_iterator node_begin = g.nodes_cbegin();
    set<int>::const_iterator node_end = g.nodes_cend();
    for(int n1 = *node_begin; node_begin!=node_end; node_begin++)
    {
        checked_nodes.insert(n1);

        set<int>::const_iterator edge_begin = g.edges_cbegin(n1);
        set<int>::const_iterator edge_end = g.edges_cend(n1);

        for(int n2 = *edge_begin; edge_begin!=edge_end; edge_begin++)
        {
            //Skip nodes we've already gone over
            //This probably speeds it up
            if(checked_nodes.find(n2) != checked_nodes.end())
            {
                continue;
            }
            add_edge(n1, n2);
        }
    }
}

bool Graph::has_edge(int n1, int n2) const
{
    set<int> adj = edges_from_nodes_.at(n1);
    return adj.find(n2) != adj.end();
}

void Graph::add_edge(int n1, int n2)
{
    //Don't bother to error-check for now
    edges_from_nodes_.at(n1).insert(n2);
    edges_from_nodes_.at(n2).insert(n1);
}

void Graph::add_node(int n)
{
    nodes_.insert(n);
    set<int> adj;
    edges_from_nodes_.insert(make_pair(n, adj));
}

void Graph::remove_node(int n)
{
    nodes_.erase(n);
    set<int> adj_to_n = edges_from_nodes_.at(n);
    //Remove all edges from this node
    edges_from_nodes_.erase(n);

    //Remove this node from other nodes' edges
    for(int adj: adj_to_n)
    {
        edges_from_nodes_.at(adj).erase(n);
    }
}