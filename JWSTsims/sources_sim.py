# Script that creates sources and looks at it using JWST PSF's
# Run in webbpsf-env to avoid conflicts
# Las modified Roberto G-M 21.10.2020

from astropy.io import fits
import numpy as np
from astropy.convolution import convolve, convolve_fft
from astropy.convolution import CustomKernel
from reproject import reproject_interp
from astropy import wcs
import webbpsf
import matplotlib.pyplot as plt
import create_sources
import random
import sys
sys.path.append("/home/roberto/myscisoft/imf/imf")
import imf


# Read in JWST PSF created with webbpsf package
psf_file = 'F200W_psf.fits'
hdu_psf = fits.open(psf_file)
psf_header = hdu_psf[0].header
psf_data = hdu_psf[0].data
hdu_psf.close()
pixscale = psf_header['PIXELSCL'] #arcsec
psf_fov = psf_header['FOV'] # = pix_scale*npix, arcsec

'''
# If regridding is necessary
ww = wcs.WCS(psf_header)
hdu3 = fits.PrimaryHDU(data=new_psf, header=psf_header)
hdu3.writeto('F200W_psf_regr.fits', overwrite=True)
'''

# Create empty image
imsize = [60.0,60.0] # arcsec
imnpix_y = round(imsize[0]/pixscale)
imnpix_x = round(imsize[1]/pixscale)
data = np.zeros((imnpix_y,imnpix_x),dtype=np.float64)

# Create sources:
# Binary example
#sources = create_sources.binary(br=0.5,Dec_offset=0.3,RA_offset=0.1,imsize=imsize,pixscale=pixscale)

# Cluster example
br_arr = imf.make_cluster(10000) #Mass of cluster in Msun
nstars = br_arr.shape[0]
dec_arr = np.random.uniform(-29,29,nstars)
ra_arr = np.random.uniform(-29,29,nstars)
sources = create_sources.cluster(br=br_arr,Dec_offset=dec_arr,\
RA_offset=ra_arr,imsize=imsize,pixscale=pixscale)


# Example with a few sources
#sources = create_sources.multiple(br=[1.0,0.5,0.3,0.1],Dec_offset=[0.1,-0.2,0.3,-0.4],\
#RA_offset=[0.1,-0.3,0.35,0.5],imsize=imsize,pixscale=pixscale)


# Fill in point sources
for source in sources:
    data[sources[source]['Dec'],sources[source]['RA']] = sources[source]['Brightness']

# Write model image with point sources to fits
fits.writeto('model.fits',data,overwrite=True)


# Create custom convolution Kernel from PSF
try:
    psf_kern = CustomKernel(psf_data)
except:
    print('Adding dummy row and column to psf data for CustomKernel to work.')
    psfnpix_y = psf_data.shape[0]+1
    psfnpix_x = psf_data.shape[1]+1
    new_psf = np.zeros((psfnpix_y,psfnpix_x),dtype=np.float64)
    new_psf[:psfnpix_y-1,:psfnpix_x-1] = psf_data
    #hdu_new_psf = fits.PrimaryHDU(new_psf)
    psf_header['NAXIS1'] = psfnpix_y
    psf_header['NAXIS2'] = psfnpix_x
    fits.writeto('new_psf.fits',new_psf,psf_header,overwrite=True)
    psf_kern = CustomKernel(new_psf)

#Convolve model image with PSF and save FITS file
convl_image = convolve_fft(data,psf_kern, allow_huge=True)
im_head = psf_header
im_head['NAXIS1'] = convl_image.shape[0]
im_head['NAXIS2'] = convl_image.shape[1]
fits.writeto('convl_model.fits',convl_image,im_head,overwrite=True)

#Display on screen and save png
webbpsf.display_psf('convl_model.fits')
plt.savefig('convl_model.png')
plt.show()
