# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 16:25:57 2024

@author: Qiujin
"""
import numpy as np
# Original rigid response coefficent defined by Lindeley and Yow (1980)
#sai: the spectral acceleration of the ith mode
#fi: modal frequency
def lindley_rigid (PGA,sai):
    alphai=PGA/sai
    if alphai>1:
        alphai=0
    
    return alphai