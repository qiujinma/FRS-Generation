#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 13:59:47 2026

@author: maqiujin
"""
# Conduct modal combination
# modal_sa: modal FRS for (wo,xo)
# contri: modal contribution
def main_modal_combination(Q, wo, xo, w_p1, x_p1, modal_sa, contri, dofs, alpha_g, alpha_l):
    import numpy as np
    # calculate corrlation coefficients between modal FRS
    from frs_generation.lamda_matrix import lamda_matrix     # Function for correlation coefficents between multiple modes
    
    LAMDA=lamda_matrix(Q,wo,xo,w_p1,x_p1)   # Calculate spectral momemnts using Eqns (18), (19) and (20)
    cqc_para_res=np.eye(Q)
    for ss in range(Q):
        for jj in range(Q):
            if ss!=jj:
                cqc_para_res[ss][jj]=(np.real(LAMDA[ss][jj])/np.sqrt(LAMDA[ss][ss]*LAMDA[jj][jj]))
    frs=[]            
    for dof in dofs:
        #CQC-FRS: 
            #sa_cqcm - Eqn (33): CQC-FRS for modal FRS; 
            #sa_cqcg and sa_cqcl - for Eqn (30): CQC-FRS for modal periodic components computed by modified Gupta and modified Lindley-Yow, respectively
        sa_cqcg=0
        sa_cqcl=0
        sa_cqcm=0
        for jj in range(Q):
            for kk in range(Q):      
                sa_cqcg=sa_cqcg+contri[dof][jj]*modal_sa[jj]*contri[dof][kk]*modal_sa[kk]*cqc_para_res[jj][kk]*np.sqrt(1-alpha_g[jj]**2)*np.sqrt(1-alpha_g[kk]**2)
                
                sa_cqcl=sa_cqcl+contri[dof][jj]*modal_sa[jj]*contri[dof][kk]*modal_sa[kk]*cqc_para_res[jj][kk]*np.sqrt(1-alpha_l[jj]**2)*np.sqrt(1-alpha_l[kk]**2)
                
                sa_cqcm=sa_cqcm+contri[dof][jj]*modal_sa[jj]*contri[dof][kk]*modal_sa[kk]*cqc_para_res[jj][kk]
                
        sa_cqc_frs=np.sqrt(sa_cqcm)

        # rigid modes combination - Eqn (31): sa_g and sa_l for modal rigid components combination by modified Gupta and modified Lindley-Yow, respectively
        sa_g=0
        sa_l=0
        for jj in range(Q):
            
            sa_g=sa_g+alpha_g[jj]*modal_sa[jj]*contri[dof][jj]
            sa_l=sa_l+alpha_l[jj]*modal_sa[jj]*contri[dof][jj]
        
        #SRSS combination for periodic and rigid responses - Eqn (32)
        sa_g_r=np.sqrt(sa_cqcg+sa_g**2)
        sa_l_r=np.sqrt(sa_cqcl+sa_l**2)
        
        #Final FRS: taken as the maximum value of the two combinations - Eqn (34)
        sa_rcqc_frs=max(sa_cqc_frs,sa_g_r,sa_l_r) 
        frs.append(sa_rcqc_frs)
    return frs