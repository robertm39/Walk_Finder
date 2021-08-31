# -*- coding: utf-8 -*-
"""
Created on Tue Aug 31 17:33:12 2021

@author: rober
"""

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