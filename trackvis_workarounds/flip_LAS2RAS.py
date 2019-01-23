#!/usr/bin/env python
import nibabel as nib
import sys
import numpy as np

'''
This is a quick script to resave LAS to RAS 

Usage: flip_LAS2RAS.py mytrack.trk

Output: mytrack_RAS.trk
'''

def flipsls(sls, vsz, dim):
    newlist = []
    for sl in sls:
        newsl = sl.copy()
        newsl[:,0]=dim[0]*vsz[0]-sl[:,0]
        newlist.append(newsl)
    return newlist

inpath = sys.argv[1]
trk,hdr = nib.trackvis.read(inpath)
sls = [item[0] for item in trk]

dim = hdr['dim']
vsz = hdr['voxel_size']
vorder = str(hdr['voxel_order'])[-4:]

print(vorder)

newsls = flipsls(sls, vsz, dim)

newhdr = hdr.copy()

if vorder.upper().strip('\'') == 'LAS':
    newhdr['voxel_order'] = np.array('RAS')
    newhdr['pad2'] = np.array('RAS')
    savepath = inpath.replace('.trk','_RAS.trk')
else:
    raise('Please use this script for LAS to RAS xfm only')

newtrk = ((item, None, None) for item in newsls)
nib.trackvis.write(savepath, newtrk, newhdr)
