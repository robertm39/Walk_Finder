# -*- coding: utf-8 -*-
"""
Created on Tue Aug 31 10:32:54 2021

@author: rober
"""

import math

import numpy as np

SQRT_3_OVER_4 = math.sqrt(3) / 2

#Maybe change to long double for more precise equality tests
#(since this is very important) 
#Actually long double isn't any longer on this platform
DTYPE = np.double

def coords(x, y):
    return np.array([x, y], dtype=DTYPE)

class Graph:
    def __init__(self, nodes, edges):
        self.edge_dict = dict()
        self.nodes = set(nodes)
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
    
    def copy(self):
        coords_from_nodes = dict()
        for node, coords in self.coords_from_nodes.items():
            coords_from_nodes[node] = coords.copy()
        return SubWalk(coords_from_nodes)
    
    #Can be used as keys, but equality is exact object equality
    #Do not ever have equivalent groups in the same map
    def __hash__(self):
        return id(self)
    
    def __iter__(self):
        return  iter(self.nodes)
    
    def __contains__(self, node):
        return node in self.nodes
    
def get_triangle_subwalk(n1, n2, n3):
    """
    Return a subwalk containing the three given nodes in a triangle.
    """
    coords_from_nodes = dict()
    coords_from_nodes[n1] = coords(0, 0)
    coords_from_nodes[n2] = coords(1, 0)
    coords_from_nodes[n3] = coords(0.5, SQRT_3_OVER_4)
    
    return SubWalk(coords_from_nodes)

def get_edge_subwalk(n1, n2):
    """
    Return a subwalk containing the two given nodes on an edge
    """
    coords_from_nodes = dict()
    coords_from_nodes[n1] = coords(0, 0)
    coords_from_nodes[n2] = coords(1, 0)
    return SubWalk(coords_from_nodes)

# class SetKey:
#     def __init__(self, s):
#         self.s = s
        
#         self.hash = 17
#         for h in sorted([hash(i) for i in self.s]):
#             self.hash += h
#             self.hash *= 31
    
#     def __eq__(self, other):
#         return self.s == other.s
    
#     def __neq__(self, other):
        
    
#     def __hash__(self):
#         return self,hash

class SubWalks:
    """
    Keep track of all the current subwalks.
    """
    def __init__(self):
        self.subwalks = set()
        self.subwalks_from_nodes = dict()
        self.pairs_from_num_common = dict()
        self.pairs_from_subwalks = dict()
    
    def add_subwalk(self, subwalk):
        if subwalk in self.subwalks:
            raise ValueError('Duplicate subwalk: {}'.format(subwalk))
            
        self.subwalks.add(subwalk)
        
        subwalks_with_common_node = set()
        for node in subwalk.nodes:
            if not node in self.subwalks_from_nodes:
                self.subwalks_from_nodes[node] = set()
                
            for sw2 in self.subwalks_from_nodes[node]:
                subwalks_with_common_node.add(sw2)
                
            self.subwalks_from_nodes[node].add(subwalk)
        
        pairs = set()
        self.pairs_from_subwalks[subwalk] = pairs
        for sw2 in subwalks_with_common_node:
            num_common = len(subwalk.nodes_in_common(sw2))
            
            #Even if there's only one common node, 
            #connections between the two may make merging them feasible
            # if num_common >= 2:
            if not num_common in self.pairs_from_num_common:
                self.pairs_from_num_common[num_common] = set()
            self.pairs_from_num_common[num_common].add((subwalk, sw2))
            pairs.add((subwalk, sw2, num_common))
            
            #Almost forgot this part
            self.pairs_from_subwalks[sw2].add((subwalk, sw2, num_common))
        
        # for node in subwalk.nodes:
        #     if not node in self.subwalks_from_nodes:
        #         self.subwalks_from_nodes[node] = set()
        #     self.subwalks_from_nodes[node].add(subwalk)
    
    def remove_subwalk(self, subwalk):
        if not subwalk in self.subwalks:
            raise ValueError('Subwalk not in subwalks: {}'.format(subwalk))
        
        self.subwalks.remove(subwalk)
        
        for node in subwalk.nodes:
            self.subwalks_from_nodes[node].remove(subwalk)
        
        for sw1, sw2, num_common in list(self.pairs_from_subwalks[subwalk]):
            self.pairs_from_num_common[num_common].remove((sw1, sw2))
            self.pairs_from_subwalks[sw1].remove((sw1, sw2, num_common))
            self.pairs_from_subwalks[sw2].remove((sw1, sw2, num_common))
        
        del self.pairs_from_subwalks[subwalk]
    
    def copy(self):
        copy = SubWalks()
        for subwalk in self.subwalks:
            copy.add_subwalk(subwalk.copy())
        return copy

