'''
Script to convert from mm-flux intensity to column density
'''

import numpy as np

def beam_area(bmaj, bmin):
    bmaj_rad = bmaj / ((180/np.pi)*3600)
    bmin_rad = bmin / ((180/np.pi)*3600)
    area_arcsec2 = 1.442*(np.pi/4)*bmaj*bmin 
    area_sterr = 1.442*(np.pi/4)*bmaj_rad*bmin_rad 
    result_dict = {'arcsec2':area_arcsec2, 'sterr':area_sterr}
    return result_dict

def dust_column(flux, area, nu, Tdust=20, kappa=1.0, nu_kappa=230e9, beta=1.8):
    '''
    [flux] = mJy
    [area] = sterr
    [nu] = Hz
    [Tdust] = K
    [kappa] = cm^2 g^-1
    '''
    # Useful constants: 
    h = 6.6260755e-27 #cgs 
    c = 2.99792458e10
    k = 1.380658e-16
    #Calculate kappa at the relevant frequency: 
    kappa_nu = kappa*(nu/nu_kappa)**beta
    dust_intensity = (2*h*nu**3/c**2)*(np.exp((h*nu)/(k*Tdust))-1)**-1
    #
    print('Calculating tau and Sigma with full Planck function:')
    avg_intensity = (flux*1e-3*1e-23)/area
    tau_planck = avg_intensity/dust_intensity
    print('tau_planck is: {}'.format(tau_planck))
    sigma_planck = tau_planck/kappa_nu
    #
    print('Calculating tau and Sigma under Rayleigh-Jeans approximation:') 
    Tb = (avg_intensity*c**2)/(2*k*nu**2)
    tau_RJ = Tb/Tdust
    print('tau_RJ is: {}'.format(tau_RJ))
    sigma_RJ = tau_RJ/kappa_nu
    result_dict = {'planck':sigma_planck, 'rj':sigma_RJ}
    return result_dict   