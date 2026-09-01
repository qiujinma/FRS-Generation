#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 15:08:53 2026

@author: maqiujin
"""
# Structural properties: 
    #modal frequencies (rad/s): w_p
    #modal damping ratio: x_p
    #mode shape: phi (no_of_dofs x no_of_modes)
    #mode participation factors in the direction of input motions: partis
    #Rayleigh damoing coefficeint: al

# Input spectrum: Sa(m/s^2), Sv(m/s), Sd(m) 
    #Frequency range (Hz):  RS_frequency  
    #Damping ratio range: xis
    #Rigid frequency (Hz): fr
    #PGA (m/s^2)
    
# Damping level of FRS: xo

def main_FRS(dofs, w_p, x_p, phi, partis, al, fr, PGA, Sa, Sv, Sd, RS_frequency, xis, xo):
    import numpy as np
    
    #Determine the number of modes to be included for FRS calculation - Q: 
        #Q=M+1: find the number of modes (M) with frequency (Hz) lower than fr, and the M+1 th mode has the corresponding frequency of fr
        # if all modal frequencies ar elower than fr, all modes need to be considered
    flag=0
    for i in range(len(w_p)):
        if i>=1:
            if w_p[i]/(2*np.pi)>=fr and w_p[i-1]/(2*np.pi)<fr:
                Q=i+1      # the total number of modes = M+1
                flag=1
        # if all modal frequencies < fr
    contri={}   # modal contribution calculation for each dof of interest
    if flag==0:
        Q=len(w_p)
        #original modal properties used for FRS calculation
        w_p1=w_p
        x_p1=x_p
        # calculate modal contributions
        for dof in dofs:
            contri[dof]=[]
            for i in range (Q):
                contri[dof].append(phi[dof-1][i]*partis[i])
            
    elif flag==1:
        #update modal properties used for FRS calculation
        w_p1=np.zeros(Q)
        x_p1=np.zeros(Q)
        for i in range(Q):
            if i==Q-1:
                wr=2*fr*np.pi
                w_p1[i]=wr
                x_p1[i]=0.5*(al[0]/wr+al[1]*wr)
            else:
                w_p1[i]=w_p[i]
                x_p1[i]=x_p[i]  
        for dof in dofs:
            contri[dof]=[]
            sum_mm=0
            for i in range(Q):
                if i==Q-1:   # for the missing mass modes, the modal contribution is computed using Eqn (29) in Ma and Kwon (2026)
                    contri[dof].append(1-sum_mm)    #here the influence value is taken as 1 since the DOF of interst is assumed  to be in the direction of the input motion
                else:
                    contri[dof].append(phi[dof-1][i]*partis[i])
                    sum_mm=sum_mm+phi[dof-1][i]*partis[i]
                
    
    #Extract spectral values and the F1 for rigid coefficent calculation (23), for the Q modes and the NSC
    from frs_generation.spectral_values_FRS import spectral_values
    F1_s, ra_s, rv_s, rd_s, F1_p, ra_p, rv_p, rd_p=spectral_values(x_p1, w_p1, xis, xo, Sa, Sv, Sd, RS_frequency)
    
    from frs_generation.main_modal_FRS import main_modal_FRS   #Function for modal FRS calculation
    from frs_generation.main_modal_combination import main_modal_combination  #Function for modal combination
    
    FRS={}
    for dof in dofs:
        FRS[dof]=[]
    for ii in range(len(RS_frequency)):
        #calculate FRS for each frequency of interest
        fo=RS_frequency[ii]
        wo = 2*np.pi*fo 
                
        #Modal FRS execution for NSC (wo,xo) mounted on a modal equivalent SDOF structure (wn, xn) for Q modes
        modal_sa, alpha_g, alpha_l = main_modal_FRS(Q, ii, xo, wo, w_p1, x_p1, rd_p, rv_p, ra_p, rd_s, ra_s, rv_s, PGA, F1_s, F1_p, fr, RS_frequency)
        
        #modal FRS combination for each dof of interest
        frs=main_modal_combination(Q, wo, xo, w_p1, x_p1, modal_sa, contri, dofs, alpha_g, alpha_l)
        for jj in range(len(dofs)):
            FRS[dofs[jj]].append(frs[jj])
    
    FRS_value={}
    for dof in dofs:
        FRS_value[dof]=[]
        frs_array = [np.asarray(x).ravel()[0] for x in FRS[dof]]
        for x in frs_array:
            FRS_value[dof].append(float(x)/9.81)
    
    # Peak broadening ot evaluated FRS
    broadened_FRS={}
    for dof in dofs:
        broadened_FRS[dof]=[]
        # Find local maximum at modal frequencies
        sam5=[]
        for mode in range(Q):
            rs5=[]
            for j in range(len(RS_frequency)):
                w=RS_frequency[j]*2*np.pi
                if 0.85*w_p1[mode]<=w<=1.15*w_p1[mode]:
                    rs5.append(FRS_value[dof][j])
                    
            sam5.append(max(rs5))
            
        #apply peak Broadening
        for jj in range(len(RS_frequency)):
            flag=0
            w=RS_frequency[jj]*2*np.pi
            for mode in range(Q):
                if 0.85*w_p1[mode]<=w<=1.15*w_p1[mode]:
                    flag=1
                    broadened_FRS[dof].append(sam5[mode])
                    break
            if flag==0:
                broadened_FRS[dof].append(FRS_value[dof][jj])
    return FRS_value, broadened_FRS