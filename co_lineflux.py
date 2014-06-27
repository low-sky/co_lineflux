#!/usr/bin/env python
import sys
import numpy as np
import os
from astropy import units as u
import pyradex


def Intensity_12CO(NCo,nH2,T_kin,del_v):
    """ This function accepts CO column density, H2 density, kinetic temperature of the gas, and line width. 
    Assumed even proportions of ortho/para H2 for collider densities, background temp of 2.73K, and abundance of 10^{-4}*H2
    Units as follows:
    [log(NCo)] = cm^-2
    [log(nH2)] = cm^-3
    [log(T)] = K
    [del_v] = km/s
    
    Returns a dictionary of integrated intensity values for each line of CO (first 10 lines only)
    """
    
#   import os
#   if not os.path.exists('co.dat'):
#      import urllib
#      urllib.urlretrieve('http://home.strw.leidenuniv.nl/~moldata/datafiles/co.dat')
        
    #define input parameters
    ph2_dens = np.power(10,nH2)/2
    oh2_dens = np.power(10,nH2)/2
    abundance = 1.0E-4
    temperature = np.power(10,T_kin)
    column = np.power(10,NCo)
    tbackground = 2.73
    
    # Run Radex code, get table of parameters
    R = pyradex.Radex(species='/Users/ksgreen/Radex/data/co', collider_densities={'ph2':ph2_dens,'oh2':oh2_dens}, 
    R = pyradex.Radex(species='co', collider_densities={'ph2':ph2_dens,'oh2':oh2_dens}, 
                      column=column, abundance=abundance, tbackground=tbackground, deltav=del_v, 
                      temperature=temperature)
    
    R.run_radex()
    table = R.get_table()
    
    #Grab frequency and brightness values from table, create dictionary
    frequency = table['frequency']
    brightness = table['brightness']
    line_names = ['one_zero','two_one','three_two','four_three','five_four','six_five','seven_six','eight_seven',
                  'nine_eight','ten_nine']
 
    intensity = dict(zip(line_names,brightness[0:10]))
    return intensity
    
