//#pragma once

#include <iostream>
#include <utility>
//#include <unordered_map>
#include <set>

#include "graph.hpp"

using std::make_pair;
//using std::unordered_map;
using std::set;
using std::cout;
using std::endl;

Graph::Graph(const Graph &g)
{
    //Add all the nodes to this graph
    set<int>::const_iterator node_begin = g.nodes_cbegin();
    set<int>::const_iterator node_end = g.nodes_cend();
    for(; node_begin!=node_end; node_begin++)
    {
        int n = *node_begin;
        add_node(n);
    }

    //Add all the edges to this graph
    set<int> checked_nodes;
    
    node_end = g.nodes_cend();
    int n1;
    for(node_begin = g.nodes_cbegin(); node_begin!=node_end; node_begin++)
    {
        n1 = *node_begin;
        checked_nodes.insert(n1);

        
        set<int>::const_iterator edge_end = g.edges_cend(n1);

        int n2;
        for(set<int>::const_iterator edge_begin = g.edges_cbegin(n1); edge_begin!=edge_end; edge_begin++)
        {
            n2 = *edge_begin;
            //Skip nodes we've already gone over
            //This probably speeds it up
            if(checked_nodes.find(n2) != checked_nodes.end())
            {
                continue;
            }
            //cout << "adding edge to copy" << endl;
            add_edge(n1, n2);
        }
    }
}

bool Graph::has_edge(int n1, int n2) const
{
    if(!(has_node(n1) && has_node(n2)))
    {
        return false;
    }
    //cout << "getting edges at " << n1 << " to check for one"<< endl;
    set<int> adj = edges_from_nodes_.at(n1);
    return adj.find(n2) != adj.end();
}

int Graph::num_edges(int node) const
{
    //cout << "getting edges at " << node << endl;
    return edges_from_nodes_.at(node).size();
}

void Graph::add_edge(int n1, int n2)
{
    //Don't bother to error-check for now
    //cout << "inserting edge between " << n1 << " and " << n2 << endl;
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

    //cout << "removing node " << n << endl;
    set<int> adj_to_n = edges_from_nodes_.at(n);
    //Remove all edges from this node
    edges_from_nodes_.erase(n);

    //Remove this node from other nodes' edges
    for(int adj: adj_to_n)
    {
        //cout << "removing edges from " << adj << endl;
        edges_from_nodes_.at(adj).erase(n);
    }
}

//Return true if every node and edge in g1 is also in g2, false otherwise.
bool equals_one_way(const Graph &g1, const Graph &g2)
{
    for(auto n_i = g1.nodes_cbegin(); n_i != g1.nodes_cend(); n_i++)
    {
        int n1 = *n_i;
        if(!g2.has_node(n1))
        {
            return false;
        }
        auto e_end = g1.edges_cend(n1);
        for(auto e_begin = g1.edges_cbegin(n1); e_begin != e_end; e_begin++)
        {
            int n2 = *e_begin;
            if(!g2.has_edge(n1, n2))
            {
                return false;
            }
        }
    }
    return true;
}

bool operator==(const Graph &g1, const Graph &g2)
{
    return equals_one_way(g1, g2) && equals_one_way(g2, g1);
}

bool operator!=(const Graph &g1, const Graph &g2)
{
    return !(g1 == g2);
}