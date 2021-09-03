#pragma once

#include <string>

#include "walk.hpp"
#include "graph.hpp"
#include "walk_and_graph.hpp"

using std::string;

void save(const Walk&, const Graph&, const string&, bool);
WalkAndGraph load(const string&);