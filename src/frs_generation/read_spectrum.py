# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 13:57:11 2026

@author: Qiujin
"""
# Input spectrum: Sa(m/s^2), Sv(m/s), Sd(m) 
    #Frequency range (Hz):  RS_frequency  
    #Damping ratio range: xis
def read_spectrum(spectral_folder,spectral_file, xis):
    Sa={}
    Sv={}
    Sd={}
    RS_frequency=[]
    for xi in xis:
        Sa[xi]=[]
        Sv[xi]=[]
        Sd[xi]=[]
        spectral_f=spectral_folder+'/Damping='+str(xi)+'/'+spectral_file
        spec1 = open(spectral_f).readlines()
        for j in range(3,len(spec1)):
            values=spec1[j].split(',')
            if xi==xis[0]:
                RS_frequency.append(float(values[0]))
            Sa[xi].append(float(values[1]))
            Sv[xi].append(float(values[2]))
            Sd[xi].append(float(values[3]))
            
    return Sa, Sv, Sd, RS_frequency