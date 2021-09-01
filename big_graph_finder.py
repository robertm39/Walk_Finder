# -*- coding: utf-8 -*-
"""
Created on Tue Aug 31 18:11:13 2021

@author: rober
"""

import queue

import walk_builder

import file_reader

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

#Want to find a graph that can't be five-colored
def color_graph(graph=None, n_colors=None, c_state=None):
    
    if c_state is None:
        if graph is None:
            raise ValueError('Both arguments are none')
        
        # print('n_colors: {}'.format(n_colors))
        c_state = ColoringState(graph, n_colors=n_colors)
    
    #Everything is initialized now
    while True: #This will end
        if not c_state.uncolored: #The whole thing is colored
            return c_state.colorings
    
        numbers_of_colors = sorted(list(set(c_state.nodes_from_numbers)))
        for num in numbers_of_colors:
            
            nodes = c_state.nodes_from_numbers[num]
            if not nodes:
                continue
            
            if num == 0:
                #There are no colors to color it with
                #we failed
                return False
            
            node = next(iter(nodes))
            colors = c_state.possible_colors_from_nodes[node]
            color = next(iter(colors))
            
            #No need for recursion
            #if this fails, the whole thing fails
            if num == 1:
                c_state.set_color(node, color)
            #There's more than one color
            else:
                copy_c_state = c_state.copy()
                copy_c_state.set_color(node, color)
                s_result = color_graph(graph, c_state=copy_c_state)
                if s_result:
                    return s_result
                #It didn't work, so that color doesn't work for this node
                c_state.rule_out_color(node, color)
            
            #This loop is only supposed to do one step at a time
            break

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

def splice_subwalks(sw1, sw2, cn1, cn2, ln1, ln2, edges):
    """
    Return a subwalk gotten by identifying cn1 and cn2 and linking ln1 and ln2.
    The subwalks must have no nodes in common.
    """
    pass
