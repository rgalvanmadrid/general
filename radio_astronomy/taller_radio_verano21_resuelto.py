'''
Taller de radioastronomía e imágenes. Escuela de Verano 2021 #
Autor: Roberto Galván Madrid
Estudiante:
'''

# Se importan las librerías necesarias para hacer el programa
import numpy as np
import matplotlib.pyplot as plt

from skimage import io, draw
from skimage.transform import resize

from astropy.convolution.kernels import CustomKernel
from astropy.convolution import convolve, convolve_fft

import random

'''
Paso 0
Determinar el tamaño del dominio 2D que se usará.
'''
dom_size = 501 # Tamaño del dominio, de preferencia un entero impar.
 # Dominio 2D de la apertura.
apert = np.zeros([dom_size,dom_size])
amp = 1. # Normalización de la iluminación en la apertura.


'''
Paso 1:
Crear una apertura circular con iluminación constante.
'''
apert_rad = 10 # Radio de la apertura circular.
apert_ctr = [apert.shape[0]/2,apert.shape[0]/2] # Centro de la apertura circular.
xx, yy = draw.circle(apert_ctr[0], apert_ctr[1], apert_rad)  # Crear la apertura circular.
apert[xx,yy] = amp

'''
Paso 2:
Crear el patrón de respuesta del haz del telescopio (Point Spread Function, PSF)
'''
E_field = np.fft.fftshift(np.fft.fft2(apert, norm='ortho')) #Campo eléctrico en el cielo.
beam = np.abs(np.square(E_field)) #El haz, beam, o PSF, es el módulo del campo eléctrico en el cielo.
beam = beam/beam.max() #Normalizar el beam para que el pico sea 1
print('Tamaño de la matriz del beam: {}'.format(beam.shape))

'''
Paso 3:
Convolucionar la imagen modelo con el PSF, para obtener la imagen vista por el instrumento
'''
# Leer imagen modelo
image = io.imread('PDS70c.jpg',as_gray=True)  #Cargar como escala de grises, no como RGB
image = resize(image, (image.shape[0] // 2, image.shape[1] // 2),anti_aliasing=True)
print('Tamaño de la matriz de la imagen: {}'.format(image.shape))

#Límites para truncar el kernel de convolución
zoom = 1 # zoom factor to truncate and display kernel
kern_min = int((dom_size-1)/2-(dom_size-1)/(2*zoom))
kern_max = int((dom_size-1)/2+(dom_size-1)/(2*zoom))

kernel = CustomKernel(beam[kern_min:kern_max+1,kern_min:kern_max+1])
print('Tamaño de la matriz del kernel de convolución: {}'.format(kernel.shape))


#Ejecutar la convolución:
#im_conv = convolve(image, kernel)
im_conv = convolve_fft(image, kernel)

'''
Paso 4:
Crear, desplegar y guardar las figuras.
'''

fig = plt.figure(figsize=(10, 10))
ax1 = plt.subplot(2, 2, 1)
ax2 = plt.subplot(2, 2, 2)
ax3 = plt.subplot(2, 2, 3)
ax4 = plt.subplot(2, 2, 4)


ax1.imshow(apert, cmap='Oranges')
#ax1.set_axis_off()
ax1.set_title('Iluminación de la apertura del telescopio')


ax2.imshow(np.log(beam[kern_min:kern_max,kern_min:kern_max]))
#ax2.set_axis_off()
ax2.set_title('Haz del telescopio en el cielo (PSF)')

ax3.imshow(np.sqrt(image), cmap='Oranges')
ax3.set_title('Imagen modelo')

ax4.imshow(np.sqrt(im_conv), cmap='Oranges')
ax4.set_title('Imagen modelo convolucionada con el PSF')


# Show and save plots
plt.tight_layout()
#plt.savefig('taller_radio_apert{}.png'.format(apert_rad), dpi=300)
plt.show()
