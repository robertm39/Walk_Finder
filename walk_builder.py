# -*- coding: utf-8 -*-
"""
Created on Tue Aug 31 10:32:54 2021

@author: rober
"""

import math

import numpy as np

SQRT_3_OVER_4 = math.sqrt(3) / 4

#Maybe change to long double for more precise equality tests
#(since this is very important) 
#Actually long double isn't any longer on this platform
DTYPE = np.double

def coords(x, y):
    return np.array([x, y], dtype=DTYPE)

class Graph:
    def __init__(self, nodes, edges):
        self.edge_dict = dict()
        for node in nodes:
            self.edge_dict[node] = set()
        for n1, n2 in edges:
            self.edge_dict[n1].add(n2)
            self.edge_dict[n2].add(n1)
    
    def has_edge(self, n1, n2):
        return n2 in self.edge_dict[n1]
    
    def adjacent(self, n1):
        return self.edge_dict[n1]
    
    def __iter__(self):
        return iter(self.edge_dict)

class SubWalk:
    def __init__(self, coords_from_nodes):
        self.coords_from_nodes = coords_from_nodes
        self.nodes = set(coords_from_nodes)
    
    def nodes_in_common(self, other):
        return self.nodes.intersection(other.nodes)
    
    #Can be used as keys, but equality is exact object equality
    #Do not ever have equivalent groups in the same map
    def __hash__(self):
        return id(self)
    
def get_triangle_subwalk(n1, n2, n3):
    coords_from_nodes = dict()
    coords_from_nodes[n1] = coords(0, 0)
    coords_from_nodes[n2] = coords(1, 0)
    coords_from_nodes[n3] = coords(0.5, SQRT_3_OVER_4)
    
    return SubWalk(coords_from_nodes)

class SubWalks:
    """
    Keep track of all the current subwalks.
    """
    def __init__(self):
        self.subwalks = set()
        self.subwalks_from_nodes = dict()
    
    def add_subwalk(self, subwalk):
        if subwalk in self.subwalks:
            raise ValueError('Duplicate subwalk: {}'.format(subwalk))
            
        self.subwalks.add(subwalk)
        for node in subwalk.nodes:
            if not node in self.subwalks_from_nodes:
                self.subwalks_from_nodes[node] = set()
            self.subwalks_from_nodes[node].add(subwalk)

def add_triangle_subwalks(graph, subwalks):
    """
    Add all triangle subwalks to the given subwalks object.
    """
    checked_nodes = set()
    
    #For each node, check for triangles involving that node
    #and not involving nodes already checked
    for n1 in graph:
        #Add now so single edges aren't recognized as degenerate triangles
        checked_nodes.add(n1)
        for n2 in graph.adjacent(n1):
            if n2 in checked_nodes:
                continue
            for n3 in graph.adjacent(n2):
                if n3 in checked_nodes: #Maybe get rid of this check
                    continue
                if graph.has_edge(n3, n1): #We found a triangle
                    triangle_subwalk = get_triangle_subwalk(n1, n2, n3)
                    subwalks.add_subwalk(triangle_subwalk)

def find_angle(n1, n2, subwalk):
    coords_1 = subwalk.coords_from_nodes(n1)
    coords_2 = subwalk.coords_from_nodes(n2)
    diff = coords_2 - coords_1
    angle = math.atan2(diff[1], diff[0])
    return angle

def translate_subwalk(t_coords, subwalk):
    """
    Translate the given subwalk by the given coords.
    This does change an object used as a key,
    but does not change any data members used to calculate the hash
    (since none are),
    so it's fine.
    """
    for node in subwalk.nodes:
        subwalk.coords_from_nodes[node] += t_coords

def rotate_subwalk(theta, subwalk):
    """
    Rotate the given subwalk counterclockwise by the given angle in radians.
    Rotation is done around the origin.
    This does change an object used as a key,
    but does not change any data members used to calculate the hash
    (since none are),
    so it's fine.
    """
    rot_matrix = np.matrix([[np.cos(theta), -np.sin(theta)],
                            [np.sin(theta),  np.cos(theta)]], dtype=DTYPE)
    
    for node in subwalk.nodes:
        coords = subwalk.coords_from_nodes[node]
        coords = rot_matrix @ coords
        subwalk.coords_from_nodes[node] = coords

