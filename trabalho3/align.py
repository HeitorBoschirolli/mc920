#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun May 13 20:23:16 2018

@author: hboschirolli
"""

import numpy as np
import cv2
import sys

"""
input: numpy array
output: the array's sum of the squared differences
"""
def sds (vector):
    total = 0
    
    for i in range(vector.shape[0] - 1):
        total += pow(vector[i] - vector[i - 1], 2)
    return total

"""
input: grayscale image name
output: aligned grayscale image
"""
def hough_align(input_image):
    img = cv2.imread(input_image, 0)
    edges = cv2.Canny(img, 50, 150, apertureSize = 3)
    lines = cv2.HoughLines(edges, 1, np.pi/180, 30)
    
    rho = lines[0][0][1] # angle of the line with greater number of points
    rho = -rho * 180/(np.pi) + 90
    M = cv2.getRotationMatrix2D((img.shape[1]/2, img.shape[0]/2), rho, 1)
    return cv2.warpAffine(img,M,(img.shape[1], img.shape[0]))
    
"""
input: grayscale image name
output: aligned grayscale image
"""
def vproj_align(input_image):
    img = cv2.imread(input_image, 0)
    initial = img # save the initial image to apply the rotation later
    
    img = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                cv2.THRESH_BINARY_INV,11,2)
    img = cv2.medianBlur(img, 3)
    kernel = np.ones((3, 3))
    img = cv2.dilate(img,kernel,iterations=1)
    
    rev = np.empty(img.shape)
    best = None
    best_angle = None
    
    # set the background to black and the text to white
    rev[img != 0] = 1
    rev[img == 0] = 0 
    
    for theta in range (0, 360):
        temp = rev
        M = cv2.getRotationMatrix2D((temp.shape[1]/2, temp.shape[0]/2), theta, 1)
        temp = cv2.warpAffine(temp, M,(temp.shape[1], temp.shape[0]))
        perfil = np.ndarray.sum(temp, axis=1)
        current = sds(perfil)
        
        # save the best angle so far
        if (best == None or current > best):
            best = current
            best_angle = theta
    
    M = cv2.getRotationMatrix2D((temp.shape[1]/2, temp.shape[0]/2), best_angle, 1)
    return cv2.warpAffine(initial,M,(img.shape[1], img.shape[0]))

if __name__ == "__main__":
    
    # if the number of parameters is wrong, hint the right usage and terminate
    if (len(sys.argv) != 4):
        print "Usage: align.py input_image.png mode output_image.png"
        print "Mode can be 0 (align using vertical projection) ",
        print "or 1 (align using Hough's transform)"
        exit()

    input_image = sys.argv[1]
    mode = sys.argv[2]
    output_image = sys.argv[3]
    
    if (int(mode) == 0):
        res = hough_align(input_image)
    elif (int(mode) == 1):
        res = vproj_align(input_image)
    else:
        print "the mode must be 0 or 1"
        exit()
    
    cv2.imwrite(output_image, res)
