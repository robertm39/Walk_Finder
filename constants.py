# -*- coding: utf-8 -*-
"""
Created on Wed Sep  1 16:10:51 2021

@author: rober
"""

#Now I can globally change epsilon just by changing this one number

#It seems like calculations tend to be accurate to 15 decimal places
#so I don't want to go too close to that, or I'll get false negatives
EPS = 1e-12