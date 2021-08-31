# -*- coding: utf-8 -*-
"""
Created on Tue Aug 31 18:11:13 2021

@author: rober
"""

import walk_builder

import file_reader

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
    