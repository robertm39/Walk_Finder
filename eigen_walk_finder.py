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
    # print(scales.data)
    # optimizer = optim.Adam([scales], lr=lr)
    
    # for j in range(1, num_steps + 1):
    #     scaled_parts = list()
    #     for i in range(num_dims):
    #         scaled_parts.append(parts[i] * scales[i])
        
    #     nodes = torch.stack(scaled_parts,dim=1)
        
    #     loss = walk_finder_test.get_loss(edges, nodes)
    #     # if j % 10 == 0:
    #     print('{:3d}:   loss = {:.4f}'.format(j, loss.item()))
    #     loss.backward()
        
    #     with torch.no_grad():
    #         optimizer.step()
    #         optimizer.zero_grad()
    
    print(scales.data)
    
    scaled_parts = list()
    for i in range(num_dims):
        scaled_parts.append(parts[i] * scales[i])
    
    nodes = torch.stack(scaled_parts,dim=1)
    print(walk_finder_test.get_loss(edges, nodes).item())
    return nodes

def dim_reduce_eigen(n, edges):
    """
    Put the graph into the plane by starting at a high dimension
    and gradually going down.
    """
    
    edge_mat = np.zeros((n, n))
    
    #Get the starting matrix for the full-dimensional embedding.
    for i1 in range(n-1):
        for i2 in range(i1+1, n):
            val = 1.0 if (i1, i2) in edges else 2.0
            edge_mat[i1, i2] = edge_mat[i2, i1] = val
    
    lr = 0.01
    num_steps = 200
    
    first_fit = eigen_fit(edges, edge_mat, n)
    return first_fit

def dim_reduce_eigen_test():
    # #Start with the simple diamond
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
    
    fit = dim_reduce_eigen(n, edges)

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