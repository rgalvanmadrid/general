#### Script to convert Jy/beam to K and Viceversa
### User defined parameters of unt conversion ###
#test 1.0 Jy/beam are 101.001022909 K
#nu = 220.0e9 [Hz]
#S=1.0  [Jy]
#a=0.5/2 #semiaxes [arcsec], bmaj = 0.5 
#b=0.5/2 #semiaxes [arcsec], bmin = 0.5
#end test
import math
def conversion(nu, bmaj, bmin):
	S=1.0
	c = 2.99792458e10
	kB = 1.380658e-16
	JYcgs = 1e-23
	arcsec2rad = 1.0/((180/math.pi)*3600.0)
	TBperJy = (c**2.0/(2*kB*nu**2.0))*(math.log(2.0))*((S*JYcgs)/(math.pi*(bmaj/2.)*(bmin/2.)*arcsec2rad**2.0))
	JyperTB = 1.0/TBperJy
	print(str(S)+' Jy/beam are '+str(TBperJy)+' K')
	print(str(S)+' K are '+str(JyperTB)+' Jy/beam')
	print('See output dictionary')
	return {'KperJy':TBperJy, 'JyperK':JyperTB}

