# Introduction to Digital Image Processing Project 1
The purpose of this work is to perform basic image processing, such as finding object measurements, color transformations, and collecting statistics about objects in images.

## Prerequisites
  - Python 2.7
  - scikit-image
  - numpy

## Running the program on Unix terminal (i.e. Linux or Mac)
To run the main.py file, simply type "python main.py" into a Linux terminal and press the enter key. Once the code is executed, it prompts the user to enter the name of the image to be processed in the terminal's standard entry; the image name must include its extension, and if the image is not in the same directory as the script main.py, you must pass the absolute path.

Then some properties of the image will be displayed in the terminal's default output and the <input_image_name> _grayscale.png, <input_image_name> _edges.png, <input_image_name> _labeled.png, and <input_image_name> _histogram.png images that contain the original image converted to grayscale, the edges of the original image objects, the numbered original image objects, and a histogram with the number of objects for each size (small, medium, or large) respectively will appear in the same directory as the original image. <input_image_name> represents the name of the image entered by the user at the beginning of execution.

