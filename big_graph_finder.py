# -*- coding: utf-8 -*-
"""
Created on Tue Aug 31 18:11:13 2021

@author: rober
"""

import numpy as np

import walk_builder

import file_reader

from constants import EPS

import point_store

# EPS = 1e-10

class ColoringState:
    def __init__(self,
                 graph,
                 n_colors=None,
                 uncolored=None,
                 colorings=None,
                 nodes_from_numbers=None,
                 possible_colors_from_nodes=None):
        if n_colors is None:
            n_colors = 5
        if uncolored is None:
            uncolored = set(graph)
        if colorings is None:
            colorings = dict()
        if nodes_from_numbers is None:
            nodes_from_numbers = {n: set() for n in range(n_colors)}
            nodes_from_numbers[n_colors] = set(graph)
        if possible_colors_from_nodes is None:
            possible_colors_from_nodes = {n: set(range(n_colors)) for n in graph}
        
        self.graph = graph
        self.n_colors = n_colors
        self.uncolored = uncolored
        self.colorings = colorings
        self.nodes_from_numbers = nodes_from_numbers
        self.possible_colors_from_nodes = possible_colors_from_nodes
    
    def copy(self):
        uncolored = self.uncolored.copy()
        colorings = self.colorings.copy()
        # nodes_from_numbers = {n:s.copy() for n, s in self.nodes_from_numbers}
        nodes_from_numbers = dict()
        for num, nodes in self.nodes_from_numbers.items():
            nodes_from_numbers[num] = nodes.copy()
        possible_colors_from_nodes = dict()
        for node, colors in self.possible_colors_from_nodes.items():
            possible_colors_from_nodes[node] = colors.copy()
        # possible_colors_from_nodes = self.possible_colors_from_nodes.copy()
        return ColoringState(self.graph,
                             self.n_colors,
                             uncolored,
                             colorings,
                             nodes_from_numbers,
                             possible_colors_from_nodes)
    
    def set_color(self, node, color):
        if not node in self.graph:
            raise ValueError('Node not in graph: {}'.format(node))
        
        self.uncolored.remove(node)
        self.colorings[node] = color
        num = len(self.possible_colors_from_nodes[node])
        self.nodes_from_numbers[num].remove(node)
        self.possible_colors_from_nodes[node] = {color}
        for o_n in self.graph.adjacent(node):
            if o_n in self.colorings:
                #o_n is already colored, so to avoid a key error, continue
                continue
            if not color in self.possible_colors_from_nodes[o_n]:
                continue
            num_colors = len(self.possible_colors_from_nodes[o_n])
            self.nodes_from_numbers[num_colors].remove(o_n)
            self.nodes_from_numbers[num_colors - 1].add(o_n)
            self.possible_colors_from_nodes[o_n].discard(color)

    def rule_out_color(self, node, color):
        if not node in self.graph:
            raise ValueError('Node not in graph: {}'.format(node))
        
        if not color in self.possible_colors_from_nodes[node]:
            return
        
        num = len(self.possible_colors_from_nodes[node])
        self.nodes_from_numbers[num].remove(node)
        self.nodes_from_numbers[num-1].add(node)
        self.possible_colors_from_nodes[node].discard(color)

def do_initial_coloring(graph, c_state):
    """
    Color in a mutually connected triangle of nodes. No loss of generality.
    """
    checked = set()
    for n1 in graph:
        checked.add(n1)
        for n2 in graph.adjacent(n1):
            for n3 in graph.adjacent(n2):
                if n3 in checked:
                    continue
                if graph.has_edge(n3, n1):
                    #We've found a triangle
                    c1 = next(iter(c_state.possible_colors_from_nodes[n1]))
                    c_state.set_color(n1, c1)
                    
                    c2 = next(iter(c_state.possible_colors_from_nodes[n2]))
                    c_state.set_color(n2, c2)
                    
                    c3 = next(iter(c_state.possible_colors_from_nodes[n3]))
                    c_state.set_color(n3, c3)
                    
                    return

class ColoringHypothetical:
    """
    A hypothetical coloring of a node, along with the state before it.
    """
    def __init__(self, coloring_state, node, color):
        self.coloring_state = coloring_state.copy()
        self.node = node
        self.color = color

