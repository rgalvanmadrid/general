# Script that uses WebbPSF to create PSF to use in simulations
# Needs to run in webbpsf-env to avoid conflicts

import stpsf
import matplotlib.pyplot as plt

filter = 'F200W'

nc = stpsf.NIRCam()
nc.filter = filter
psf = nc.calc_psf(outfile='{}_psf.fits'.format(filter),oversample=2,fov_arcsec=5.0)
stpsf.display_psf(psf)
plt.show()
