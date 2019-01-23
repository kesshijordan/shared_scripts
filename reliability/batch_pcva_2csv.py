#!/usr/bin/env python

#This script runs a batch to get the pcva overlaps for inter-rater reliability

import os
import operator
from pcva_calc import return_pcva
import csv

def save_data_csv(file_path, file_list, data, fieldnames=None):
    with open(file_path, 'wb') as file:
        writer = csv.writer(file)
        count=0
        if fieldnames is not None:
            writer.writerow(fieldnames)
        for item in data:
            writer.writerow((file_list[count],item[0],item[1],item[2]))
            count=count+1

subject_list = ['sub1','sub2','sub3']
data_loc = 'path_to_data'
save_loc = 'path_to_save_location'
operator_list = ['op2','op1']

owd = os.getcwd()

pcva_list = []
file_list = []
lost_list = [] #DO THIS

for sub in subject_list:
    os.chdir(data_loc+sub)
    binim_loc1 = data_loc+sub+'/'+operator_list[0]+'/TRACKs/Results/binthresh_final/'
    binim_loc2 = data_loc+sub+'/'+operator_list[1]+'/TRACKs/Results/binthresh_final/'
    for file in sorted(os.listdir(binim_loc1)):
        otherfile = list(file)
        #print otherfile[-21]
        otherfile[-21] = 'E'
        otherfile = ''.join(otherfile)
        #reduce(operator.add,otherfile)
        print sub+'_'+otherfile
        file_list.append(sub+'_'+otherfile)
        if os.path.exists(binim_loc2+otherfile):
            #print "found match: "+binim_loc2+otherfile
            pcva = return_pcva(binim_loc1+file,binim_loc2+otherfile)
            pcva_list.append(pcva)
            print "pcva_#voxop1_#voxop2: "+str(pcva)
        else:
            print "could not find: "+ binim_loc2+otherfile
            lost_list.append(binim_loc2+otherfile) # DO THIS

save_file = save_loc+'pcva_results_final.csv'
save_data_csv(save_file,file_list,pcva_list,("filename","pcva","#voxK","#voxE"))
print "NEVER FOUND"
print lost_list #DO THIS

os.chdir(owd)

