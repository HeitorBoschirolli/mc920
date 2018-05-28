import cv2
import numpy as np
import argparse
import math


def P (t):
    return max (t, 0)

def R (s):
    return 1.0 / 6 * (pow(P(s + 2), 3) - 4 * pow(P(s + 1), 3) + 6 * pow(P(s), 3) - 4 * pow(P(s - 1), 3))

def L (n, x, y, dx, dy, f):
    ret = -dx * (dx - 1) * (dx - 2) * f[x - 1][y + n - 2]/6.0
    ret += (dx + 1) * (dx - 1) * (dx - 2) * f[x][y + n - 2]/2.0
    ret += -dx * (dx + 1) * (dx - 2) * f[x + 1][y + n - 2]/2.0
    ret += dx * (dx + 1) * (dx - 1) * f[x + 2][y + n - 2]/6.0

    return ret

def nearest (x_, y_, input):
    return input[round(x_)][round(y_)]

def bilinear (x_, y_, input):
    dx = x_ - math.floor(x_)
    dy = y_ - math.floor(y_)
    x = math.floor(x_)
    y = math.floor(y_)
    ret = (1 - dx) * (1 - dy) * input[x][y] + dx * (1 - dy) * input[x + 1][y]
    ret += (1 - dx) * dy * input[x][y + 1] + dx * dy * input[x + 1][y + 1]
    return ret

def bicubic (x_, y_, input):
    dx = x_ - math.floor(x_)
    dy = y_ - math.floor(y_)
    x = math.floor(x_)
    y = math.floor(y_)
    x = math.floor(x)
    y = math.floor(y)
    acc = 0
    for m in range(-1, 3):
        for n in range (-1, 3):
            acc += input[x + m][y + n] * R(m - dx) * R(dy - n)
    return acc

def lagrange (x_, y_, input):
    dx = x_ - math.floor(x_)
    dy = y_ - math.floor(y_)
    x = math.floor(x_)
    y = math.floor(y_)
    L1 = L(1, x, y, dx, dy, input)
    L2 = L(2, x, y, dx, dy, input)
    L3 = L(3, x, y, dx, dy, input)
    L4 = L(4, x, y, dx, dy, input)
    acc = - dy * (dy - 1) * (dy - 2) * L1/ 6.0
    acc += (dy + 1) * (dy - 1) * (dy - 2) * L2/ 2.0
    acc += -dy * (dy + 1) * (dy - 2) * L3/ 2.0
    acc += dy * (dy + 1) * (dy - 1) * L4 / 6.0
    
    return acc

def rescale (img, interpolation, output_dimension=None, scale_factor=None):
    if output_dimension != None and scale_factor == None:
        x_dim = output_dimension[0]
        y_dim = output_dimension[1]
        scale_factor = float(x_dim)/img.shape[0]
    elif scale_factor != None and output_dimension == None:
        x_dim = math.ceil (img.shape[0] * scale_factor)
        y_dim = math.ceil (img.shape[1] * scale_factor)
        x_dim = int(x_dim)
        y_dim = int(y_dim)
    else:
        print("error in method 'rescale'")
        exit()
    
    rescaled = np.empty((x_dim, y_dim))
    if interpolation == 'Nearest':
        for i in range (rescaled.shape[0] - 1):
            for j in range (rescaled.shape[1] - 1):
                x_ = float(i) / scale_factor
                y_ = float(j) / scale_factor
                rescaled[i][j] = nearest(x_, y_, img)
        
        for i in range (rescaled.shape[0]):
            rescaled[i][rescaled.shape[1] - 1] = rescaled[i][rescaled.shape[1] - 2]
        for i in range (rescaled.shape[1]):
            rescaled[rescaled.shape[0] - 1][i] = rescaled[rescaled.shape[0] - 2][i]
    elif interpolation == 'Bilinear':
        for i in range (rescaled.shape[0] - 3):
            for j in range (rescaled.shape[1] - 3):
                x_ = float(i) / scale_factor
                y_ = float(j) / scale_factor
                rescaled[i][j] = bilinear(x_, y_, img)
    elif interpolation == 'Bicubic':
        for i in range (1, rescaled.shape[0] - 5):
            for j in range (1, rescaled.shape[1] - 5):
                x_ = float(i) / scale_factor
                y_ = float(j) / scale_factor
                rescaled[i][j] = bicubic(x_, y_, img)
    elif interpolation == 'Lagrange':
        for i in range (1, rescaled.shape[0] - 5):
            for j in range (1, rescaled.shape[1] - 5):
                x_ = float(i) / scale_factor
                y_ = float(j) / scale_factor
                rescaled[i][j] = lagrange(x_, y_, img)
    else:
        print("error in method 'rescale_factor'")
        exit()

    return rescaled

parser = argparse.ArgumentParser()
parser.add_argument(
    "-a", "--angle", type=float, help="Angle (in degrees) at which the image will be rotated counterclockwise",
    metavar='')
parser.add_argument(
    "-e", "--scale", type=float, help="Scale factor", metavar='')
parser.add_argument(
    "-d", "--dimensions", type=int, help="Output image dimensions", metavar='', nargs="+")
parser.add_argument(
    "-m", "--interpolation", type=str, help="What interpolation method should be used", metavar='',
    choices=['Nearest', 'Bilinear', 'Bicubic', 'Lagrange'], default='Nearest')
parser.add_argument(
    "-i", "--input", help="Name of the input image", metavar='')
parser.add_argument(
    "-o", "--output", help="Name of the output image. "
    "If not provided the output will be saved as out.png", metavar='')
args = parser.parse_args()

if args.input == None:
    print("No input image especified")
    exit()
if args.angle == None and args.scale == None and args.dimensions == None:
    print("The image must be rotated or scaled")
    exit()
if args.angle != None and (args.scale != None or args.dimensions != None):
    print("Only one operation (rotate or rescale) can be done at a time")
    exit()
if args.scale != None and args.dimensions != None:
    print("Define only scale or output dimension to rescale the image")
    exit()
if args.dimensions != None:
    if len(args.dimensions) > 2: 
        print("Output image must be bidimensional")
        exit()
if args.output == None:
    message = "WARNING: no output image defined, the output will be saved as out.png "
    message += "overwriting any file with this name in the process."
    print (message)
    print("Wish to continue?")
    while (True):
        res = input("(Y)es or (N)o: ")
        if (res == 'Y') or res == 'YES' or res == 'yes' or res == 'Yes' or res == 'y':
            break
        if res == 'N' or res == 'NO' or res == 'no' or res == 'No' or res == 'n':
            exit()

img = cv2.imread(args.input, 0)
print (img.shape)
rescaled = rescale(img, args.interpolation, scale_factor=args.scale, output_dimension=args.dimensions)
cv2.imwrite('out.png', rescaled)

cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

rescaled = np.array(rescaled, dtype=np.uint8)

cv2.imshow('image2', rescaled)
cv2.waitKey(0)
cv2.destroyAllWindows()

print (rescaled.shape)
