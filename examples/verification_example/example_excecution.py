#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 11:18:57 2026

@author: maqiujin
"""

from pathlib import Path
import sys

src_path = Path(__file__).resolve().parents[2] / "src"
sys.path.insert(0, str(src_path))

from frs_generation.main_FRS import main_FRS    #Function for FRS evaluation
from frs_generation.read_spectrum import read_spectrum   #Function to read input response spectrum
from frs_generation.read_modal_prop import read_modal_prop  #Function to read modal properties of the supporting structure
from frs_generation.save_plot_FRS import save_plot_FRS  # Function to save and plot FRS results

#Define target response spectrum
# Read response spectrum file
# Input spectrum: Sa(m/s^2), Sv(m/s), Sd(m) 
    #Frequency range (Hz):  RS_frequency  
    #Damping ratio range: xis
    #Rigid frequency (Hz): fr
    #PGA (m/s^2)
xis=[0.02,0.05,0.07,0.10]
spectral_folder='spectrum_input'
spectral_file='/RS_values.csv'
Sa, Sv, Sd, RS_frequency = read_spectrum(spectral_folder, spectral_file, xis)
PGA=3.68 # in m/s^2
#Define the zero period frequency (Hz): the difference in the spectral acceelrations beyond this frequency is within 2%.
fr=44

#Define supporting structure properties for 5dof2
#Rayleigh coefficient
al=[5.2558, 0.000334501]
modal_prop_file='Modal_Properties.csv'
mode_shape_file='Mode_Shapes.csv'
w_p, partis, x_p, phi = read_modal_prop(modal_prop_file, mode_shape_file,al)

#Define dof of interest
dofs=[1,2,3,4,5]

#Define the FRS damping ratio
xo=0.05

# FRS excecution
FRS, FRS_broadened=main_FRS(dofs, w_p, x_p, phi, partis, al, fr, PGA, Sa, Sv, Sd, RS_frequency, xis, xo)  # unit (g)

# Plot and save FRS results
result_folder='FRS_RESULTS'
save_plot_FRS(dofs,RS_frequency,FRS, FRS_broadened, result_folder)

#Check with FRS from time history results and the direct evaluation results from Ma and Kwon (2026)
import matplotlib.pyplot as plt
for dof in dofs:
    #Read time history results from file
    file1='reference_results'+'/FRS_DOF'+str(dof)+'.csv'
    f1 = open(file1).readlines()
    tha=[]
    frs=[]
    for j in range(2,len(f1)):
        values=f1[j].split(',')
        tha.append(float(values[1]))
        frs.append(float(values[2]))
    fig1 = plt.figure(figsize=(3.5,2.5), dpi=600)
    plt.xscale('log')
    plt.plot(RS_frequency,tha, c='k',label='THA')
    plt.plot(RS_frequency,frs,c='c',linestyle='dashdot',label='Direct from paper')
    plt.plot(RS_frequency,FRS[dof],c='r',linestyle='dashed',label='Implementation')
    plt.title("DOF"+str(dof), fontsize=7) 
    plt.legend(fontsize=7,loc='upper left')
    plt.xlabel('Frequency (Hz)',fontsize=7)
    plt.ylabel('FRS (g)',fontsize=7)
    plt.xticks(fontsize=7)
    plt.yticks(fontsize=7)
    plt.grid(which ='both',linewidth=0.4)
    plt.show()

