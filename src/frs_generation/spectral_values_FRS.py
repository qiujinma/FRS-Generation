# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 11:25:24 2026

@author: Qiujin
"""

def spectral_values(x_p1, w_p1, xis, xo, Sa, Sv, Sd, RS_frequency):
    import numpy as np
    
    #define spectral values (rd, rv, and ra), and F1 (used for rigid response coefficnet calculation from Eqn (23)) for the modes of interest of the supporting structure (with subscript 'p')             
    F1_p=[]
    rd_p=[]
    rv_p=[]
    ra_p=[]
    for mode in range(len(x_p1)):
        x1=x_p1[mode]
        fp=w_p1[mode]/(2*np.pi)
        for i in range(len(xis)):
            if x1==xis[i]:
                print('find exact damping')
                F1_p.append(max(Sa[xis[i]])/(2*np.pi*max(Sv[xis[i]])))
                
                rd_pp=np.interp(fp,RS_frequency,Sd[xis[i]])
                rd_p.append(rd_pp)
                rv_pp=np.interp(fp,RS_frequency,Sv[xis[i]])
                rv_p.append(rv_pp)
                ra_pp=np.interp(fp,RS_frequency,Sa[xis[i]])
                ra_p.append(ra_pp)

            elif x1>xis[i] and x1<xis[i+1]:
                print('damping interpolate')
                saa=[]
                svv=[]
                sdd=[]
                for js in range(len(RS_frequency)):
                    ra=np.interp(x1,[xis[i],xis[i+1]],[Sa[xis[i]][js],Sa[xis[i+1]][js]])
                    saa.append(ra)
                    rv=np.interp(x1,[xis[i],xis[i+1]],[Sv[xis[i]][js],Sv[xis[i+1]][js]])
                    svv.append(rv)
                    rd=np.interp(x1,[xis[i],xis[i+1]],[Sd[xis[i]][js],Sd[xis[i+1]][js]])
                    sdd.append(rd)
                F1_p.append(max(saa)/(2*np.pi*max(svv)))
                
                rd_pp=np.interp(fp,RS_frequency,sdd)
                rd_p.append(rd_pp)
                rv_pp=np.interp(fp,RS_frequency,svv)
                rv_p.append(rv_pp)
                ra_pp=np.interp(fp,RS_frequency,saa)
                ra_p.append(ra_pp)
                
    #Define the spectral values for the frequency of interst based on the NSC damping level and the F1 for rigid response coefficient calculation
    for i in range(len(xis)):
        if xo==xis[i]:
            ra_s=Sa[xis[i]]
            rv_s=Sv[xis[i]]
            rd_s=Sd[xis[i]]
            
            F1_s=max(ra_s)/(2*np.pi*max(rv_s))
        elif xo>xis[i] and xo<xis[i+1]: 
            ra_s=[]
            rv_s=[]
            rd_s=[]
            for js in range(len(RS_frequency)):
                ra=np.interp(xo,[xis[i],xis[i+1]],[Sa[xis[i]][js],Sa[xis[i+1]][js]])
                ra_s.append(ra)
                rv=np.interp(xo,[xis[i],xis[i+1]],[Sv[xis[i]][js],Sv[xis[i+1]][js]])
                rv_s.append(rv)
                rd=np.interp(xo,[xis[i],xis[i+1]],[Sd[xis[i]][js],Sd[xis[i+1]][js]])
                rd_s.append(rd)
            F1_s=(max(ra_s)/(2*np.pi*max(rv_s)))
    
    return F1_s, ra_s, rv_s, rd_s, F1_p, ra_p, rv_p, rd_p