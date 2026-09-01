# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 14:17:24 2024

@author: Qiujin
"""
#Calculate coefficient matrix in Eqn (9) for modal FRS calculation
def coef_matrix(dof,wo,xo,w1,x1):
    import numpy as np
    cqc_para_real=np.eye(2*dof+2, dtype=float)
    
    ww=np.zeros(dof+1)
    ww[0]=wo
    ww[1]=w1
    
    xx=np.zeros(dof+1)
    xx[0]=xo
    xx[1]=x1
    
    for k in range(dof+1):
        wk=ww[k]
        xk=xx[k]
        for j in range(dof+1):
            wj=ww[j]
            xj=xx[j]
                
            D01=(wk**2-wj**2)**2+4*wk*wj*xk*xj*(wk**2+wj**2)+4*wk**2*wj**2*(xk**2+xj**2)
            cqc_para_real[2*k][2*j]=8*wk*wj*np.sqrt(wk*wj*xk*xj)*(wk*xj+wj*xk)/D01
            cqc_para_real[2*k][2*j+1]=-4*(wk**2-wj**2)*np.sqrt(wk*wj**3*xk*xj)/D01
            cqc_para_real[2*k+1][2*j]=4*(wk**2-wj**2)*np.sqrt(wj*wk**3*xk*xj)/D01
            cqc_para_real[2*k+1][2*j+1]=8*wk*wj*np.sqrt(wk*wj*xk*xj)*(wk*xk+wj*xj)/D01
            cqc_para_real[2*j][2*k]=cqc_para_real[2*k][2*j]
            cqc_para_real[2*j][2*k+1]=cqc_para_real[2*k+1][2*j]
            cqc_para_real[2*j+1][2*k]=cqc_para_real[2*k][2*j+1]
            cqc_para_real[2*j+1][2*k+1]=cqc_para_real[2*k+1][2*j+1]
            
    return cqc_para_real
    