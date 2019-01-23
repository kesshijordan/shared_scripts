#!/usr/bin/env python

#This script runs a batch to get the dti metrics for all of the inter-rater reliability tracks.

import os
import csv
from getmetrics import calc_dti_metrics

def save_data_csv(file_path, file_list, data, fieldnames=None):
    with open(file_path, 'wb') as file:
        writer = csv.writer(file)
        count=0
        if fieldnames is not None:
            writer.writerow(fieldnames)
        for item in data:
            writer.writerow((file_list[count],item[0],item[1],item[2],item[3]))
            count=count+1

subject_list = ['sub1','sub2','sub3']
operator_list = ['op1','op2']
data_loc = 'path_to_data'
save_loc = 'path_to_save'

owd = os.getcwd()

metric_list = []
file_list = []

for sub in subject_list:
    os.chdir(data_loc+sub)
    fa_nii = []
    L1_nii = []
    md_nii = []
    rd_nii = []
    toomany = []
    nonefound = []
    for file in os.listdir(data_loc+sub):
        if file.endswith('fa.nii.gz'):
            fa_nii.append(file)
        elif file.endswith('L1.nii.gz'):
            L1_nii.append(file)
        elif file.endswith('md.nii.gz'):
            md_nii.append(file)
        elif file.endswith('rd.nii.gz'):
            rd_nii.append(file)
    if not fa_nii:
        nonefound.append(sub+"_fa")
    elif len(fa_nii)>1:
        toomany.append(sub+"_fa")
    if not L1_nii:
        nonefound.append(sub+"_L1")
    elif len(L1_nii)>1:
        toomany.append(sub+"_L1")
    if not md_nii:
        nonefound.append(sub+"_md")
    elif len(md_nii)>1:
        toomany.append(sub+"_md")
    if not rd_nii:
        nonefound.append(sub+"_rd")
    elif len(rd_nii)>1:
        toomany.append(sub+"_rd")
    if toomany or nonefound:
        print("multiple metric files were found for these:")
        print(toomany)
        print("no metric file was found for these:")
        print(nonefound)
        print("Please resolve the above issues prior to proceeding")
    else:
        for oper in operator_list:
            binim_loc = data_loc+sub+"/"+oper+"/TRACKs/Results/binthresh_final"
            subdata_loc = data_loc+sub+'/'
            for binim in sorted(os.listdir(binim_loc)):
                file_list.append(sub+'_'+binim)
                metrics = calc_dti_metrics(binim_loc+'/'+binim, subdata_loc+fa_nii[0], subdata_loc+L1_nii[0], subdata_loc+rd_nii[0], subdata_loc+md_nii[0])
                metric_list.append(metrics)
                print(sub+'_'+binim+'_'+'fa_L1_rd_md:')
                print(metrics)

save_file = save_loc+'dti_metric_results_final.csv'
save_data_csv(save_file,file_list,metric_list,("filename","FA","L1","RD","MD"))

os.chdir(owd)    