#Want to find a graph that can't be five-colored
#I need to change this so it doesn't use recursion
def color_graph(graph, n_colors=5):
    c_state = ColoringState(graph, n_colors=n_colors)
    
    hypotheticals = list()
    
    while True: #This will end
        if not c_state.uncolored: #It's all colored
            return c_state.colorings
        
        numbers_of_colors = sorted(list(set(c_state.nodes_from_numbers)))
        for num in numbers_of_colors:
            nodes = c_state.nodes_from_numbers[num]
            if not nodes:
                continue
            
            if num == 0:
                #There are no colors to color this node with,
                #so pop the current hypothetical if there is one,
                #or fail if there isn't.
                if hypotheticals:
                    #Pop the current hypothetical and rule out its premise.
                    ch = hypotheticals.pop()
                    c_state = ch.coloring_state
                    c_state.rule_out_color(ch.node, ch.color)
                    break #Go back to the top and iterate again
                else:
                    return False #We failed to color the graph
            
            if num == 1:
                #No need for a hypothetical, just set the color
                node = next(iter(nodes))
                color = next(iter(c_state.possible_colors_from_nodes[node]))
                c_state.set_color(node, color)
                break #Go back to the top and iterate again
            
            else:
                #num >= 2
                #we need to make a hypothetical
                #which now doesn't involve any recursion
                node = next(iter(nodes))
                color = next(iter(c_state.possible_colors_from_nodes[node]))
                hypothetical = ColoringHypothetical(c_state, node, color)
                hypotheticals.append(hypothetical)
                
                c_state.set_color(node, color)

# def color_graph(graph=None, n_colors=None, c_state=None):
    
#     if c_state is None:
#         if graph is None:
#             raise ValueError('Both arguments are none')
        
#         # print('n_colors: {}'.format(n_colors))
#         c_state = ColoringState(graph, n_colors=n_colors)
        
#         #This will save a lot of time when a coloring is impossible
#         do_initial_coloring(graph, c_state)
    
#     #Everything is initialized now
#     while True: #This will end
#         if not c_state.uncolored: #The whole thing is colored
#             return c_state.colorings
    
#         numbers_of_colors = sorted(list(set(c_state.nodes_from_numbers)))
#         for num in numbers_of_colors:
            
#             nodes = c_state.nodes_from_numbers[num]
#             if not nodes:
#                 continue
            
#             if num == 0:
#                 #There are no colors to color it with
#                 #we failed
#                 return False
            
#             node = next(iter(nodes))
#             colors = c_state.possible_colors_from_nodes[node]
#             color = next(iter(colors))
            
#             #No need for recursion
#             #if this fails, the whole thing fails
#             if num == 1:
#                 c_state.set_color(node, color)
#             #There's more than one color
#             else:
#                 copy_c_state = c_state.copy()
#                 copy_c_state.set_color(node, color)
#                 s_result = color_graph(graph, c_state=copy_c_state)
#                 if s_result:
#                     return s_result
#                 #It didn't work, so that color doesn't work for this node
#                 c_state.rule_out_color(node, color)
            
#             #This loop is only supposed to do one step at a time
#             break

def reduce_graph(graph, n_colors):
    """
    Iteratively remove all nodes with fewer edges than n_colors.
    This does not change whether the graph can be colored with n colors.
    """
    changed = True
    while changed:
        changed = False
        nodes = set(graph)
        print('Remain {} nodes'.format(len(nodes)))
        for node in nodes:
            num_edges = len(graph.adjacent(node))
            if num_edges < n_colors:
                graph.remove_node(node)
                changed = True
        
        #Check to see if edges were removed correctly
        if not check_graph(graph):
            raise ValueError('Edges were removed wrong')
    
    if not check_num_edges(graph, n_colors):
        raise ValueError('Nodes remaining without enough edges')
    
    print('Done')

def check_graph(graph):
    """
    Verify that all edges in the given graph are between nodes in the graph.
    """
    for n1 in graph:
        for n2 in graph.adjacent(n1):
            if not n2 in graph:
                return False
    return True

