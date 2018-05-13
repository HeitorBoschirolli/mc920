#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tur Mar 23 19:47:20 2018

@author: hboschirolli
"""
from __future__ import print_function
from skimage.color import rgb2gray
from skimage.io import imread, imsave
import numpy as np
from skimage.measure import label, regionprops
import matplotlib.pyplot as plt
import os
from skimage.filters import roberts

# open the image and save it's name without the extension
img_name = raw_input("Enter the image name: ")
img = imread(img_name)
img_name = os.path.splitext(img_name)[0]

# convert the image to grayscale and save it
gray_img = rgb2gray(img)
imsave(img_name + '_grayscale.png', gray_img)

# binarize the image to make contour detection and labeling simpler
b_and_w = np.copy(gray_img)
b_and_w[b_and_w < 1] = 0

# detect and plot the contours
edges_img = roberts(b_and_w)
edges_img = 1 - edges_img
imsave(img_name + '_edges.png', edges_img)

# label the objects of the image and get it's properties
labeled, num = label(b_and_w, connectivity=1, background=1, return_num=True)
properties_list = regionprops(labeled, intensity_image=b_and_w)

# output some of the properties of the objects
for i in xrange(len(properties_list)):
    print('region: %-d \t perimeter: %-d  \t area: %-d' % 
          (i, properties_list[i].perimeter, properties_list[i].area))

# write the label of each object on the the grayscaled image and save it
plt.imshow(gray_img, cmap='gray')
i = 0
for element in properties_list[:]:
    plt.text(int(element.centroid[1]) - 7, int(element.centroid[0]) + 5, str(i),
             color='red', fontsize=10)
    i += 1
plt.savefig(img_name + '_labeled.png')
plt.gcf().clear()

# get how many objects are large (>= 3000 pixels), small(< 1500 pixels) and ...
# ... medim (others)
sizes = np.empty(len(properties_list))
for i in xrange(len(properties_list)):
    sizes[i] = properties_list[i].area

# plot the histogram of how many images are small, medium and large
plt.rcParams["patch.force_edgecolor"] = True
plt.hist(sizes, bins=[0, 1500, 3000, max(sizes.max(), 4500)], color='orange')
plt.ylabel('Number of objects')
plt.xlabel('Area')
plt.title("Area's histogram")
plt.savefig(img_name + '_histogram.png')
