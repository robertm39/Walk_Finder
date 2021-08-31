# -*- coding: utf-8 -*-
"""
Created on Sun Aug 29 14:51:42 2021

@author: rober
"""

import math

import numpy as np

import torch
import torch.optim as optim
from torch.nn import Parameter as Parameter

import walk_finder_test
import graph_shower

def eigen_fit(edge_mat, num_dims):
    # u, _, _ = np.linalg.svd(edge_mat)
    u, _, _ = torch.linalg.svd(edge_mat)
    
    parts = list()
    for i in range(num_dims):
        part = u[:, i]
        part = part.clone().detach().requires_grad_(True)
        parts.append(part)
    
    scales = Parameter(torch.ones([num_dims], dtype=torch.double))
    with torch.no_grad():
        scales.data *= math.sqrt(0.5)
    
    scaled_parts = list()
    for i in range(num_dims):
        scaled_parts.append(parts[i] * scales[i])
    
    nodes = torch.stack(scaled_parts,dim=1)
    # print(walk_finder_test.get_loss(edges, nodes).item())
    return nodes

def get_dist_matrix(n, distances):
    """
    Return the distance matrix, given the distance dict.
    """
    result = torch.zeros([n, n])
    for i in range(n):
        for j in range(i, n):
            if i == j:
                dist = distances[i, j]
                result[i, j] = dist
            else:
                dist = distances[i, j]
                result[i, j] = dist
                result[j, i] = dist
    
    return result

def get_singular_value_loss(dist_matrix, target_dim):
    """
    Return the singular value loss for dimensionality reduction.
    """
    svs = torch.linalg.svdvals(dist_matrix)
    
    vals_to_kill = svs[target_dim:]
    squ_vals = torch.square(vals_to_kill)
    return squ_vals.sum()    

def get_double_singular_value_loss(n, dist_matrix, target_dim):
    #First, get the coordinate representation
    nodes = eigen_fit(dist_matrix, n)
    
    #Then takes its singular values
    svs = torch.linalg.svdvals(nodes)
    
    vals_to_kill = svs[target_dim:]
    squ_vals = torch.square(vals_to_kill)
    return squ_vals.sum()    

def dim_reduce_eigen(n, edges, lr=0.01, num_steps_per_dim=100):
    """
    Put the graph into the plane by starting at a high dimension
    and gradually going down.
    """
    
    #Initialize the distances and get the parameters
    distances = dict()
    params = list()
    
    for i in range(n):
        for j in range(i,n):
            if i == j:
                distances[i, j] = 0
            elif (i, j) in edges:
                distances[i, j] = 1.0 #just a constant, shouldn't change
            else:
                dist = Parameter(torch.ones([], dtype=torch.double))
                with torch.no_grad():
                    dist.data *= 1.732
                params.append(dist)
                distances[i, j] = dist
    
    optimizer = optim.Adam(params, lr=lr)
    
    for p in params:
        print(p.data.item())
    
    # step = 0
    # for num_dims in range(n-1, 1, -1):
    #     print('Num target dims: {}'.format(num_dims))
    #     num_steps = num_steps_per_dim[step]
    for i in range(1, num_steps_per_dim):
        dist_matrix = get_dist_matrix(n, distances)
        
        # svd_loss = get_singular_value_loss(dist_matrix, 2)
        # end_loss = get_singular_value_loss(dist_matrix, 2)
        
        svd_loss = get_double_singular_value_loss(n, dist_matrix, 2)
        
        svd_loss.backward()
        
        with torch.no_grad():
            optimizer.step()
            optimizer.zero_grad()
        
        if i % 200 == 0:
            # s = '{:5d} steps:   loss={:.4f}, end loss={:.4f}'
            s = '{:5d} steps:   loss={:.4f}'
            print(s.format(i, svd_loss.item()))
            for p in params:
                print(p.data.item())
        # print('')
        # step += 1
    
    dist_matrix = get_dist_matrix(n, distances)
    print(dist_matrix)
    with torch.no_grad():
        svs = torch.linalg.svdvals(dist_matrix)
    # print(svs.data)
    
    nodes = eigen_fit(dist_matrix, n)
    print(nodes)
    
    print(nodes.shape)
    graph_shower.make_graph_png_with_lines(nodes, edges)

def dim_reduce_eigen_test():
    #Start with the simple diamond
    # edges = {(0, 1), (0, 2), (1, 2), (1, 3), (2, 3)}
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
              (4, 6))
    n = 7
    
    # #            6    5    4    3     2
    # num_steps = [400, 400, 400, 2000, 10000]
    
    #            3     2
    # num_steps = [2000, 2000]
    num_steps = 10000
    fit = dim_reduce_eigen(n, edges, num_steps_per_dim=num_steps)