def reflect_subwalk(subwalk):
    """
    Reflect the given subwalk over the x-axis.
    This does change an object used as a key,
    but does not change any data members used to calculate the hash
    (since none are),
    so it's fine.
    """
    for node, (x, y) in subwalk.coords_from_nodes.items():
        subwalk.coords_from_nodes[node] = coords(x, -y)

def union_subwalk(sw1, sw2):
    """
    Return the union of two subwalks. To be used on aligned subwalks
    with no overlaps.
    """
    coords_from_nodes = sw1.coords_from_nodes.copy()
    coords_from_nodes.update(sw2.coords_from_nodes)
    
    return SubWalk(coords_from_nodes)

#There should be a way to do this faster than quadratic
#Based on putting nodes into buckets based on their rough coordinates
#But I'll do it the simpler way for now
def check_overlaps(sw1, sw2, eps=1e-10):
    """
    Return whether there are different nodes in the same place
    in the two given subwalks, up to the given epsilon.
    To be used on aligned walks, otherwise meaningless.
    """
    checked = set()
    for n1 in sw1.nodes:
        c1 = sw1.coords_from_nodes[n1]
        checked.add(n1) #This also avoids checking a node against itself
        for n2 in sw2.nodes:
            if n2 in checked:
                continue
            c2 = sw2.coords_from_nodes[n2]
            
            #Check for approximate equality
            if np.allclose(c1, c2, rtol=0, atol=eps):
                #They overlap
                return True
    
    return False

def merge_subwalks_with_two_common_nodes(sw1, sw2):
    """
    Return a lost of subwalks containing both the nodes in sw1 and sw2,
    assuming they share exactly two nodes.
    """
    
    common_nodes = sw1.nodes_in_common(sw2)
    
    if len(common_nodes) != 2:
        s = 'Subwalks should have two common nodes, found {}'
        raise ValueError(s.format(len(common_nodes)))
    
    #There will be either 0, 1, or 2 choices in the end
    #because the graphs are aligned by a combination of a rotation
    #and an optional mirroring
    #The rotation is forced, and the choice for mirroring may also be forced
    n1, n2 = list(common_nodes)
    
    #Find the angle from the first common node to the second
    #in the first subwalk and second subwalks
    angle_1 = find_angle(n1, n2, sw1)
    angle_2 = find_angle(n1, n2, sw2)
    
    #Now we can transform both so that the first common point is at the origin
    #and the second is at (1, 0)
    #After this, mirroring is just a matter of switching the y coordinate
    #(which can be done exactly, even in floating point)
    
    #Do the translation
    translate_subwalk(-sw1.coords_from_nodes[n1], sw1)
    translate_subwalk(-sw2.coords_from_nodes[n1], sw2)
    
    #Do the rotation
    rotate_subwalk(-angle_1, sw1)
    rotate_subwalk(-angle_2, sw2)
    
    #Now the common points have been aligned
    #The one degree of freedom is whether we mirror the second over the x-axis
    #Try both and see what works
    result = list()
    if not check_overlaps(sw1, sw2):
        merged = union_subwalk(sw1, sw2)
        result.append(merged)
    
    #The previous merged subwalk does not directly reference either
    #of its component subwalks, so mutating the sw2 is fine.
    reflect_subwalk(sw2)
    if not check_overlaps(sw1, sw2):
        merged = union_subwalk(sw1, sw2)
        result.append(merged)
    
    return result

def build_walk(n, edges):
    """
    Return a graph where the nodes linked by edges have unit distance.
    """
    nodes = range(n)
    subwalks = SubWalks()
    graph = Graph(nodes, edges)
    
    #Initialize the subwalks collection with all triangles.
    add_triangle_subwalks(graph, subwalks)
    
    