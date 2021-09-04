# -*- coding: utf-8 -*-
"""
Created on Wed Sep  1 15:30:46 2021

@author: rober
"""

import random

import numpy as np

import walk_builder

from constants import EPS

NUM_DECIMALS = 2

# EPS = 1e-10

#I'm not actually gonna support changing the number of decimal places for now
#Actually I will

#What I thought was the center was actually the lower-left corner

#The cells that could have something in roughly the same place
#This works as long as epsilon is reasonably small
SAME_RING = (( 0,  0),
             ( 1,  0),
             ( 1,  1),
             ( 0,  1),
             (-1,  1),
             (-1,  0),
             (-1, -1),
             ( 0, -1),
             ( 1, -1))

def get_cell_ring(num_decimals=NUM_DECIMALS, _cache=dict()):
    if num_decimals in _cache:
        return _cache[num_decimals]
    
    width = 10**(-num_decimals)
    num_cells_wide = 10 ** num_decimals #How many cells wide a 1x1 square is
    
    diag = width * np.sqrt(2)
    
    #Pad by EPS to make sure
    min_dist = 1 - diag - EPS
    max_dist = 1 + diag + EPS
    
    corner_disps = (walk_builder.coords(0, 0),
                    walk_builder.coords(0, width),
                    walk_builder.coords(width, width),
                    walk_builder.coords(width, 0))
    
    #The most the maximum and minimum distance can differ from the distance
    #between the centers is at most this much
    #(this is an overestimate, which is good anyways)
    
    cells = set()
    
    for dx in range(-num_cells_wide-1, num_cells_wide+2):
        for dy in range(-num_cells_wide-1, num_cells_wide+2):
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
            
            #Before, I was just doing these with one
            #I need to apply them to both
            
            for d1 in corner_disps:
                for d2 in corner_disps:
                    #d1 is the disp from the cell to its corner
                    #d2 is the disp from the origin to its corner
                    corner_to_corner = diff + d1 - d2
                    overall_dist = np.hypot(*corner_to_corner)
                    
                    if np.isclose(overall_dist, 1, rtol=0, atol=EPS):
                        ge_one=True
                        le_one=True
                        break
                    if overall_dist >= 1:
                        ge_one = True
                    if overall_dist <= 1:
                        le_one = True
    
            if ge_one and le_one:
                cell = (dx, dy)
                cells.add(cell)
    
    result = list(cells)
    
    _cache[num_decimals] = result
    
    return result

def get_cell_disk(num_decimals=NUM_DECIMALS, _cache=dict()):
    if num_decimals in _cache:
        return _cache[num_decimals]
    
    width = 10**(-num_decimals)
    num_cells_wide = 10 ** num_decimals #How many cells wide a 1x1 square is
    
    diag = width * np.sqrt(2)
    # min_dist = 2 - diag
    max_dist = 2 + diag
    
    corner_disps = (walk_builder.coords(0, 0),
                    walk_builder.coords(0, width),
                    walk_builder.coords(width, width),
                    walk_builder.coords(width, 0))
    
    #The most the maximum and minimum distance can differ from the distance
    #between the centers is at most this much
    #(this is an overestimate, which is good anyways)
    
    cells = set()
    
    for dx in range(-num_cells_wide*2-2, num_cells_wide*2+4):
        for dy in range(-num_cells_wide*2-2, num_cells_wide*2+4):
            #The coordinates at the center
            cx, cy= dx * width, dy * width
            diff = walk_builder.coords(cx, cy)
            
            dist_from_origin = np.hypot(cx, cy)
            # if dist_from_origin < min_dist:
            #     continue
            if dist_from_origin > max_dist:
                continue
            
            #Now we actually need to check the corners
            # ge_one = False
            le_two = False
            
            #Before, I was just doing these with one
            #I need to apply them to both
            
            for d1 in corner_disps:
                for d2 in corner_disps:
                    #d1 is the disp from the cell to its corner
                    #d2 is the disp from the origin to its corner
                    corner_to_corner = diff + d1 - d2
                    overall_dist = np.hypot(*corner_to_corner)
                    
                    if np.isclose(overall_dist, 2, rtol=0, atol=EPS):
                        # ge_one=True
                        le_two=True
                        break
                    # if overall_dist >= 1:
                    #     ge_one = True
                    if overall_dist <= 2:
                        le_two = True
    
            if le_two:
                cell = (dx, dy)
                cells.add(cell)
    
    result = list(cells)
    
    _cache[num_decimals] = result
    
    return result