#I think I'll just use actual recursion
#if it gets too deep I'll have to use this
#but I think I can manage the depth by focusing on forced mergings
class CheckPoint:
    """
    A state to go back to if embedding fails.
    """
    def __init__(self, subwalks, sw1, sw2, mergings):
        self.subwalks = subwalks.copy()
        self.sw1 = sw1.copy()
        self.sw2 = sw2.copy()
        self.mergings = mergings

def add_triangle_subwalks(graph, subwalks):
    """
    Add all triangle subwalks to the given subwalks object.
    """
    checked_nodes = set()
    
    nodes_in_triangles = set()
    #For each node, check for triangles involving that node
    #and not involving nodes already checked
    for n1 in graph:
        #Add now so single edges aren't recognized as degenerate triangles
        checked_nodes.add(n1)
        sub_checked_nodes = set()
        for n2 in graph.adjacent(n1):
            if n2 in checked_nodes:
                continue
            sub_checked_nodes.add(n2)
            for n3 in graph.adjacent(n2):
                if n3 in checked_nodes:
                    continue
                if n3 in sub_checked_nodes:
                    continue
                if graph.has_edge(n3, n1): #We found a triangle
                    nodes_in_triangles.add(n1)
                    nodes_in_triangles.add(n2)
                    nodes_in_triangles.add(n3)
                    triangle_subwalk = get_triangle_subwalk(n1, n2, n3)
                    subwalks.add_subwalk(triangle_subwalk)
    
    #Also add edges for all nodes that aren't in triangles
    checked_nodes = nodes_in_triangles
    for n1 in graph:
        if n1 in checked_nodes:
            continue
        checked_nodes.add(n1)
        for n2 in graph.adjacent(n1):
            if n2 in checked_nodes:
                continue
            edge_subwalk = get_edge_subwalk(n1, n2)
            subwalks.add_subwalk(edge_subwalk)

    #There won't be any free-floating nodes

