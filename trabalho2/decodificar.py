#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
@author: hboschirolli
"""

import sys
import numpy as np
import cv2

if (len(sys.argv) != 4):
    print "how to use the program:"
    print "python " + sys.argv[0] + " <input_image> <image_with_message> <bit_plane> <output_message_file>"
    sys.exit()
    
img_name = sys.argv[1]
bit_plane = int(sys.argv[2])
message_name = sys.argv[3]

img = cv2.imread(img_name, 1)
n_rows = img.shape[0]
n_cols = img.shape[1]

i = 0 # index of the next character to be read from the image
channel = 2 # red channel
row = 0 # row of the image from which to read the next character
col = 0 # column of the image from which to read the next character
message = ''
stop_code = False
while (not(stop_code)):
    letter = ''
    stop_code = True
    # read a character from the image
    for j in xrange(8):
        # if the bit is no 0, cannot be the stop code
        if (((img[row][col][channel] & (1 << bit_plane)) >> bit_plane) == 1):
            stop_code = False
        letter += str(((img[row][col][channel] & (1 << bit_plane)) >> bit_plane))
        channel -= 1
        
        # if red, blue and green have been used, go back to red
        if (channel == -1):
            channel = 2
            col +=1
            # if it is the end of a row, go to the next one
            if col >= n_cols:
                row += 1
                col = 0
    if not(stop_code):
        message += chr(int(letter, 2))
    i += 1
    
message_file = open(message_name, 'w')
message_file.write(message)