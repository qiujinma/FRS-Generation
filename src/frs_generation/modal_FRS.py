#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: maqiujin
"""

# Modal properties of the supporting structure: 
    # modal frequency (rad/s) and modal damping ratio: w1 and x1;
    # frequency of interest for FRS generation:  fo in Hz

# Parameters used for modal rigid response coefficents calculation: 
    #fr - zero period frequency of the target response spectrum
    #F1_s and F1_p used in Eqn (23) for NSC and the modal equivalent SDOF, respectively.
    # PGA_m can be calculated from either of the two ways: 
            #(a) peak ground acceelration from mean spectrum of the selected ground motions; 
            #(b) the zero period acceleratioj from the target response spectrum.
    
        
def modal_FRS(xo, wo, w1, x1, dis_p, v_p, a_p, dis_s, v_s, a_s, PGA_m, F1_s, f1_p, fr): 
    import numpy as np
    from frs_generation.coef_matrix_modal_FRS import coef_matrix
    from frs_generation.gupta_rigid import gupta_rigid
    from frs_generation.lindley_rigid import lindley_rigid
    
    # spectral displacements and velocities for the NSC (dis_s, v_s) 
    RS=np.zeros(4)
    RS[0]=v_s
    RS[1]=dis_s
    
    #extract modal frequency w1 and damping ratio x1 for mode j
    f_p=w1/(2*np.pi)      #modal frequency in Hz   
    fo=wo/(2*np.pi)
    # spectral displacements and velocities for the modal equivalent SDOF (dis_p,v_p)
    RS[2]=v_p
    RS[3]=dis_p

    #calculate modal contribution to NSC's response: |S_n (t)|max
    if wo/w1==1 and xo/x1>=0.98 and xo/x1<=1.02:
        #perfect tuning cases with Eqn (7.2)
        #print('perfect tuning')
        # Parameters in Eqn (7.2)
        A3a=(1-8*xo**2+8*xo**4)/wo
        A4a=(-3*xo+4*xo**3)
        AA=[A3a,A4a]
        
        #|S_n (t)|_(max,ω_0=ω_1 )
        sa_srss=0
        for jj in range(2):
            aa_s=(AA[jj]*RS[jj])**2*2
            sa_srss=aa_s+sa_srss
        sa=np.sqrt(sa_srss)*wo**2/(4*xo*(1-xo**2))
        
        #calculate rigid response coefficient for modal FRS
        #Rigid response coefficient by Gupta (Eqn (23))
        a_gup=gupta_rigid(f_p,F1_s,fr)
        
        #Rigid response coefficient by Lindely-Yow (Eqn(24))
        a_lind=lindley_rigid(PGA_m,a_p)
        
    else:
        # Non-perfect resonance cases
        #Calculate coefficent matrix based on Eqn (9)
        cqc_para=coef_matrix(1,wo,xo,w1,x1)
    
        #Parameetrs in Eqns (7.1) and (8)
        denom=(wo**2-w1**2)**2-4*wo*w1*xo*x1*(wo**2+w1**2)+4*wo**2*w1**2*(xo**2+x1**2)
        A1=-4*wo*w1*(w1**3*xo-4*w1**2*wo*x1*xo**2+4*w1*wo**2*x1**2*xo-wo**3*x1)/(2*denom)
        A2=-2*w1**2*wo**2*(w1**2-4*xo*w1*wo*x1+4*wo**2*x1**2-wo**2)/(2*denom)
        B1=4*wo*w1*(w1**3*xo-4*w1**2*wo*x1*xo**2+4*w1*wo**2*x1**2*xo-wo**3*x1)/(2*denom)
        B2=-2*w1**2*wo**2*(4*w1**2*xo**2-w1**2-4*x1*w1*wo*xo+wo**2)/(2*denom)
        A=[A1,A2,B1,B2]
        
        #|Sn(t)|max
        sa_cqcr=0
        for jj in range(4):
            
            for kk in range(4):           
                aar=A[jj]*RS[jj]*A[kk]*RS[kk]*cqc_para[jj][kk]
                sa_cqcr=aar+sa_cqcr
               
        sa=np.sqrt(sa_cqcr)
        
        #Calculate modified rigid response coefficent for modal FRS
        #Original Rigid response coefficient by Gupta (Eqn (23))
        a_gup1=gupta_rigid(f_p,f1_p,fr)   # for mode j
        a_gupo=gupta_rigid(fo,F1_s,fr)       # for NSC
        # Modified rigid response coefficient for modal FRS based on Eqn (25)
        a_gup=np.sqrt((A1*RS[0]*a_gupo+A2*RS[1]*a_gupo+B1*RS[2]*a_gup1+B2*RS[3]*a_gup1)**2/sa_cqcr)
        if a_gup>1:
            a_gup=1
            
        #Original Rigid response coefficient by Lindely-Yow (Eqn(24))
        a_lind1=lindley_rigid(PGA_m,a_p)    # for mode j
        a_lindo=lindley_rigid(PGA_m,a_s)  # for NSC
        # Modified rigid response coefficient for modal FRS based on Eqn (25)
        a_lind=np.sqrt((A1*RS[0]*a_lindo+A2*RS[1]*a_lindo+B1*RS[2]*a_lind1+B2*RS[3]*a_lind1)**2/sa_cqcr)
        if a_lind>1:
            a_lind=1
        
    return sa, a_gup, a_lind
    
    