def check_num_edges(graph, n_edges):
    """
    Verify that all nodes in the given graph have at least n_edges edges.
    """
    for node in graph:
        adj = graph.adjacent(node)
        if len(adj) < n_edges:
            return False
    return True

def verify_colorable(graph, n_colors):
    #We're gonna considerably change the graph, so make a copy
    graph = graph.copy()
    reduce_graph(graph, n_colors)
    
    #The graph turned out to be empty, so it can be colored
    if len(graph) == 0:
        return True
    
    # print('Finding coloring')
    return bool(color_graph(graph=graph, n_colors=n_colors))

def get_heule_subwalk(offset=0):
    """
    Return a subwalk containing the heule graph, and the edges.
    """
    edges = file_reader.edges_from_file('heule_529.txt', offset=offset)
    
    coords_from_nodes = dict()    
    
    with open('calc_coords_529_good.txt') as file:
        for i, line in enumerate(file):
            # line = line.replace(']', '')
            # line = line.replace('[', '')
            x, y = line.split()
            x, y = float(x), float(y)
            coords_from_nodes[i+offset] = walk_builder.coords(x, y)
    
    subwalk = walk_builder.SubWalk(coords_from_nodes)
    return subwalk, edges

#Improve this to use PointStore
def add_new_nodes(walk, graph, ps1=None, ps2=None, eps=EPS):
    """
    Add all points at unit distance from at least two points in the graph.
    Add all edges, even incidental ones.
    """
    #I can tweak the number of decimals for optimization
    
    if ps1 is None:
        num_decimals = 2
        ps1 = point_store.PointStore(num_decimals=num_decimals)
        ps2 = point_store.PointStore(num_decimals=0,
                                      unit=False,
                                      same=False,
                                      two=True)
        
        # print('Initializing Point Store')
        #Initialize the point store
        for node, coords in walk.items():
            ps1[coords] = node
            ps2[coords] = node
            
        # print('Point Store initialized')
    
    new_points = list()
    
    #Now use the second PointStore to only look at point that could be 
    #within two
    checked = set()
    
    for n1, c1 in walk.items():
        checked.add(n1)
        for c2, n2 in ps2.get_entries_within_two(c1):
            if n2 in checked:
                continue
            
            #We still need to check because the PointStore is imprecise
            diff = c2 - c1
            dist = np.hypot(*diff)
            #The two nodes are distance two apart
            #So the point at unit distance from both is their midpoint
            if np.isclose(dist, 2.0, rtol=0, atol=EPS):
                half_diff = diff / 2.0
                midpoint = c1 + half_diff
                new_points.append(midpoint)
            elif dist > 2.0: #They're too far apart
                pass
            else: #Their distance is less than two
                half_diff = diff / 2.0
                midpoint = c1 + half_diff
                dx, dy = diff[0], diff[1]
                qv = walk_builder.coords(-dy, dx)
                qv = qv / dist #The length of q is the length of diff, ie dist.
                q_len = np.sqrt(1 - (dist*dist / 4))
                qv = qv * q_len
                
                #Now we have the q vector
                p1 = midpoint + qv
                p2 = midpoint - qv
                new_points.append(p1)
                new_points.append(p2)
    
    
    # for n1, c1 in walk.items():
    #     checked.add(n1)
    #     for n2, c2 in walk.items():
    #         if n2 in checked:
    #             continue
    #         diff = c2 - c1
    #         dist = np.hypot(*diff)
    #         #The two nodes are distance two apart
    #         #So the point at unit distance from both is their midpoint
    #         # if np.allclose(dist, 2.0, rtol=0, atol=EPS):
    #         if np.isclose(dist, 2.0, rtol=0, atol=EPS):
    #             half_diff = diff / 2.0
    #             midpoint = c1 + half_diff
    #             new_points.append(midpoint)
    #         elif dist > 2.0: #They're too far apart
    #             pass
    #         else: #Their distance is less than two
    #             half_diff = diff / 2.0
    #             midpoint = c1 + half_diff
    #             dx, dy = diff[0], diff[1]
    #             qv = walk_builder.coords(-dy, dx)
    #             qv = qv / dist #The length of q is the length of diff, ie dist.
    #             q_len = np.sqrt(1 - (dist*dist / 4))
    #             qv = qv * q_len
                
    #             #Now we have the q vector
    #             p1 = midpoint + qv
    #             p2 = midpoint - qv
    #             new_points.append(p1)
    #             new_points.append(p2)
    
    #Find the highest node, and count up from there
    #Put the nodes into the walk and 
    max_node = max(walk)
    current_node = max_node + 1
    
    using_point_store=True
    
    for c1 in new_points:
        
        #Find all nodes unit distance from this node and add the edges
        #This node is not in the walk, so no need to check for that
        
        if using_point_store:
            #See if this node is in the same place as any others
            duplicate = False
            for c2, n2 in ps1.get_entries_in_same_place(c1):
                diff = c2 - c1
                dist = np.hypot(*diff)
                
                # if np.allclose(dist, 0.0, rtol=0, atol=eps):
                if np.isclose(dist, 0.0, rtol=0, atol=eps):
                    duplicate = True
                    break
            
            if duplicate:
                continue
            
            adjacent_nodes = list()
            #Here's where the point store comes in handy
            #First, find the nodes one away
            for c2, n2 in ps1.get_entries_one_away(c1):
                diff = c2 - c1
                dist = np.hypot(*diff)
                
                #I still need to test because the point store isn't exact
                #but this way, I only check a few nodes instead of all of them
                #Add an edge if they have unit distance
                # if np.allclose(dist, 1.0, rtol=0, atol=eps):
                if np.isclose(dist, 1.0, rtol=0, atol=eps):
                    adjacent_nodes.append(n2)
                    # graph.add_edge(current_node, n2)
        
        #Here's the old code, to test if they're the same
        else:
            adjacent_nodes = []
            duplicate = False
            for n2, c2 in walk.items():
                diff = c2 - c1
                dist = np.hypot(*diff)
                
                #Add an edge if they have unit distance
                # if np.allclose(dist, 1.0, rtol=0, atol=EPS):
                if np.isclose(dist, 1.0, rtol=0, atol=EPS):
                    adjacent_nodes.append(n2)
                    # graph.add_edge(current_node, n2)
                #We have a duplicate
                # elif np.allclose(dist, 0.0, rtol=0, atol=EPS):
                elif np.isclose(dist, 0.0, rtol=0, atol=EPS):
                    duplicate = True
                    break
            if duplicate:
                continue
        
        graph.add_node(current_node)
        for n2 in adjacent_nodes:
            graph.add_edge(current_node, n2)
    
        walk.add_node(current_node, c1)
        ps1[c1] = current_node
        ps2[c1] = current_node
        
        current_node += 1
    
    new_edges = 0
    for node in walk:
        if node <= max_node:
            continue #Only check new nodes
        new_edges += len(graph.adjacent(node))

    num_new_nodes = len(walk) - max_node - 1
    s = '{} new nodes, {} new edges, {} average edges per new node'
    print(s.format(num_new_nodes, new_edges, new_edges/num_new_nodes))
    
    return ps1, ps2

# def new_indices(graph_1, graph_2, splice_pairs):
#     """
#     Return the new indices 
#     """
#     splice_pairs_less = 0
#     removed_numbers = [n2 for n1, n2 in splice_pairs]
    
#     subs = {n2:n1 for n1, n2 in splice_pairs}
#     result = dict()
    
#     removed_numbers_iter = iter(nodes)
#     nums_iter = iter(range())
#     current_number = 0
    
#     try:
#         current_next_to_remove = next(removed_numbers_iter)
        
#     except StopIteration:
#         pass
    
#     return result

def splice_graph(sw1, sw2, cn1_1, cn1_2, cn2_1, cn2_2, edges):
    """
    Return a subwalk gotten by identifying cn1_1 with cn1_2
    and cn2_1 with cn2_2, along with the edges.
    """
    pass

def spindle_subwalk(sw1, sw2, cn1, cn2, ln1, ln2, edges):
    """
    Return a subwalk gotten by identifying cn1 and cn2 and linking ln1 and ln2,
    along with the new edges.
    The subwalks must have no nodes in common.
    """
    pass