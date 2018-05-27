import cv2
import numpy as np
import argparse
import math

# def rescale_dimension (img, interpolation, dimension):
#     if interpolation == 'Nearest':
#         pass
#     elif interpolation == 'Bilinear':
#         pass
#     elif interpolation == 'Bicubic':
#         pass
#     elif interpolation == 'Lagrange':
#         pass
#     else:
#         print("error in method 'rescale_dimension'")
#         exit()

# def rescale_factor (img, interpolation, factor):
#     x_dim = math.ceil (img.shape[0] * factor) - 1
#     y_dim = math.ceil (img.shape[1] * factor) - 1
#     rescaled = np.empty((x_dim, y_dim))

#     if interpolation == 'Nearest':
#         for i in range (rescaled.shape[0]):
#             for j in range (rescaled.shape[1]):
#                 rescaled[i][j] = img[round(i/factor)][round(j/factor)]
#     elif interpolation == 'Bilinear':
#         pass
#     elif interpolation == 'Bicubic':
#         pass
#     elif interpolation == 'Lagrange':
#         pass
#     else:
#         print("error in method 'rescale_factor'")
#         exit()

#     return rescaled

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
                x = int(round(i/scale_factor))
                y = int(round(j/scale_factor))
                rescaled[i][j] = img[x][y]
    elif interpolation == 'Bilinear':
        for i in range (rescaled.shape[0] - 3):
            for j in range (rescaled.shape[1] - 3):
                x = i/float(scale_factor)
                y = j/float(scale_factor)
                dx = x - math.floor(x)
                dy = y - math.floor(y)
                x = math.floor(x)
                y = math.floor(y)
                rescaled[i][j] = (1 - dx) * (1 - dy) * img[x][y] + dx * (1 - dy) * img[x + 1][y]
                rescaled[i][j] += (1 - dx) * dy * img[x][y + 1] + dx * dy * img[x + 1][y + 1]
    elif interpolation == 'Bicubic':
        for i in range (1, rescaled.shape[0] - 5):
            for j in range (1, rescaled.shape[1] - 5):
                x = float(i) / scale_factor
                y = float(j) / scale_factor
                dx = x - math.floor(x)
                dy = y - math.floor(y)
                x = math.floor(x)
                y = math.floor(y)
                acc = 0
                for m in range(-1, 3):
                    for n in range (-1, 3):
                        acc += img[x + m][y + n] * R(m - dx) * R(dy - n)
                rescaled[i][j] = acc


    elif interpolation == 'Lagrange':
        for i in range (1, rescaled.shape[0] - 4):
            for j in range (1, rescaled.shape[1] - 4):
                x = float(i) / scale_factor
                y = float(j) / scale_factor
                dx = x - math.floor(x)
                dy = y - math.floor(y)
                x = math.floor(x)
                y = math.floor(y)
                L1 = L(1, x, y, dx, dy, img)
                L2 = L(2, x, y, dx, dy, img)
                L3 = L(3, x, y, dx, dy, img)
                L4 = L(4, x, y, dx, dy, img)
                acc = - dy * (dy - 1) * (dy - 2) * L1/6.0
                acc += (dy + 1) * (dy - 1) * (dy - 2) * L2/2.0
                acc += -dy * (dy + 1) * (dy - 2) * L3/2.0
                acc += dy * (dy + 1) * (dy - 1) * L4 / 6.0
                rescaled[i][j] = acc
        
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
