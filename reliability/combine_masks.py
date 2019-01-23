#!/usr/bin/env python

#This script combines masks

import os
import nibabel as nib
import numpy as np

#this returns a combined mask that includes all voxels in either mask (added in a boolean sense)
def return_combo_mask(bin1_path, bin2_path,flag_whatrep):

    if flag_whatrep == 1: #if it's the first one, then you actually have to load both datasets...otherwise you are just loading the new one that will be added to the existing mask (already a variable)
        bin1_img = nib.load(bin1_path)
        bin1_data = bin1_img.get_data()
    else:
        bin1_data = bin1_path
    
    
    bin2_img = nib.load(bin2_path)

    
    bin2_data = bin2_img.get_data()

    bool1_data = (bin1_data>0)
    bool2_data = (bin2_data>0)
    
    either_yes = bool1_data | bool2_data

    return either_yes

##yes_yes_saved = nib.Nifti1Image(yes_yes,bin1_img.get_affine(),header=bin1_img.get_header())

#yes_yes_saved = nib.Nifti1Image(yes_yes,bin1_img.get_affine())


#this returns a combined density mask so the masks are added numerically
def return_added_mask(bin1_path, bin2_path,flag_whatrep):

    if flag_whatrep == 1:
        bin1_img = nib.load(bin1_path)
        bin1_data = bin1_img.get_data()
        intbool1_data = 1.*(bin1_data==1)

    else:
        intbool1_data = bin1_path
    
    
    bin2_img = nib.load(bin2_path) 
    bin2_data = bin2_img.get_data()  
    intbool2_data = 1.*(bin2_data==1)
    
    sum_yes = intbool1_data + intbool2_data
    print np.max(sum_yes)

    return sum_yes