def homogenize(num_s):
    """
    Make it so num_s is in decimal format.
    """
    
    #Deal with numbers that don't have a decimal
    if not '.' in num_s:
        num_s = num_s + '.'
        return num_s #There shouldn't be anything more to do
    
    #Deal with numbers in scientific notation
    if 'e' in num_s:
        e_index = num_s.index('e')
        exponent = int(num_s[e_index+1:])
        mantissa = num_s[:e_index]
        
        #Move the decimal point according to the mantissa
        
        #Strip the negative, add it later
        negative = mantissa[0] == '-'
        mantissa = mantissa.replace('-', '')
        
        decimal_index = mantissa.index('.')
        new_index = decimal_index + exponent #This works nicely
        
        mantissa = mantissa.replace('.', '')
        
        #The decimal point will be to the left of everything
        if new_index <= 0:
            pad_zeros = abs(new_index)
            mantissa = '0.' + '0'*pad_zeros + mantissa
        #The decimal point will be to the right of everything
        elif new_index >= len(mantissa):
            pad_zeros = new_index - len(mantissa)
            mantissa = mantissa + '0'*pad_zeros + '.0'
        #The decimal point will be in the middle
        else:
            mantissa = mantissa[:new_index] + '.' + mantissa[new_index:]
        
        if negative:
            mantissa = '-' + mantissa
        
        return mantissa
    
    return num_s

# def pad(num_s):
#     decimal_index = num_s.index('.')
#     needed_len = decimal_index+num_decimals + 1
#     len_shortfall = needed_len - len(num_s)
#     if len_shortfall > 0:
#         num_s = num_s + '0' * len_shortfall
    
#     return num_s

def get_key(num, num_decimals=NUM_DECIMALS):
    num_s = str(num)
    num_s = homogenize(num_s)
    
    decimal_index = num_s.index('.')
    needed_len = decimal_index+num_decimals + 1
    len_shortfall = needed_len - len(num_s)
    if len_shortfall > 0:
        num_s = num_s + '0' * len_shortfall
    
    key = num_s[:decimal_index+num_decimals+1]
    
    #The number of decimals is fixed, so the decimal place is unnecessary
    key = key.replace('.', '')
    
    #To make this work, we need to make the negative keys one lower
    if key[0] == '-':
        subkey = key[1:]
        subkey = int(subkey) + 1
        key = -subkey
    else:
        key = int(key)
    
    #Now the key looks like an integer, so we'll make it one
    #to make doing math with them easier
    # key = int(key)
    
    return key

class PointStore:
    """
    A class to efficiently store and retrieve points in certain regions.
    """
    def __init__(self,
                 unit=True,
                 same=True,
                 two=False,
                 num_decimals=NUM_DECIMALS):
        #Store that values that are approximately unit distance away
        self.unit = unit
        self.same = same
        self.two = two
        
        if self.unit:
            self.one_dist_from_cells = dict()
            self.unit_ring = get_cell_ring(num_decimals=num_decimals)
        
        #Store the values that are in roughly the same place
        if self.same:
            self.same_from_cells = dict()
        
        if self.two:
            self.two_dist_from_cells = dict()
            self.two_disk = get_cell_disk(num_decimals=num_decimals)
        
        self.num_decimals = num_decimals
        
    
    def __setitem__(self, coords, value):
        """
        Put the given value at the given coords.
        """
        x, y = coords[0], coords[1]
        x_key = get_key(x, num_decimals=self.num_decimals)
        y_key = get_key(y, num_decimals=self.num_decimals)
        val = (coords, value)
        
        #Put the value in the appropriate unit-ring buckets.
        if self.unit:
            for dx, dy in self.unit_ring:
                total_x = x_key + dx
                total_y = y_key + dy
                
                key = (total_x, total_y)
                if not key in self.one_dist_from_cells:
                    self.one_dist_from_cells[key] = list()
                
                #Store both the coords and the value in case they're needed
                # val = (coords, value)
                self.one_dist_from_cells[key].append(val)
        
        #Put the value in the appropriate same-place buckets.
        if self.same:
            for dx, dy in SAME_RING:
                total_x = x_key + dx
                total_y = y_key + dy
                
                key = (total_x, total_y)
                if not key in self.same_from_cells:
                    self.same_from_cells[key] = list()
                
                #Store both the coords and the value in case they're needed
                # val = (coords, value)
                self.same_from_cells[key].append(val)
        
        #Put the value in the appropriate two-disk buckets.
        if self.two:
            for dx, dy in self.two_disk:
                total_x = x_key + dx
                total_y = y_key + dy
                
                key = (total_x, total_y)
                if not key in self.two_dist_from_cells:
                    self.two_dist_from_cells[key] = list()
                
                #Store both the coords and the value in case they're needed
                # val = (coords, value)
                self.two_dist_from_cells[key].append(val)
    
    def get_entries_one_away(self, coords):
        x, y = coords[0], coords[1]
        x_key = get_key(x, num_decimals=self.num_decimals)
        y_key = get_key(y, num_decimals=self.num_decimals)
        key = (x_key, y_key)
        
        return self.one_dist_from_cells.get(key, list())
    
    def get_entries_in_same_place(self, coords):
        x, y = coords[0], coords[1]
        x_key = get_key(x, num_decimals=self.num_decimals)
        y_key = get_key(y, num_decimals=self.num_decimals)
        key = (x_key, y_key)
        
        return self.same_from_cells.get(key, list())

    def get_entries_within_two(self, coords):
        x, y = coords[0], coords[1]
        x_key = get_key(x, num_decimals=self.num_decimals)
        y_key = get_key(y, num_decimals=self.num_decimals)
        key = (x_key, y_key)
        
        return self.two_dist_from_cells.get(key, list())

