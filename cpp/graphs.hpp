#pragma once

#include "constants.hpp"
#include "walk.hpp"
#include "graph.hpp"
#include "point.hpp"
#include "walk_and_graph.hpp"

WalkAndGraph get_moser_spindle();
WalkAndGraph get_small_triangle();
WalkAndGraph get_points_on_line();
WalkAndGraph get_two_points();
WalkAndGraph rename_nodes(const WalkAndGraph&);