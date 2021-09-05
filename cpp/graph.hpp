#pragma once

#include <unordered_map>
#include <set>

using std::unordered_map;
using std::set;

//Mostly tested and worked
class Graph
{
    private:
        unordered_map<int, set<int>> edges_from_nodes_;
        set<int> nodes_;
    public:
        Graph() {} //Just construct the graph after making it for ease of coding
        Graph(const Graph&); //Have a copy constructor instead of a copy method
        int size() const {return nodes_.size();}
        bool has_node(int n) const {return nodes_.find(n) != nodes_.end();}
        bool has_edge(int, int) const;
        int num_edges(int) const;
        void add_edge(int, int);

        void add_node(int);
        void remove_node(int);

        //Iterators for iterating over the edges of a node
        set<int>::iterator edges_begin(int n) {return edges_from_nodes_.at(n).begin();}
        set<int>::iterator edges_end(int n) {return edges_from_nodes_.at(n).end();}

        set<int>::const_iterator edges_cbegin(int n) const {return edges_from_nodes_.at(n).cbegin();}
        set<int>::const_iterator edges_cend(int n) const {return edges_from_nodes_.at(n).cend();}

        //Iterators for iterating over the nodes
        set<int>::iterator nodes_begin() {return nodes_.begin();}
        set<int>::iterator nodes_end() {return nodes_.end();}

        //I won't actually use these
        /*set<int>::reverse_iterator n_rbegin() {return nodes_.rbegin();}
        set<int>::reverse_iterator n_rend() {return nodes_.rend();}*/
        set<int>::const_iterator nodes_cbegin() const {return nodes_.cbegin();}
        set<int>::const_iterator nodes_cend() const {return nodes_.cend();}
        /*set<int>::const_reverse_iterator n_crbegin() const {return nodes_.crbegin();}
        set<int>::const_reverse_iterator n_crend() const {return nodes_.crend();}*/
};