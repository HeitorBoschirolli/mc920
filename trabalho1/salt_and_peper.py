#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 18:47:42 2018

@author: hboschirolli
"""

from __future__ import print_function
from skimage.color import rgb2gray
from skimage.io import imread, imsave, imshow
import numpy as np
from skimage.measure import label, regionprops
import matplotlib.pyplot as plt
import os
from skimage.filters import roberts

img = imread('objetos1.png')

for row in range (img.shape[0]):
    for col in range (img.shape[1]):
        if (np.random.rand() < 0.001):
            img[row][col][0] = 255
            img[row][col][1] = 255
            img[row][col][2] = 255
        if (np.random.rand() < 0.001):
            img[row][col][0] = 0
            img[row][col][1] = 0
            img[row][col][2] = 0
            
imsave ('salt_and_peper_objetos1.png', img)