def key_test():
    print(get_key(0.0001))
    print(get_key(-0.0001))
    print(get_key(0.01))
    print(get_key(-0.01))
    print(get_key(0.15))
    print(get_key(-0.15))

def ring_test():
    cell_ring = get_cell_ring()
    for cell in cell_ring:
        print(cell)

def point_store_test():
    point_store = PointStore()
    point_store[0, 0] = 'The origin'
    # print(point_store.get_entries_one_away([1, 0]))
    
    print('Testing point store')
    succeeded = True
    # for degrees in range(0, 3600000):
    #     theta = degrees * np.pi / 1800000
    #     x = np.cos(theta)
    #     y = np.sin(theta)
        
    #     entries = point_store.get_entries_one_away([x, y])
    #     if len(entries) != 1:
    #         print('Failed at x={}, y={}'.format(x, y))
    #         succeeded=False
    
    #Test a million random pairs of points
    for i in range(1, 1000000 + 1):
        point_store = PointStore()
        x = random.random() + random.randint(-5, 5)
        y = random.random() + random.randint(-5, 5)
        
        x *= 10 ** (random.randint(-10, 3))
        y *= 10 ** (random.randint(-10, 3))
        
        theta = random.random() * np.pi * 2
        
        x2 = x + np.cos(theta)
        y2 = y + np.sin(theta)
        
        point_store[x, y] = 'Thing'
        entries = point_store.get_entries_one_away((x2, y2))
        
        if len(entries) != 1:
            print('Failed at ({}, {}), ({}, {})'.format(x, y, x2, y2))
            succeeded = False
            
            #Do it again for debugging
            point_store = PointStore()
            point_store[x, y] = 'Thing'
            entries = point_store.get_entries_one_away((x2, y2))
        
        if i % 10000 == 0:
            print('Tested {} pairs of points'.format(i))
        
    if succeeded:
        print('Succeeded')


def point_store_two_test():
    print('Testing Point Store for coords within two')
    
    
    point_store = PointStore(num_decimals=0,
                             unit=False,
                             same=False,
                             two=True)
    # print(len(point_store.two_disk))
    
    succeeded=True
    #Test for a million pairs
    for i in range(1, 1000000 + 1):
        point_store = PointStore(num_decimals=0,
                                 unit=False,
                                 same=False,
                                 two=True)
        x = random.random() + random.randint(-5, 5)
        y = random.random() + random.randint(-5, 5)
        
        x *= 10 ** (random.randint(-10, 3))
        y *= 10 ** (random.randint(-10, 3))
        
        theta = random.random() * np.pi * 2
        r = random.random() * 2
        
        x2 = x + r * np.cos(theta)
        y2 = y + r * np.sin(theta)
        
        point_store[x, y] = 'Thing'
        entries = point_store.get_entries_within_two((x2, y2))
        
        if len(entries) != 1:
            print('Failed at ({}, {}), ({}, {})'.format(x, y, x2, y2))
            succeeded = False
            
            #Do it again for debugging
            point_store = PointStore()
            point_store[x, y] = 'Thing'
            entries = point_store.get_entries_within_two((x2, y2))
        
        if i % 10000 == 0:
            print('Tested {} pairs of points'.format(i))
        
    if succeeded:
        print('Succeeded')

def point_store_same_test():
    point_store = PointStore()
    point_store[0, 0] = 'The origin'
    
    print(point_store.get_entries_in_same_place([-0.0001, 0.0001]))