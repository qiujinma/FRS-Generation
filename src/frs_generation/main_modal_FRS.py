#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 11:18:57 2026

@author: maqiujin
"""
#Calculate modal contribution to NSC's response at (wo,xo)
#Q: total number of modes considered

def main_modal_FRS(Q, ii, xo, wo, w_p1, x_p1, rd_p, rv_p, ra_p, GRSD_s, GRSA_s, GRSV_s, PGA, F1_s, F1_p, fr, RS_frequency):
    import numpy as np
    from frs_generation.modal_FRS import modal_FRS       #Function for modal FRS calculation
    
    #Modal FRS execution for NSC (wo,xo) mounted on a modal equivalent SDOF structure (wn, xn)
    modal_sa=[]
    # rigid response coefficients for modal FRS
    alpha_g=np.zeros((Q,1))
    alpha_l=np.zeros((Q,1))
    for j in range(Q):
        # Extract modal frequency and damping ratio
        wn=w_p1[j]
        xn=x_p1[j]
        fn=wn/(2*np.pi)
        
        #interpolate to find the spectral displacement and the velocity based 
        #on the provided GRS at modal frequencies of the supporting structure 
        sd_s=np.interp(fn,RS_frequency, GRSD_s)
        sv_s=np.interp(fn,RS_frequency, GRSV_s)
        sa_s=np.interp(fn,RS_frequency, GRSA_s)
                
        #calculate the local max for modal FRS at (wn,xo)
        sa_m, a_gupm, a_lindm = modal_FRS(xo, wn, wn, xn, rd_p[j], rv_p[j], ra_p[j], sd_s, sv_s, sa_s, PGA, F1_s, F1_p[j], fr)
        #calculate the modal FRS at (wo,xo)
        sa, a_gup, a_lind = modal_FRS(xo, wo, wn, xn, rd_p[j], rv_p[j], ra_p[j], GRSD_s[ii], GRSV_s[ii], GRSA_s[ii], PGA, F1_s, F1_p[j], fr)
        alpha_g[j]=a_gup
        alpha_l[j]=a_lind
        
        #check if modal FRS values exceed local maximum based on Eqn (7)
        if wo/wn>0.5 and wo/wn<2:
            if sa>sa_m:
                sa=sa_m
        modal_sa.append(sa)      
                
    return modal_sa, alpha_g, alpha_l
        
        


