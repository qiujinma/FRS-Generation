# -*- coding: utf-8 -*-
"""
Created on Mon Jul 14 12:50:42 2025

@author: Qiujin
"""
#calculate spectral momements based Eqns (18), (19), and (20)
#supporting structure: modal frequencies - w_p (rad/s), modal damping ratios - x_p
#dof: number of modes considered.
#properties of NSC: (wo, xo)
def lamda_matrix(dof,wo,xo,w_p,x_p):
    import numpy as np
    wod=wo*np.sqrt(1-xo**2)
    lamda=np.zeros((dof,dof), dtype=float)
    for k in range(dof):
        wk=w_p[k]
        xk=x_p[k]

        for j in range(dof):
            wj=w_p[j]
            xj=x_p[j]
            
            denom_oj=(wo**2-wj**2)**2-4*wo*wj*xo*xj*(wo**2+wj**2)+4*wo**2*wj**2*(xo**2+xj**2)
            denom_ok=(wo**2-wk**2)**2-4*wo*wk*xo*xk*(wo**2+wk**2)+4*wo**2*wk**2*(xo**2+xk**2)
            de1_oj=(wo**2-wj**2)**2+4*wo*wj*xo*xj*(wo**2+wj**2)+4*wo**2*wj**2*(xo**2+xj**2)
            de1_ko=(wk**2-wo**2)**2+4*wk*wo*xk*xo*(wk**2+wo**2)+4*wk**2*wo**2*(xk**2+xo**2)
            de1_kj=(wk**2-wj**2)**2+4*wk*wj*xk*xj*(wk**2+wj**2)+4*wk**2*wj**2*(xk**2+xj**2)
            
            
            # spectral moments of the same mode
            if k==j:
                if wo/wk==1 and xo/xk>=0.98 and xo/xk<=1.02:
                    A3a=(1-8*xo**2+8*xo**4)/wo
                    A4a=-3*xo+4*xo**3
                    
                    Ak=np.asarray([A3a, A4a])*np.sqrt(2)*wo**2/(4*(1-xo**2)*xo)
                    Aj=np.asarray([A3a, A4a])*np.sqrt(2)*wo**2/(4*(1-xo**2)*xo)
                    HH3=np.zeros((2,2),dtype=float)
                    HH3[0][0]=np.pi/(4*wo*xo)
                    HH3[1][1]=np.pi/(4*wo**3*xo)
                    l_kj=0
                    for ks in range(2):
                        for js in range(2):
                            l_kj=Ak[ks]*Aj[js]*HH3[ks][js]+l_kj
                    lamda[k][j]=l_kj

                else:
                    A1k=-4*wo*wk*(wk**3*xo-4*wk**2*wo*xk*xo**2+4*wk*wo**2*xk**2*xo-wo**3*xk)/(2*denom_ok)
                    A2k=-2*wk**2*wo**2*(wk**2-4*xo*wk*wo*xk+4*wo**2*xk**2-wo**2)/(2*denom_ok)
                    B1k=4*wo*wk*(wk**3*xo-4*wk**2*wo*xk*xo**2+4*wk*wo**2*xk**2*xo-wo**3*xk)/(2*denom_ok)
                    B2k=-2*wk**2*wo**2*(4*wk**2*xo**2-wk**2-4*xk*wk*wo*xo+wo**2)/(2*denom_ok)
                    Ak=[A1k,A2k,B1k,B2k]
                    
                    A1j=-4*wo*wj*(wj**3*xo-4*wj**2*wo*xj*xo**2+4*wj*wo**2*xj**2*xo-wo**3*xj)/(2*denom_oj)
                    A2j=-2*wj**2*wo**2*(wj**2-4*xo*wj*wo*xj+4*wo**2*xj**2-wo**2)/(2*denom_oj)
                    B1j=4*wo*wj*(wj**3*xo-4*wj**2*wo*xj*xo**2+4*wj*wo**2*xj**2*xo-wo**3*xj)/(2*denom_oj)
                    B2j=-2*wj**2*wo**2*(4*wj**2*xo**2-wj**2-4*xj*wj*wo*xo+wo**2)/(2*denom_oj)
                    Aj=[A1j,A2j,B1j,B2j]
                    
                    HH2=np.zeros((4,4),dtype=float)
                    HH2[0][0]=np.pi/(4*wo*xo)
                    HH2[0][2]=4*np.pi*wo*wj*(wo*xj+wj*xo)/(2*de1_oj)
                    HH2[0][3]=-2*np.pi*(wo**2-wj**2)/(2*de1_oj)
                    HH2[1][1]=np.pi/(4*wo**3*xo)
                    HH2[1][2]=2*np.pi*(wo**2-wj**2)/(2*de1_oj)
                    HH2[1][3]=4*np.pi*(wo*xo+wj*xj)/(2*de1_oj)
                    HH2[2][0]=4*np.pi*wo*wk*(wo*xk+wk*xo)/(2*de1_ko)
                    HH2[2][1]=2*np.pi*(wo**2-wk**2)/(2*de1_ko)
                    HH2[2][2]=4*np.pi*wk*wj*(wk*xj+wj*xk)/(2*de1_kj)
                    HH2[2][3]=-2*np.pi*(wk**2-wj**2)/(2*de1_kj)
                    HH2[3][0]=2*np.pi*(wk**2-wo**2)/(2*de1_ko)
                    HH2[3][1]=4*np.pi*(wk*xk+wo*xo)/(2*de1_ko)
                    
                    HH2[3][2]=2*np.pi*(wk**2-wj**2)/(2*de1_kj)
                    HH2[3][3]=4*np.pi*(wk*xk+wj*xj)/(2*de1_kj)
                    l_kj=0
                    for ks in range(4):
                        for js in range(4):
                            l_kj=l_kj+Ak[ks]*Aj[js]*HH2[ks][js]
                    lamda[k][j]=l_kj
            # spectral moments between different modes are calculated
            else:
                # for perfect resonance mode k
                if wo/wk==1 and xo/xk>=0.98 and xo/xk<=1.02:
                    A3a=(1-8*xo**2+8*xo**4)/wo
                    A4a=-3*xo+4*xo**3
                    
                    Ak=np.asarray([A3a, A4a])*np.sqrt(2)*wo**2/(4*(1-xo**2)*xo)
                    
                    # for perfect resonance modes k and j
                    if wo/wj==1 and xo/xj>=0.98 and xo/xj<=1.02:
                        A3a=(1-8*xo**2+8*xo**4)/wo
                        A4a=-3*xo+4*xo**3
                        
                        Aj=np.asarray([A3a, A4a])*np.sqrt(2)*wo**2/(4*(1-xo**2)*xo)
                        HH3=np.zeros((2,2),dtype=float)
                        HH3[0][0]=np.pi/(4*wo*xo)
                        HH3[1][1]=np.pi/(4*wo**3*xo)
                        l_kj=0
                        for ks in range(2):
                            for js in range(2):
                                l_kj=Ak[ks]*Aj[js]*HH3[ks][js]+l_kj
                        lamda[k][j]=l_kj
                    # for perfect resonance mode k and non-perfect resonance mode j
                    else:
                        
                        A1j=-4*wo*wj*(wj**3*xo-4*wj**2*wo*xj*xo**2+4*wj*wo**2*xj**2*xo-wo**3*xj)/(2*denom_oj)
                        A2j=-2*wj**2*wo**2*(wj**2-4*xo*wj*wo*xj+4*wo**2*xj**2-wo**2)/(2*denom_oj)
                        B1j=4*wo*wj*(wj**3*xo-4*wj**2*wo*xj*xo**2+4*wj*wo**2*xj**2*xo-wo**3*xj)/(2*denom_oj)
                        B2j=-2*wj**2*wo**2*(4*wj**2*xo**2-wj**2-4*xj*wj*wo*xo+wo**2)/(2*denom_oj)
                        Aj=[A1j,A2j,B1j,B2j]
                        
                        HH1=np.zeros((2,4), dtype=float)
                        HH1[0][0]=np.pi/(4*wo*xo)
                        HH1[0][2]=4*np.pi*wo*wj*(wo*xj+wj*xo)/(2*de1_oj)
                        HH1[0][3]=-2*np.pi*(wo**2-wj**2)/(2*de1_oj)
                        HH1[1][1]=np.pi/(4*wo**3*xo)
                        HH1[1][2]=2*np.pi*(wo**2-wj**2)/(2*de1_oj)
                        HH1[1][3]=4*np.pi*(wo*xo+wj*xj)/(2*de1_oj)
                        l_kj=0
                        for ks in range(2):
                            for js in range(4):
                                l_kj=l_kj+Ak[ks]*Aj[js]*HH1[ks][js]
                        lamda[k][j]=l_kj
                #for non-perfect resonance mode k
                else:
                    A1k=-4*wo*wk*(wk**3*xo-4*wk**2*wo*xk*xo**2+4*wk*wo**2*xk**2*xo-wo**3*xk)/(2*denom_ok)
                    A2k=-2*wk**2*wo**2*(wk**2-4*xo*wk*wo*xk+4*wo**2*xk**2-wo**2)/(2*denom_ok)
                    B1k=4*wo*wk*(wk**3*xo-4*wk**2*wo*xk*xo**2+4*wk*wo**2*xk**2*xo-wo**3*xk)/(2*denom_ok)
                    B2k=-2*wk**2*wo**2*(4*wk**2*xo**2-wk**2-4*xk*wk*wo*xo+wo**2)/(2*denom_ok)
                    Ak=[A1k,A2k,B1k,B2k]
                    # for non-perfect resonance mode k and perfect-resonance mode j
                    if wo/wj==1 and xo/xj>=0.98 and xo/xj<=1.02:
                        A3a=(1-8*xo**2+8*xo**4)/wo
                        A4a=-3*xo+4*xo**3
                        
                        Aj=np.asarray([A3a, A4a])*np.sqrt(2)*wo**2/(4*(1-xo**2)*xo)
                        
                        HH1=np.zeros((2,4), dtype=float)
                        HH1[0][0]=np.pi/(4*wo*xo)
                        HH1[0][2]=4*np.pi*wo*wk*(wo*xk+wk*xo)/(2*de1_ko)
                        HH1[0][3]=-2*np.pi*(wo**2-wk**2)/(2*de1_ko)
                        HH1[1][1]=np.pi/(4*wo**3*xo)
                        HH1[1][2]=2*np.pi*(wo**2-wk**2)/(2*de1_ko)
                        HH1[1][3]=4*np.pi*(wo*xo+wk*xk)/(2*de1_ko)
                        l_kj=0
                        for js in range(2):
                            for ks in range(4):
                                l_kj=l_kj+Aj[js]*Ak[ks]*HH1[js][ks]
                        lamda[k][j]=l_kj
                    
                    #for non-perfect resonance modes k and j
                    else:
                        A1j=-4*wo*wj*(wj**3*xo-4*wj**2*wo*xj*xo**2+4*wj*wo**2*xj**2*xo-wo**3*xj)/(2*denom_oj)
                        A2j=-2*wj**2*wo**2*(wj**2-4*xo*wj*wo*xj+4*wo**2*xj**2-wo**2)/(2*denom_oj)
                        B1j=4*wo*wj*(wj**3*xo-4*wj**2*wo*xj*xo**2+4*wj*wo**2*xj**2*xo-wo**3*xj)/(2*denom_oj)
                        B2j=-2*wj**2*wo**2*(4*wj**2*xo**2-wj**2-4*xj*wj*wo*xo+wo**2)/(2*denom_oj)
                        Aj=[A1j,A2j,B1j,B2j]
                        
                        HH2=np.zeros((4,4),dtype=float)
                        HH2[0][0]=np.pi/(4*wo*xo)
                        HH2[0][2]=4*np.pi*wo*wj*(wo*xj+wj*xo)/(2*de1_oj)
                        HH2[0][3]=-2*np.pi*(wo**2-wj**2)/(2*de1_oj)
                        HH2[1][1]=np.pi/(4*wo**3*xo)
                        HH2[1][2]=2*np.pi*(wo**2-wj**2)/(2*de1_oj)
                        HH2[1][3]=4*np.pi*(wo*xo+wj*xj)/(2*de1_oj)
                        HH2[2][0]=4*np.pi*wo*wk*(wo*xk+wk*xo)/(2*de1_ko)
                        HH2[2][1]=2*np.pi*(wo**2-wk**2)/(2*de1_ko)
                        HH2[2][2]=4*np.pi*wk*wj*(wk*xj+wj*xk)/(2*de1_kj)
                        HH2[2][3]=-2*np.pi*(wk**2-wj**2)/(2*de1_kj)
                        HH2[3][0]=2*np.pi*(wk**2-wo**2)/(2*de1_ko)
                        HH2[3][1]=4*np.pi*(wk*xk+wo*xo)/(2*de1_ko)
                        HH2[3][2]=2*np.pi*(wk**2-wj**2)/(2*de1_kj)
                        HH2[3][3]=4*np.pi*(wk*xk+wj*xj)/(2*de1_kj)
                        l_kj=0
                        for ks in range(4):
                            for js in range(4):
                                l_kj=l_kj+Ak[ks]*Aj[js]*HH2[ks][js]
                        lamda[k][j]=l_kj
    return lamda
                        
                        
                        
                        
                        
                        
    
                        
                        
                        
                    
                        
                
                                
                        
                        
                        
                
