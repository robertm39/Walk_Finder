#pragma once

#include "walk.hpp"
#include "graph.hpp"

class WalkAndGraph
{
    public:
        Walk walk;
        Graph graph;
        WalkAndGraph(Walk w, Graph g): walk(w), graph(g) {}
};