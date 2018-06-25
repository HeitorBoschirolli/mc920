#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
@author: hboschirolli
"""

import sys
import numpy as np
import cv2
import os

# if the program is called incorrectly, warns the user and end the program
if (len(sys.argv) != 5):
    print "how to use the program:"
    print "python " + sys.argv[0] + " <input_image> <input_message> <bit_plane> <output_image>"
    sys.exit()
    
img_name = sys.argv[1]
message_name = sys.argv[2]
bit_plane = sys.argv[3]
out_img_name = sys.argv[4]

simple_name = os.path.splitext(sys.argv[1])[0] #image name without the extention  .png

img = cv2.imread(img_name, 1)
message = open(message_name, 'r')
message_sting = message.read()
message.close()

n_rows = img.shape[0]
n_cols = img.shape[1]
# if the message is too big to fit the image, warns the user and end the program
# the +1 is for the stop code 
if len(message_sting) + 1 > (n_rows * n_cols * 3)/8:
    print "the message is too big for this image"
    print "choose a bigger imager or use a smaller message"
    sys.exit()
    
# convert the message into a list of strings in which string is the binary...
# ... representation of a character from the message
bin_message = ['{0:08b}'.format(ord(c)) for c in message_sting]

i = 0 # index of the next character to be placed in the image
channel = 2 # red channel
row = 0 # row of the image to place the next character
col = 0 # column of the image to place the next character
while (i < len(bin_message)):
    # place a character in the image
    for j in xrange(8):
        img[row][col][channel] &= ~(1 << int(bit_plane))
        img[row][col][channel] |= int(bin_message[i][j]) << int(bit_plane)
        channel -= 1
        
        # if red, blue and green have been used, go back to red
        if (channel == -1):
            channel = 2
            col +=1
            # if it is the end of a row, go to the next one
            if col >= n_cols:
                row += 1
                col = 0
    i += 1

# write the stop code '00000000' after the message
for j in xrange(8):
    img[row][col][channel] &= ~(1 << int(bit_plane))
    channel -= 1
    if (channel == -1):
        channel = 2
        col +=1
        if col >= n_cols:
            row += 1
            col = 0

cv2.imwrite(out_img_name, img)

# produces and saves images containing the first, the secont, the third and ...
# ... the last bit planes of the image
first_plane = np.empty(img.shape)
second_plane = np.empty(img.shape)
third_plane = np.empty(img.shape)
last_plane = np.empty(img.shape)

first_plane[:, :, 2] = ((img[:,:,2] >> 0) % 2) * 255
first_plane[:, :, 1] = ((img[:,:,1] >> 0) % 2) * 255
first_plane[:, :, 0] = ((img[:,:,0] >> 0) % 2) * 255
cv2.imwrite(simple_name + "_first_plane.png", first_plane)

second_plane[:, :, 2] = ((img[:,:,2] >> 1) % 2) * 255
second_plane[:, :, 1] = ((img[:,:,1] >> 1) % 2) * 255
second_plane[:, :, 0] = ((img[:,:,0] >> 1) % 2) * 255
cv2.imwrite(simple_name + "_second_plane.png", second_plane)

third_plane[:, :, 2] = ((img[:,:,2] >> 2) % 2) * 255
third_plane[:, :, 1] = ((img[:,:,1] >> 2) % 2) * 255
third_plane[:, :, 0] = ((img[:,:,0] >> 2) % 2) * 255
cv2.imwrite(simple_name + "_third_plane.png", third_plane)

last_plane[:, :, 2] = ((img[:,:,2] >> 7) % 2) * 255
last_plane[:, :, 1] = ((img[:,:,1] >> 7) % 2) * 255
last_plane[:, :, 0] = ((img[:,:,0] >> 7) % 2) * 255
cv2.imwrite(simple_name + "_last_plane.png", last_plane)