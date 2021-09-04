#pragma once

#include "constants.hpp"
#include "walk.hpp"
#include "graph.hpp"
#include "point.hpp"
#include "save_load.hpp"
#include "walk_and_graph.hpp"
#include "point_store.hpp"

void grow_graph(Walk&, Graph&);
void prune_graph(Walk&, Graph&);