# -*- coding: utf-8 -*-
"""
Created on Tue Aug 31 17:33:12 2021

@author: rober
"""

import numpy as np

import walk_builder

def edges_from_file(filename, offset=0):
    with open(filename) as file:
        edges = list()
        skipped = False
        for line in file:
            if not skipped:
                skipped = True
                continue
            _, node_1, node_2 = line.split()
            node_1 = int(node_1)
            node_2 = int(node_2)
            edge = node_1 - 1 + offset, node_2 - 1 + offset
            edges.append(edge)
    return edges

def write_to_file(walk, graph, filename):
    with open(filename, 'w') as file:
        file.write('NODES\n')
        for node, coords in walk.items():
            x = coords[0]
            y = coords[1]
            file.write('{} {} {}\n'.format(node, x, y))
        
        file.write('EDGES\n')
        for n1, n2 in graph.edges():
            file.write('{} {}\n'.format(n1, n2))
        file.write('DONE')

def read_from_file(filename):
    with open(filename) as file:
        line_iter = iter(file)
        
        #Skip the NODES line
        next(line_iter)
        
        coords_from_nodes = dict()
        line = next(line_iter)
        while line != 'EDGES\n':
            node, x, y = line.split()
            node = int(node)
            coords_string = '{} {}'.format(x, y)
            coords = np.fromstring(coords_string,
                                   sep=' ',
                                   dtype=walk_builder.DTYPE)
            coords_from_nodes[node] = coords
            
            line = next(line_iter)
        #line == 'EDGES\n'
        # next(line_iter)
        line = next(line_iter)
        edges = set()
        while line != 'DONE':
            n1, n2 = line.split()
            edge = int(n1), int(n2)
            edges.add(edge)
            line = next(line_iter)
    
    nodes = set(coords_from_nodes)
    walk = walk_builder.SubWalk(coords_from_nodes)
    graph = walk_builder.Graph(nodes, edges)
    return walk, graph