def find_angle(n1, n2, subwalk):
    coords_1 = subwalk.coords_from_nodes[n1]
    coords_2 = subwalk.coords_from_nodes[n2]
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
    rot_matrix = np.array([[np.cos(theta), -np.sin(theta)],
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
    for node, crd in subwalk.coords_from_nodes.items():
        # print(c)
        x, y = crd[0], crd[1]
        subwalk.coords_from_nodes[node] = coords(x, -y)

def union_subwalk(sw1, sw2):
    """
    Return the union of two subwalks. To be used on aligned subwalks
    with no overlaps.
    """
    coords_from_nodes = sw1.copy().coords_from_nodes
    coords_from_nodes.update(sw2.copy().coords_from_nodes) #maybe don't copy
    
    return SubWalk(coords_from_nodes)

#There should be a way to do this faster than quadratic
#Based on putting nodes into buckets based on their rough coordinates
#But I'll do it the simpler way for now

#As for epsilon, it seems like errors of the scale occur 1e-16
#so stay a few orders of magnitude above that
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
                return False
    
    return True

def check_connected_nodes(sw1, sw2, graph, eps=1e-10):
    """
    Check whether nodes connected between the subwalks are at unit distance.
    To be used on aligned walks, otherwise meaningless.
    """
    for node in sw1:
        c1 = sw1.coords_from_nodes[node]
        for n2 in graph.adjacent(node):
            if n2 in sw2:
                c2 = sw2.coords_from_nodes[n2]
                diff = c2 - c1
                # print('diff: {}'.format(diff))
                dist = np.hypot(*diff)
                if not np.allclose(dist, 1.0, rtol=0, atol=eps):
                    return False
    return True

def check_identical(sw1, sw2, eps=1e-10):
    """
    Make sure that the same nodes have the same coords in both subwalks.
    To be used on aligned walks, otherwise meaningless.
    """
    for node in sw1.nodes_in_common(sw2):
        c1 = sw1.coords_from_nodes[node]
        c2 = sw2.coords_from_nodes[node]
        if not np.allclose(c1, c2, rtol=0, atol=eps):
            return False
    return True

def check_validity(sw1, sw2, graph, eps=1e-10):
    """
    Check whether the two subwalks could be validly merged, that is,
    whether they're free of overlaps and all nodes connected between the two
    are at unit distance.
    To be used on aligned walks, otherwise meaningless.
    """
    if not check_overlaps(sw1, sw2, eps=eps):
        return False #Not valid because they overlap
    
    if not check_identical(sw1, sw2, eps=eps):
        return False #Not valid because the same node is in different places
    
    return check_connected_nodes(sw1, sw2, graph, eps)

def merge_subwalks_with_two_common_nodes(sw1, sw2, graph):
    """
    Return a lost of subwalks containing both the nodes in sw1 and sw2,
    assuming they share at least two nodes.
    """
    sw1 = sw1.copy()
    sw2 = sw2.copy()
    
    common_nodes = sw1.nodes_in_common(sw2)
    
    if len(common_nodes) < 2:
        s = 'Subwalks should have at least two common nodes, found {}'
        raise ValueError(s.format(len(common_nodes)))
    
    #There will be either 0, 1, or 2 choices in the end
    #because the graphs are aligned by a combination of a rotation
    #and an optional mirroring
    #The rotation is forced, and the choice for mirroring may also be forced
    n1, n2 = list(common_nodes)[:2]
    #Align by the first two
    #aligning by the rest can only be a matter of mirroring
    #so it will be handled later
    #this automatically handles the case of colinear nodes
    
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
    if check_validity(sw1, sw2, graph):
        merged = union_subwalk(sw1, sw2)
        result.append(merged)
    
    #The previous merged subwalk does not directly reference either
    #of its component subwalks, so mutating the sw2 is fine.
    reflect_subwalk(sw2)
    if check_validity(sw1, sw2, graph):
        merged = union_subwalk(sw1, sw2)
        result.append(merged)
    
    return result

def merge_subwalks_with_one_common_node(sw1, sw2, graph):
    """
    Merge two subwalks with one common node and at least one edge between them.
    """
    sw1 = sw1.copy()
    sw2 = sw2.copy()
    
    common_nodes = sw1.nodes_in_common(sw2)
    if len(common_nodes) != 1:
        s = 'Subwalks should have 1 common node, got {}'
        raise ValueError(s.format(len(common_nodes)))
    
    common = next(iter(common_nodes))
    
    #Translate the subwalks so that the common node is at the origin
    translate_subwalk(-sw1.coords_from_nodes[common], sw1)
    translate_subwalk(-sw2.coords_from_nodes[common], sw2)
    
    #Find two connected nodes, where none are the common node
    node_1 = None
    node_2 = None
    done = False
    for n1 in sw1:
        if done:
            break
        if n1 == common:
            continue
        for n2 in graph.adjacent(n1):
            if not n2 in sw2:
                continue
            if n2 == common:
                continue
            
            #We've found an edge
            done = True
            node_1 = n1
            node_2 = n2
            break
    
    #Now node_1 and node_2 are two connected nodes
    
    #Rotate sw1 and sw2 so node_1 and node_2 are on the x-axis
    node_1_angle = find_angle(common, node_1, sw1)
    node_2_angle = find_angle(common, node_2, sw2)
    
    rotate_subwalk(-node_1_angle, sw1)
    rotate_subwalk(-node_2_angle, sw2)
    
    #Now both node_1 and node_2 are on the x-axis
    #now I need to find theta
    x_1 = sw1.coords_from_nodes[node_1][0]
    dist = sw2.coords_from_nodes[node_2][0]
    
    num = dist**2 + x_1**2 - 1
    denom = 2*dist*x_1
    
    theta = np.arccos(num / denom)
    
    #It doesn't work
    if np.isnan(theta):
        return list()
    
    #Now there are four combinations:
    #Either mirror or don't,
    #and either negate theta or don't.
    #check all.
    
    result = list()
    #First: don't mirror, don't negate theta.
    sw2_copy = sw2.copy()
    rotate_subwalk(theta, sw2_copy)
    if check_validity(sw1, sw2_copy, graph):
        merged = union_subwalk(sw1, sw2_copy)
        result.append(merged)
    
    #Second: don't mirror, do negate theta.
    sw2_copy = sw2.copy()
    rotate_subwalk(-theta, sw2_copy)
    if check_validity(sw1, sw2_copy, graph):
        merged = union_subwalk(sw1, sw2_copy)
        result.append(merged)
    
    #Third: do mirror, don't negate theta
    sw2_copy = sw2.copy()
    reflect_subwalk(sw2_copy)
    rotate_subwalk(theta, sw2_copy)
    if check_validity(sw1, sw2_copy, graph):
        merged = union_subwalk(sw1, sw2_copy)
        result.append(merged)
    
    #Fourth: do mirror, do negate theta
    sw2_copy = sw2.copy()
    reflect_subwalk(sw2_copy)
    rotate_subwalk(-theta, sw2_copy)
    if check_validity(sw1, sw2_copy, graph):
        merged = union_subwalk(sw1, sw2_copy)
        result.append(merged)
    
    return result
    
def merge_subwalks(sw1, sw2, graph):
    num_common = len(sw1.nodes_in_common(sw2))
    #Merge by aligning two points and maybe mirroring
    if num_common >= 2:
        return merge_subwalks_with_two_common_nodes(sw1, sw2, graph)
    
    #Merge by aligning one point and making one edge work, and maybe mirroring
    if num_common == 1:
        return merge_subwalks_with_one_common_node(sw1, sw2, graph)
    
    #TODO merging subwalks with no common nodes but multiple edges
    return list()

def build_walk(graph, subwalks=None):
    """
    Return a graph where the nodes linked by edges have unit distance.
    """
    # nodes = range(n)
    # subwalks = SubWalks()
    # graph = Graph(nodes, edges)
    
    if subwalks is None:
        #Initialize the subwalks collection with all triangles.
        subwalks = SubWalks()
        add_triangle_subwalks(graph, subwalks)
    
    #Repeatedly merge the most promising subwalk until we fail
    #Or there's only one subwalk (we've succeeded)
    while True: #This will end
        #Success condition:
        #if there's only one subwalk left, we've embedded the graph
        if len(subwalks.subwalks) == 1:
            #Return the single subwalk remaining
            return next(iter(subwalks.subwalks))
    
        overlaps = set(subwalks.pairs_from_num_common)
        overlaps = [o for o in overlaps if subwalks.pairs_from_num_common[o]]
        
        most_overlap = max(overlaps)
        most_overlap_pairs = subwalks.pairs_from_num_common[most_overlap]
        if most_overlap_pairs:
            sw1, sw2 = next(iter(most_overlap_pairs))
            
            mergings = merge_subwalks(sw1, sw2, graph)
            if not mergings:
                #They can't be merged, nor can they ever, so we've failed
                #give up and notify the caller
                return False
            
            #This is gonna happen either way
            subwalks.remove_subwalk(sw1)
            subwalks.remove_subwalk(sw2)
            
            #If there's only one merging, no need for recursion
            if len(mergings) == 1:
                merging = mergings[0]
                
                #If it has all the nodes, it works
                #even if there are other ways
                #Without this, the algorithm would interpret
                #multiple successes as a failure
                if merging.nodes == graph.nodes:
                    return merging
                subwalks.add_subwalk(mergings[0])
            else: #There are multiple possible mergings, try each recursively
                for merging in mergings: #Here is where it branches
                    
                    if merging.nodes == graph.nodes:
                        return merging
                    
                    r_subwalks = subwalks.copy()
                    r_subwalks.add_subwalk(merging)
                    r_result = build_walk(graph, r_subwalks)
                    if r_result:
                        #Return the single subwalk returned by the child
                        return r_result
                #Merging the two subwalks in any way doesn't work
                #give up and notify the caller
                return False
        
        else:
            return False
        #Deal with mergers where we don't have any overlaps

def walk_builder_test():
    # #First is the simple diamond
    # edges = ((0, 1),
    #          (0, 2),
    #          (1, 2),
    #          (1, 3),
    #          (2, 3))
    # n = 4
    
    #Next test is the graph that needs four colors
    edges = ((0, 1),
             (0, 2),
             (0, 3),
             (1, 2),
             (1, 4),
             (2, 3),
             (3, 5),
             (3, 6),
             (4, 5),
             (4, 6),
             (5, 6))
    n = 7
    
    nodes = range(n)
    graph = Graph(nodes, edges)
    
    walk = build_walk(graph)
    if walk:
        print('Succeeded!')
        for node in nodes:
            print(walk.coords_from_nodes[node])
    else:
        print('Failed')