# -*- coding: utf-8 -*-
"""
Created on Sun Aug 29 13:00:32 2021

@author: rober
"""

import numpy as np

import pytorch as torch
import torch.optim as optim
import torch.nn.Parameter as Parameter

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

#Test the iterative method
def iterative_test():
    #Define the graph to be a diamond structure
    #  .   0
    # / \  
    #.___. 1, 2
    # \ /  
    #  .   3
    #This is simple but nontrivial
    
    edges = ((0, 1), (0, 2), (1, 2), (1, 3), (2, 3))
    
    #Shape [N, 2]
    #for N nodes in 2 dimensions
    n=4
    nodes = Parameter(torch.randn(size=[n, 2]))
    
    #Get optimizer
    optimizer = optim.Adam(nodes, lr=0.01)
    
    num_epochs = 10
    for i in range(1, num_epochs + 1):
        with torch.no_grad():
            optimizer.zero_grad()
        
        loss = get_loss(edges, nodes)
        print('Step {}: loss = {}:.4f'.format(i, loss))
        loss.backward()
        
        with torch.no_grad():
            optimizer.step()