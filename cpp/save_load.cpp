#include <string>
#include <fstream>
#include <filesystem>

#include "walk.hpp"
#include "graph.hpp"
#include "walk_and_graph.hpp"
#include "constants.hpp"

using std::string;
using std::ifstream;
using std::ofstream;
using std::stringstream;
using std::cout;
using std::endl;

bool exists(const string &filename)
{
    ifstream test;
    test.open(filename);
    return bool(test);
}

void save(const Walk &walk, const Graph &graph, const string &filename, bool overwrite=false)
{
    //If the file already exists and we're not supposed to overwrite, return
    cout << "checking for file" << endl;
    if(exists(filename) && !overwrite)
    {
        return;
    }

    ofstream f_out;
    f_out.open(filename);

    f_out.precision(std::numeric_limits<b_float>::max_digits10);  // Ensure all potentially significant bits are output.
    f_out.flags(std::ios_base::fmtflags(std::ios_base::scientific)); // Use scientific format.
    //Make the format the same as for the python files, but with more digits
    
    //Write the nodes
    f_out << "NODES" << endl;
    //cout << "saving nodes" << endl;
    //set<int>::const_iterator n_begin = walk.cbegin();
    set<int>::const_iterator n_end = walk.cend();
    int node = 0;
    for(set<int>::const_iterator n_begin = walk.cbegin(); n_begin != n_end; n_begin++)
    {
        node = *n_begin;
        //cout << "saving node "<< node << endl;
        f_out << node << " " << walk.coords(node) << endl;
    }

    //Write the edges
    f_out << "EDGES" << endl;
    //cout << endl << "saving edges" << endl;

    //fix this so it doesn't save redundant edges
    n_end = graph.nodes_cend();
    for(set<int>::const_iterator n_begin = graph.nodes_cbegin(); n_begin != n_end; n_begin++)
    {
        node = *n_begin;
        //cout << "saving edges for node " << node << endl;
        set<int>::const_iterator e_end = graph.edges_cend(node);
        for(set<int>::const_iterator e_begin = graph.edges_cbegin(node); e_begin != e_end; e_begin++)
        {
            int n2 = *e_begin;
            if(n2 <= node)
            {
                continue;
            }
            //cout << "saving edge between node " << node << " and node " << n2 << endl;
            f_out << node << " " << n2 << endl;
        }
    }

    f_out << "DONE";
}

WalkAndGraph load(const string &filename)
{
    ifstream f_in;
    f_in.open(filename);

    string line;
    getline(f_in, line); //Skip the "NODES" line

    Walk walk;
    Graph graph;

    getline(f_in, line);
    while(line != "EDGES")
    {
        stringstream s_line(line);
        int node;
        s_line >> node;

        b_float x;
        s_line >> x;

        b_float y;
        s_line >> y;

        Point p(x, y);
        walk.add_node(node, p);
        graph.add_node(node);
        
        getline(f_in, line);
    }

    //The "EDGES" line has already been consumed, don't consume it again here
    getline(f_in, line);
    while(line != "DONE")
    {
        stringstream s_line(line);
        int n1, n2;
        s_line >> n1;
        s_line >> n2;

        graph.add_edge(n1, n2);
        
        getline(f_in, line);
    }

    return WalkAndGraph(walk, graph);
}