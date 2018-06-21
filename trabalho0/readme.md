# Introduction to Digital Image Processing Project 0
The goal of this project is to perform some basic processing in grayscale images and collect some of the image's statistical measures. The statistic measures are height, weight, max, min and average intensities. The processing consists of interting the intensity levels of the image (i.e. perform 255 - px_value for all pixels) and rescale it.

## Prerequisites
  - Python 2.7
  - scikit-image
  - numpy

## Running the program on Unix terminal (i.e. Linux or Mac)
To run the program, just type "python main.py" on the directory of the source code (i.e. do arquivo main.py). If python 3 is the default for your envirnoment, type "python2 main.py" instead.
After that, the program will ask for the name of the image on which it will perform the processing, both the absolute and the relative paths can be used, the extension is also required. Following that, some of the image statistic will appear in the standard terminal output and images with the name input_name_histogram , input_name_rescaled and input_name_inverted will appear on the same directory as the input image was.

### Example
hboschirolli:~/unicamp/current/mc920/trabalho0 $ python2 main.py

Enter the image name: baboon.png

image height: 512

image width: 512

minimum intensity: 0

maximum intensity: 230

average intensity: 129.147018433

