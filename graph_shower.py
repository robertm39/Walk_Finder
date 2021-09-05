# -*- coding: utf-8 -*-
"""
Created on Sun Aug 29 13:30:15 2021

@author: rober
"""

from IPython.display import display

import numpy as np

import torch as torch

from PIL import Image, ImageDraw

def to_image_coords(point, min_x, min_y, wid, padding, dims):
    x, y = point
    x_proportion = (x - min_x) / wid
    y_proportion = (y - min_y) / wid
    
    im_width, im_height = dims
    im_width -= padding
    im_height -= padding
    
    half_pad = padding // 2
    # upper_pad = padding - lower_pad
    
    im_x = round(x_proportion * im_width) + half_pad
    im_y = round(y_proportion * im_height) + half_pad
    
    # print('im point: ({}, {})'.format(im_x, im_y))
    
    #Subtract 1 because these are actually indices
    return int(im_x) - 1, int(im_y) - 1

def get_im_points(nodes, dims=(500, 500)):
    points = list()
    xs = list()
    ys = list()
    n, _ = nodes.shape
    for i in range(n):
        x, y = nodes[i, :].detach().numpy()
        xs.append(x)
        ys.append(y)
        points.append((x, y))
    
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    
    x_wid = max_x - min_x
    y_wid = max_y - min_y
    wid = max(x_wid, y_wid)
    padding = round(0.1 * max(dims))
    
    im_points = list()
    for point in points:
        im_point = to_image_coords(point, min_x, min_y, wid, padding, dims)
        im_points.append(im_point)
    
    im_arr = np.zeros(dims, dtype=np.uint8)
    
    return im_points, im_arr

def tensor_from_list(nodes):
    t_nodes = [torch.tensor(node) for node in nodes]
    return torch.stack(t_nodes, dim=0)

#Nodes is a pytorch tensor
def make_graph_png(nodes, edges, dims=(500, 500)):
    points = list()
    xs = list()
    ys = list()
    n, _ = nodes.shape
    for i in range(n):
        # n_point = nodes[i, :].detach().numpy()
        # print('Shape: {}'.format(n_point.shape))
        x, y = nodes[i, :].detach().numpy()
        xs.append(x)
        ys.append(y)
        points.append((x, y))
    
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    
    # mid_x = (min_x + max_x) / 2.0
    # mid_y = (min_y + max_y) / 2.0
    
    x_wid = max_x - min_x
    y_wid = max_y - min_y
    wid = max(x_wid, y_wid)
    padding = round(0.1 * max(dims))
    # half_wid = wid / 2.0
    
    im_arr = np.zeros(dims, dtype=np.uint8)
    
    for point in points:
        im_x, im_y = to_image_coords(point, min_x, min_y, wid, padding, dims)
        im_arr[im_x, im_y] = 255
    
    image = Image.fromarray(im_arr, mode='L')
    image.show()

def get_line_array(im_arr, p1, p2):
    image = Image.fromarray(im_arr, mode='L')
    
    drawer = ImageDraw.Draw(image)
    color = tuple([1])
    drawer.line([p1, p2], fill=color, width=1)
    array = np.array(image, dtype=np.uint32)# / 255 #reduce the brightness
    return array

def make_smooth_graph_png_with_lines(nodes,
                                        edges,
                                        brightness=None,
                                        dims=(500, 500),
                                        filename=None,
                                        inline=True):
    
    if brightness is None:
        brightness = 16
    
    im_points, im_arr = get_im_points(nodes, dims)
    total_im_arr = np.array(im_arr, dtype=np.uint32)
    
    for i1, i2 in edges:
        p1, p2 = im_points[i1], im_points[i2]
        line_arr = get_line_array(im_arr, p1, p2) * brightness
        total_im_arr = total_im_arr + line_arr
    
    # total_im_arr = total_im_arr
    # print(type(total_im_arr))
    
    total_im_arr = np.clip(total_im_arr, a_min=0, a_max=255)
    total_im_arr = np.array(total_im_arr, dtype=np.uint8)
    
    image = Image.fromarray(total_im_arr, mode='L')
    
    if filename is None:
        filename = 'reduced_8_2.png'
    
    image.save(filename, format='png')

def make_graph_png_with_lines(nodes,
                                edges,
                                dims=(500, 500),
                                filename=None,
                                inline=True):
    im_points, im_arr = get_im_points(nodes, dims)
    
    image = Image.fromarray(im_arr, mode='L')
    
    drawer = ImageDraw.Draw(image)
    
    for i1, i2 in edges:
        p1, p2 = im_points[i1], im_points[i2]
        drawer.line([p1, p2], fill='white', width=1)
    
    # if inline:
    #     display(image)
    # else:
    #     image.show()
    if filename is None:
        filename = 'reduced_8_2.png'
    
    image.save(filename, format='png')