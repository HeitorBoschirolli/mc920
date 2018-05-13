#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 24 15:20:16 2018

@author: hboschirolli
"""

import numpy as np
from skimage.io import imshow, imsave

img = np.zeros((500, 1000, 3))
colors = np.random.rand(5, 10, 3)

for row in xrange(img.shape[0]):
    for col in xrange(img.shape[1]):
        img[row][col] = colors[row//100][col//100]
        
imsave('problem.png', img)