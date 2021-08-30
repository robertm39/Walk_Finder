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

def eigen_fit(edges, edge_mat, num_dims):
    u, _, _ = np.linalg.svd(edge_mat)
    
    parts = list()
    for i in range(num_dims):
        part = u[:, i]
        part = torch.tensor(part, requires_grad=False, dtype=torch.double)
        parts.append(part)
    
    scales = Parameter(torch.ones([num_dims], dtype=torch.double))
    with torch.no_grad():
        scales.data *= math.sqrt(0.5)
    
    scaled_parts = list()
    for i in range(num_dims):
        scaled_parts.append(parts[i] * scales[i])
    
    nodes = torch.stack(scaled_parts,dim=1)
    print(walk_finder_test.get_loss(edges, nodes).item())
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

def dim_reduce_eigen(n, edges, lr=0.01, num_steps_per_dim=100):
    """
    Put the graph into the plane by starting at a high dimension
    and gradually going down.
    """
    
    # edge_mat = np.zeros((n, n))
    
    # #Get the starting matrix for the full-dimensional embedding.
    # for i1 in range(n-1):
    #     for i2 in range(i1+1, n):
    #         val = 1.0 if (i1, i2) in edges else 2.0
    #         edge_mat[i1, i2] = edge_mat[i2, i1] = val
    
    # first_fit = eigen_fit(edges, edge_mat, n)
    
    #Don't even bother with finding a fit at first
    #Just optimize the distance matrix so that it ends up two-dimensional
    #That is, with only two nonzero singular values
    
    # if isinstance(num_steps_per_dim, int):
    #     num_steps_per_dim = [num_steps_per_dim] * (n-2)
    
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
        svd_loss = get_singular_value_loss(dist_matrix, 2)
        # end_loss = get_singular_value_loss(dist_matrix, 2)
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
    print(svs.data)

def dim_reduce_eigen_test():
    #Start with the simple diamond
    edges = {(0, 1), (0, 2), (1, 2), (1, 3), (2, 3)}
    n = 4
    
    # #Next test is the graph that needs four colors
    # edges = ((0, 1),
    #          (0, 2),
    #          (0, 3),
    #          (1, 2),
    #          (1, 4),
    #          (2, 3),
    #          (3, 5),
    #          (3, 6),
    #          (4, 5),
    #          (4, 6))
    # n = 7
    
    # #            6    5    4    3     2
    # num_steps = [400, 400, 400, 2000, 10000]
    
    #            3     2
    # num_steps = [2000, 2000]
    num_steps = 5000
    fit = dim_reduce_eigen(n, edges, num_steps_per_dim=num_steps)

# def eigen_test():
#     """
#     Test the SVD method of putting a graph into the plane.
#     """
    
#     #Start with the simple diamond
#     edges = {(0, 1), (0, 2), (1, 2), (1, 3), (2, 3)}
#     n = 4
    
#     edge_mat = np.zeros((n, n))
    
#     #Initialize the distances - 
#     #1 for nodes joined by an edge,
#     #2 otherwise (to prevent collapses)
#     for i1 in range(n-1):
#         for i2 in range(i1+1, n):
#             val = 1.0 if (i1, i2) in edges else 2.0
#             edge_mat[i1, i2] = edge_mat[i2, i1] = val
    
#     print(edge_mat)
#     print('')
    
#     num_steps = 1
#     num_inner_steps = 100
    
#     lr = 0.01
    
#     for i in range(num_steps):
#         u, _, _ = np.linalg.svd(edge_mat)
#         print(u)
#         part_1 = u[:, 0]
#         part_2 = u[:, 1]
#         print(part_1)
#         print(part_2)
        
#         part_1 = torch.tensor(part_1, requires_grad=False)
#         part_2 = torch.tensor(part_2, requires_grad=False)
        
#         #use part_1 for x and part_2 for y
#         scales = Parameter(torch.ones([2]))
        
#         optimizer = optim.Adam([scales], lr=lr)
        
#         for j in range(num_inner_steps):
#             scaled_part_1 = part_1 * scales[0]
#             scaled_part_2 = part_2 * scales[1]
#             nodes = torch.stack([scaled_part_1, scaled_part_2],dim=1)
            
#             loss = walk_finder_test.get_loss(edges, nodes)
#             if j % 10 == 0:
#                 print('{:2d}:   loss = {:.4f}'.format(j, loss.item()))
#             loss.backward()
            
#             with torch.no_grad():
#                 optimizer.step()
#                 optimizer.zero_grad()
        
        
#         scaled_part_1 = part_1 * scales[0]
#         scaled_part_2 = part_2 * scales[1]
#         nodes = torch.stack([scaled_part_1, scaled_part_2],dim=1)
#         # nodes = nodes.detach().numpy()
#         graph_shower.make_graph_png_with_lines(nodes, edges)