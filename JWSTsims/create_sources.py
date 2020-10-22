# Functions that create model stellar sources
# Created by Roberto G-M, 19.10.2020

def binary(br=1., Dec_offset=0.1, RA_offset=0.1,imsize=[3.,3.],pixscale=0.015):
    '''
    Creates binary source. Valid keywords are 'br' (source relative brightness, float),
    'Dec_offset' and 'RA_offset' (offset in arcsec, float), 'imsize' (image size in arcsec,
    Dec_size, RA_size), 'pixscale'  (pixel scale in arcsec/pix).
    '''
    imnpix_y = round(imsize[0]/pixscale)
    imnpix_x = round(imsize[1]/pixscale)
    sources = {'Primary':{'Brightness':1.,'Dec':round(imnpix_y/2),'RA':round(imnpix_x/2)}}
    sources.update({'Secondary':{'Brightness':br,'Dec':round(imnpix_y/2)+\
    round(Dec_offset/pixscale),'RA':round(imnpix_x/2)-round(RA_offset/pixscale)}})
    print(sources)
    return sources

def multiple(br=[1.], Dec_offset=[0], RA_offset=[0],imsize=[3.,3.],pixscale=0.015):
    '''
    Creates miltiple source. Valid keywords are 'br' (source relative brightness, list of
    floats),'Dec_offset' and 'RA_offset' (offset in arcsec, list of floats), 'imsize'
    (image size in arcsec, Dec_size, RA_size), 'pixscale'  (pixel scale in arcsec/pix).
    '''
    imnpix_y = round(imsize[0]/pixscale)
    imnpix_x = round(imsize[1]/pixscale)
    sources = {}
    print(br)
    for source in range(len(br)):
        sources.update({'Source{}'.format(source):{'Brightness':br[source],\
        'Dec':round(imnpix_y/2)+round(Dec_offset[source]/pixscale),\
        'RA':round(imnpix_x/2)+round(RA_offset[source]/pixscale)}})
    print(sources)
    return sources
