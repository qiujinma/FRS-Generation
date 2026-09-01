# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 14:23:49 2026

@author: Qiujin
"""

def read_modal_prop(modal_prop_file, mode_shape_file,al):
    import numpy as np
    # read modal properties
    
    modal = open(modal_prop_file).readlines()
    
    w_p=[]     # Modal frequency (rad/s)
    partis=[]  # Modal participation factor
    x_p=[]     # Modal damping ratio
    for j in range(2,len(modal)):
        values=modal[j].split(',')
        w_p.append(float(values[1])*2*np.pi)
        partis.append(float(values[2]))
    
    # calculate modal damping ratio based on rayleigh damping coefficients al
    for mode in range(len(w_p)):
        x_p.append(al[0]/(2*w_p[mode])+al[1]*w_p[mode]/2) 

    # read mode shapes
    
    mode_shape=open(mode_shape_file).readlines()
    phi=[]     # Mode shapes
    for j in range(1,len(mode_shape)):
        
        values=mode_shape[j].split(',')
        v1=[]
        for jj in range(len(values)):
            v1.append(values[jj])
        phi.append(v1)
    phi=np.asarray(phi, dtype=float)
    phi=phi.reshape(len(mode_shape)-1,-1)
    
    return w_p, partis, x_p, phi
    
    
        
    
        