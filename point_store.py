# -*- coding: utf-8 -*-
"""
Created on Wed Sep  1 15:30:46 2021

@author: rober
"""

import numpy as np

import walk_builder

from constants import EPS

NUM_DECIMALS = 2

# EPS = 1e-10

#I'm not actually gonna support changing the number of decimal places for now
#Actually I will

def get_cell_ring(num_decimals=NUM_DECIMALS):
    width = 10**(-num_decimals)
    num_cells_wide = 10 ** num_decimals #How many cells wide a 1x1 square is
    
    diag = width * np.sqrt(2)
    min_dist = 1 - diag
    max_dist = 1 + diag
    
    corner_disps = (walk_builder.coords(width/2, width/2),
                    walk_builder.coords(-width/2, width/2),
                    walk_builder.coords(-width/2, -width/2),
                    walk_builder.coords(width/2, -width/2))
    #The most the maximum and minimum distance can differ from the distance
    #between the centers is at most this much
    #(this is an overestimate, which is good anyways)
    
    cells = list()
    
    for dx in range(-num_cells_wide, num_cells_wide+1):
        for dy in range(-num_cells_wide, num_cells_wide+1):
            #The coordinates at the center
            cx, cy= dx * width, dy * width
            diff = walk_builder.coords(cx, cy)
            
            dist_from_origin = np.hypot(cx, cy)
            if dist_from_origin < min_dist:
                continue
            if dist_from_origin > max_dist:
                continue
            
            #Now we actually need to check the corners
            ge_one = False
            le_one = False
            for disp in corner_disps:
                corner = diff + disp
                corner_dist_from_origin = np.hypot(*corner)
                if np.allclose(corner_dist_from_origin, 1, rtol=0, atol=EPS):
                    ge_one=True
                    le_one=True
                    break
                if corner_dist_from_origin >= 1:
                    ge_one = True
                if corner_dist_from_origin <= 1:
                    le_one = True
            
            if ge_one and le_one:
                cell = (dx, dy)
                cells.append(cell)
    
    return cells
    
def get_key(num, num_decimals=NUM_DECIMALS):
    if np.isclose(num, 0, rtol=0, atol=EPS):
        num = 0.0
    
    num_s = str(num)
    decimal_index = num_s.index('.')
    needed_len = decimal_index+num_decimals + 1
    len_shortfall = needed_len - len(num_s)
    if len_shortfall > 0:
        num_s = num_s + '0' * len_shortfall
    
    key = num_s[:decimal_index+num_decimals+1]
    
    #The number of decimals is fixed, so the decimal place is unnecessary
    key = key.replace('.', '')
    
    #Now the key looks like an integer, so we'll make it one
    #to make doing math with them easier
    key = int(key)
    
    return key

class PointStore:
    """
    A class to efficiently store and retrieve points in certain regions.
    """
    pass

def key_test():
    print(get_key(0.0001))
    print(get_key(0.01))
    print(get_key(-0.01))
    print(get_key(0.15))
    print(get_key(-0.15))

def ring_test():
    cell_ring = get_cell_ring()
    for cell in cell_ring:
        print(cell)