# -*- coding: utf-8 -*-
"""
Created on Sun Aug 29 13:00:32 2021

@author: rober
"""

import matplotlib.pyplot as plt

import torch
import torch.optim as optim
from torch.nn import Parameter as Parameter

import graph_shower
import walk_builder
import point_store

def get_loss(edges, nodes):
    """
    Return the loss for the given edges and nodes.
    """
    
    total_loss = 0
    
    for n1, n2 in edges:
        p1, p2 = nodes[n1, :], nodes[n2, :]
        diff = p1 - p2
        diff_squ = torch.square(diff)
        squ_dist = diff_squ.sum()
        edge_loss = torch.square((squ_dist - 1))
        total_loss += edge_loss
    return total_loss

def get_spreading_loss(nodes, eps=1e-8):
    """
    Return a loss that encourages nodes to spread apart.
    Used early to prevent solutions where two nodes are in the same spot.
    """
    
    total_loss = 0
    
    for n1 in range(len(nodes)-1):
        for n2 in range(n1+1, len(nodes)):
            p1, p2 = nodes[n1, :], nodes[n2, :]
            diff = p1 - p2
            diff_squ = torch.square(diff)
            squ_dist = diff_squ.sum()
            edge_loss = 1 / (squ_dist + eps)
            edge_loss = torch.clamp(edge_loss, min=0.9, max=None)
            total_loss += edge_loss
    return total_loss

def make_scatter(nodes):
    x = nodes[:, 0].detach().numpy()
    y = nodes[:, 1].detach().numpy()
    colors = (0, 0, 0)
    
    plt.scatter(x, y, s=1.0, color=colors)
    plt.show

#Test the iterative method
def iterative_test():
    #Define the graph to be a diamond structure
    #  .   0
    # / \  
    #.___. 1, 2
    # \ /  
    #  .   3
    #This is simple but nontrivial
    
    edges = ((0, 1),
             (0, 2),
             (1, 2),
             (1, 3),
             (2, 3))
    
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
    
    #Shape [N, 2]
    #for N nodes in 2 dimensions
    n=4
    nodes = Parameter(torch.randn(size=[n, 2]))
    
    # make_scatter(nodes)
    
    #Get optimizer
    optimizer = optim.Adam([nodes], lr=0.01)
    
    print('Start:')
    # print(nodes.data)
    graph_shower.make_graph_png_with_lines(nodes, edges)
    print('')
    
    num_epochs = 20000
    spreading_loss_weight = 128.0
    spreading_loss_decay = 0.5
    spreading_loss_interval = 2000
    
    for i in range(1, num_epochs + 1):
        with torch.no_grad():
            optimizer.zero_grad()
        
        loss = get_loss(edges, nodes)
        spread_loss = get_spreading_loss(nodes)
        total_loss = loss + spreading_loss_weight * spread_loss
        
        if i % spreading_loss_interval == 0:
            spreading_loss_weight *= spreading_loss_decay
        
        if i % 500 == 0:
            s = 'Step {:6}:   loss = {:.4f}   spread loss = {:.4f}'
            print(s.format(i, loss.item(), spread_loss.item()))
        
        total_loss.backward()
        
        with torch.no_grad():
            optimizer.step()
    
    print('Result:')
    print(nodes.data)
    # make_scatter(nodes)
    # graph_shower.make_graph_png(nodes, edges)
    graph_shower.make_graph_png_with_lines(nodes, edges)

import sys

def main():
    #Recursion limit of 1,000,000 should be enough
    sys.setrecursionlimit(10000000)
    
    # iterative_test()
    # eigen_walk_finder.eigen_test()
    # eigen_walk_finder.dim_reduce_eigen_test()
    # walk_builder.walk_builder_test()
    # walk_builder.color_test()
    # walk_builder.file_test()
    walk_builder.node_adder_test()
    # point_store.key_test()
    # point_store.ring_test()
    # point_store.point_store_test()
    # point_store.point_store_two_test()
    # point_store.point_store_same_test()

if __name__ == '__main__':
    main()