#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun May 13 18:31:44 2018

@author: hboschirolli
"""

import numpy as np
import cv2

img = cv2.imread('sample1.png')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 50, 150, apertureSize = 3)

#cv2.imshow('image', img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
#
#cv2.imshow('image', edges)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

lines = cv2.HoughLines(edges, 1, np.pi/180, 30)
#for rho,theta in lines[0]:
#    a = np.cos(theta)
#    b = np.sin(theta)
#    x0 = a*rho
#    y0 = b*rho
#    x1 = int(x0 + 1000*(-b))
#    y1 = int(y0 + 1000*(a))
#    x2 = int(x0 - 1000*(-b))
#    y2 = int(y0 - 1000*(a))
#
#    cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)

rho = lines[0][0][1]
rho = -rho * 180/(np.pi) + 90
M = cv2.getRotationMatrix2D((img.shape[1]/2, img.shape[0]/2), -rho, 1)
img = cv2.warpAffine(img,M,(img.shape[1], img.shape[0]))

    
cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
