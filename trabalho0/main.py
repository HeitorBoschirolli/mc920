#!/usr/bin/env python2

import numpy as np
import skimage.io
import skimage.util
import skimage.exposure
import matplotlib.pyplot as plt
import os

# o nome da imagem deve ser o caminho (relativo ou absoluto) dela
img_name = raw_input('Enter the image name: ')
img = skimage.io.imread(img_name)

# remove a extensao do nome da imagem
img_name = os.path.splitext(img_name)[0]

# plota o histograma dos niveis de cinza da imagem
flat_img = img.ravel()
bins = np.arange(1, 256) # all possible intensity levels
plt.hist(flat_img, bins=bins)
plt.ylabel('Number of pixels')
plt.xlabel('Gray level')
plt.title('image gray level histogram')
plt.savefig(img_name + '_histogram.png')

# exibe algumas estatisticas da imagem
print 'image height:', img.shape[0]
print 'image width:', img.shape[1]
print 'minimum intensity:', np.min(img)
print 'maximum intensity:', np.max(img)
print 'average intensity:', np.mean(img)

# exibe o negativo da imagem original
plt.subplot(1, 2, 1)
inverted = skimage.util.invert(img)
skimage.io.imsave(img_name + '_inverted.png', inverted)

# exibe a imagem original com o intervalo de intensidades igual a [120, 180]
plt.subplot(1, 2, 2)
intensity_rescaled = skimage.exposure.rescale_intensity(img, (0, 255),
                                                        (120, 180))
skimage.io.imsave(img_name + '_rescaled.png', intensity_rescaled)