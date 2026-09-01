# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 15:26:35 2026

@author: Qiujin
"""

def save_plot_FRS(dofs,RS_frequency,FRS, FRS_broadened, result_folder):
    import matplotlib.pyplot as plt
    import os
    
    OutDir=result_folder
    if not os.path.exists(OutDir):
        os.makedirs(OutDir)
    
    #plot FRS results
    for dof in dofs:
        fig1 = plt.figure(figsize=(3.5,2.5), dpi=600)
        plt.xscale("log")
        plt.plot(RS_frequency,FRS[dof],c='b', label='Proposed')
        plt.plot(RS_frequency,FRS_broadened[dof],c='r',linestyle='dashed', label='Broadened')
        plt.legend(fontsize=7,loc='upper left')
        plt.title("DOF"+str(dof), fontsize=7) 
        plt.xlabel('Frequency (Hz)',fontsize=7)
        plt.ylabel('FRS (g)',fontsize=7)
        plt.xticks(fontsize=7)
        plt.yticks(fontsize=7)
        plt.grid(which ='both',linewidth=0.4)
        plt.savefig(OutDir+'/FRS_DOF'+str(dof)+'.png', dpi=600, bbox_inches='tight')
        plt.show()
        
        
    #save FRS to file
    for dof in dofs:
    
        results = open(OutDir + '/FRS_DOF'+str(dof)+'.csv', 'w')
        results.write('FRS \n')
        results.write('values seperated by a comma,\n')
        results.write('F [Hz], FRS [g], Broadened_FRS [g] \n')
        for ii in range(len(RS_frequency)):
            results.write(str(round(RS_frequency[ii],5)) + ',' + str(round(FRS[dof][ii],8)) + ',' + str(round(FRS_broadened[dof][ii],8)) +  '\n')
        results.close()

        