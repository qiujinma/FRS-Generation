# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 16:20:33 2024

@author: Qiujin
"""
import numpy as np
# Original rigid response coefficent defined by Gupta (1990)
#fi: modal frequency of ith mode in Hz
def gupta_rigid(fi,F1,fr):
    F2=(F1+2*fr)/3
    if fi<F1:
        alphai=0
    elif fi>=F1 and fi<=F2:
        alphai=np.log(fi/F1)/np.log(F2/F1)
    elif fi>F2:
        alphai=1
    return alphai