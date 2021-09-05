#pragma once

#include "constants.hpp"
#include "walk.hpp"
#include "graph.hpp"
#include "point.hpp"
#include "walk_and_graph.hpp"

WalkAndGraph get_moser_spindle();
WalkAndGraph rename_nodes(const WalkAndGraph&);