import cv2
import numpy
import argparse

parser = argparse.ArgumentParser()
# parser.add_argument("--angle", help="The angle (in degrees) at which the image will be rotated")
parser.add_argument(
    "-a", "--angle", type=float, help="Angle (in degrees) at which the image will be rotated counterclockwise",
    metavar='')
parser.add_argument(
    "-e", "--escale", type=float, help="Scale factor", metavar='')
parser.add_argument(
    "-d", "--dimensions", type=float, help="Output image dimensions", metavar='')
parser.add_argument(
    "-m", "--interpolation", type=str, help="What interpolation method should be used", metavar='',
    choices=['Nearest', 'Bilinear', 'Bicubic', 'Lagrange'], default='Nearest')
parser.add_argument(
    "-i", "--input", help="Name of the input image", metavar='')
parser.add_argument(
    "-o", "--output", help="Name of the output image. "
    "If not provided the output will be saved as out.png", metavar='')
parser.parse_args()
