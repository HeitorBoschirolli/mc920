#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May 10 16:49:54 2018

@author: hboschirolli
"""

import numpy as np
import cv2
import matplotlib.pyplot as plt

def sds (vector):
    total = 0
    
    for i in range(vector.shape[0] - 1):
        total += pow(vector[i] - vector[i - 1], 2)
    
    return total


img = raw_input('poe o nome ai: ')
img = cv2.imread(img, 0)
initial = img
#cv2.imshow('image', img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

img = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,11,2)

#cv2.imshow('image', img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

img = cv2.medianBlur(img, 3)

#cv2.imshow('image', img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

kernel = np.ones((3, 3))
img = cv2.dilate(img,kernel,iterations =1)

#cv2.imshow('image', img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

temp = np.empty(img.shape)
best = -1
best_angle = 99999
best_perfil = 999999
for theta in range (1, 360):
    temp[img != 0] = 1
    temp[img == 0] = 0
    perfil = np.ndarray.sum(temp, axis=1)
    M = cv2.getRotationMatrix2D((temp.shape[1]/2, temp.shape[0]/2), theta, 1)
    temp = cv2.warpAffine(temp, M,(temp.shape[1], temp.shape[0]))
    perfil = np.ndarray.sum(temp, axis=1)
    current = sds(perfil)
    
    if (best == -1 or current > best):
        best = current
        best_angle = theta
        best_perfil = perfil

print str(best_angle)

M = cv2.getRotationMatrix2D((img.shape[1]/2, img.shape[0]/2), best_angle, 1)
img = cv2.warpAffine(initial,M,(img.shape[1], img.shape[0]))

cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

bar_width = 1. # set this to whatever you want
data = best_perfil
positions = np.arange(perfil.shape[0])
plt.bar(positions, data, bar_width)
#plt.xticks(positions + bar_width / 2, range(perfil.shape[0]))
plt.show()
