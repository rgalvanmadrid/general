# Script that finds sources using Atropy Photutils
# Most of this script has been grabbed from the documentation of
# Photutils without much thinking. 

import numpy as np
from photutils import DAOStarFinder
from astropy.stats import mad_std
from astropy.io import fits
from photutils import aperture_photometry, CircularAperture
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm, PowerNorm


input_im = 'convl_model.fits'
hdu_input = fits.open(input_im)
input_header = hdu_input[0].header
input_data = hdu_input[0].data
hdu_input.close()

bkg_sigma = mad_std(input_data)
daofind = DAOStarFinder(fwhm=10., threshold=1e2*bkg_sigma)
sources = daofind(input_data)

for col in sources.colnames:
    sources[col].info.format = '%.8g'
print(sources)


positions = np.transpose((sources['xcentroid'], sources['ycentroid']))
apertures = CircularAperture(positions, r=10.)
phot_table = aperture_photometry(input_data, apertures)
for col in phot_table.colnames:
    phot_table[col].info.format = '%.8g'  # for consistent table output
print(phot_table)


plt.imshow(input_data, cmap='gray_r', origin='lower',\
norm=PowerNorm(vmin=input_data.min(), vmax=input_data.max(),gamma=0.333))
plt.colorbar()
apertures.plot(color='blue', lw=1.5, alpha=0.5)
plt.show()
