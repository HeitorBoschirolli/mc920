#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tur Mar 23 19:47:20 2018

@author: hboschirolli
"""
from __future__ import print_function
#from skimage.filters import sobel
from skimage.color import rgb2gray
from skimage.io import imread, imsave
import numpy as np
from skimage.measure import label, regionprops
import matplotlib.pyplot as plt
import os
from skimage.measure import find_contours
import cv2


# open the image and save it's name without the .png extension
img_name = raw_input("Enter the image name: ")
img = imread(img_name)
img_name = os.path.splitext(img_name)[0]

# convert the image to grayscale and save it
gray_img = rgb2gray(img)
imsave(img_name + '_grayscale.png', gray_img)

# binarize the image to make edge detection and labeling simpler
b_and_w = np.copy(gray_img)
b_and_w[b_and_w < 1] = 0


_, edges_img = cv2.threshold(gray_img,0,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C)
edges_img = 255 - edges_img
cv2.imwrite(img_name + '_edges.png', edges_img)

#contours = find_contours(b_and_w, 0)
#fig, ax = plt.subplots()
#for n, contour in enumerate(contours):
#    ax.plot(contour[:, 1], contour[:, 0], linewidth=1)
#plt.savefig('test.png')
#plt.gcf().clear()

# detect the edges of the objects
# any pixel inside an object and with 4-neighborhood with at least one background
# pixel is considered an edge pixel
#edges_img = np.empty(gray_img.shape)
#for row in xrange(gray_img.shape[0]):
#    for col in xrange(gray_img.shape[1]):
#        is_edge = False
#        if gray_img[row][col] != 1:
#            if row > 0 and gray_img[row - 1][col] == 1:
#                is_edge = True
#            elif col > 0 and gray_img[row][col - 1] == 1:
#                is_edge = True
#            elif row < gray_img.shape[0] - 1 and gray_img[row + 1][col] == 1:
#                is_edge = True
#            elif col < gray_img.shape[1] - 1 and gray_img[row][col + 1] == 1:
#                is_edge = True
#        if is_edge:
#            edges_img[row][col] = 0
#        else:
#            edges_img[row][col] = 1            
#imsave(img_name + '_edges.png', edges_img)

# label the objects of the image and get it's properties
labeled, num = label(b_and_w, connectivity=1, background=1, return_num=True)
properties_list = regionprops(labeled, intensity_image=b_and_w)

# output some of the properties of the objects
for i in xrange(len(properties_list)):
    print('região: %-d \t perímetro: %-d  \t area: %-d' % (i, properties_list[i].perimeter, properties_list[i].area))

# write the label of each object on the the grayscaled image and save it
plt.imshow(gray_img, cmap='gray')
i = 0
for element in properties_list[:]:
    plt.text(int(element.centroid[1]) - 7, int(element.centroid[0]) + 5, str(i), color='red', fontsize=10)
    i += 1
plt.savefig(img_name + '_labeled.png')
plt.gcf().clear()

# get how many objects are large (>= 3000 pixels), small(< 1500 pixels) and
# medim (others)
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
