# -*- coding: utf-8 -*-
"""
Created on Tue Aug 31 18:11:13 2021

@author: rober
"""

import queue

import walk_builder

import file_reader

# #Taken from https://docs.python.org/3/library/queue.html
# from dataclasses import dataclass, field
# from typing import Any

# @dataclass(order=True)
# class PrioritizedItem:
#     priority: int
#     item: Any=field(compare=False)
# #**********************

# def set_color(node,
#                color,
#                num,
#                colorings,
#                uncolored,
#                graph,
#                nodes_from_numbers,
#                possible_colors_from_nodes):
    
#     uncolored.remove(node)
#     colorings[node] = color
#     possible_colors_from_nodes[node] = {color}
#     nodes_from_numbers[num].remove(node)
#     for n in graph.adjacent(node):
#         num_colors = len(possible_colors_from_nodes[n])
#         nodes_from_numbers[num_colors].remove(n)
#         nodes_from_numbers[num_colors - 1].add(n)
#         possible_colors_from_nodes[node].remove(color)

class ColoringState:
    def __init__(self,
                 graph,
                 n_colors=5,
                 uncolored=None,
                 colorings=None,
                 nodes_from_numbers=None,
                 possible_colors_from_nodes=None):
        if uncolored is None:
            uncolored = set()
        if colorings is None:
            colorings = dict()
        if nodes_from_numbers is None:
            nodes_from_numbers = {n: set() for n in range(n_colors)}
            nodes_from_numbers[n_colors] = set(graph)
        if possible_colors_from_nodes is None:
            possible_colors_from_nodes = {n: set(range(n_colors)) for n in graph}
    
    def copy(self):
        uncolored = self.uncolored.copy()
        colorings = self.colorings.copy()
        nodes_from_numbers = self.nodes_from_numbers.copy()
        possible_colors_from_nodes = self.possible_colors_from_nodes.copy()
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
        for n in self.graph.adjacent(node):
            num_colors = len(self.possible_colors_from_nodes[n])
            self.nodes_from_numbers[num_colors].remove(n)
            self.nodes_from_numbers[num_colors - 1].add(n)
            self.possible_colors_from_nodes[node].remove(color)

    def rule_out_color(self, node, color):
        if not node in self.graph:
            raise ValueError('Node not in graph: {}'.format(node))
        
        num = len(self.possible_colors_from_nodes[node])
        self.nodes_from_numbers[num].remove(node)
        self.nodes_from_numbers[num-1].add(node)
        self.possible_colors_from_nodes[node].remove(color)

#Want to find a graph that can't be five-colored
def color_graph(graph=None, c_state=None):
    
    if c_state is None:
        if graph is None:
            raise ValueError('Both arguments are none')
        c_state = ColoringState(graph)
    
    # if uncolored is None:
    #     uncolored = set(graph)
    # else:
    #     pass
    #     # uncolored = uncolored.copy()
    
    # if colorings is None:
    #     colorings = dict()
    # else:
    #     pass
    #     # colorings = colorings.copy()
    
    # if nodes_from_numbers is None:
    #     nodes_from_numbers = {n_colors: set(graph)}
    # else:
    #     nodes_from_numbers = nodes_from_numbers.copy()
    
    # if possible_colors_from_nodes is None:
    #     #At first, all colors are possible
    #     possible_colors_from_nodes = {n: set(range(n_colors)) for n in graph}
    # else:
    #     possible_colors_from_nodes = possible_colors_from_nodes.copy()
    
    #Everything is initialized now
    while True: #This will end
        if not c_state.uncolored: #The whole thing is colored
            return c_state.colorings
    
        numbers_of_colors = sorted(list(set(c_state.nodes_from_numbers)))
        for num in numbers_of_colors:
            if num == 0:
                #There are no colors to color it with
                #we failed
                return False
            
            nodes = c_state.nodes_from_numbers[num]
            if not nodes:
                continue
            node = next(iter(nodes))
            colors = c_state.possible_colors_from_nodes[node]
            color = next(iter(colors))
            
            #No need for recursion
            #if this fails, the whole thing fails
            if num == 1:
                c_state.set_color(node, num, color)
                # set_color(node,
                #           color,
                #           num,
                #           colorings,
                #           uncolored,
                #           graph,
                #           nodes_from_numbers,
                #           possible_colors_from_nodes)
            #There's more than one color
            else:
                copy_c_state = c_state.copy()
                copy_c_state.set_color(node, color)
                s_result = color_graph(graph, copy_c_state)
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
    