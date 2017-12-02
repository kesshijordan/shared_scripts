#!/usr/bin/env python
import nibabel as nib
import sys
import numpy as np

'''
This is a quick script to resave LAS to LPS and vice versa.

Usage: flip_las_lps.py mytrack.trk

Output: mytrack_LA(P)S.trk
'''

def flipsls(sls, vsz, dim):
    newlist = []
    for sl in sls:
        newsl = sl.copy()
        newsl[:,1]=dim[1]*vsz[1]-sl[:,1]
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
    newhdr['voxel_order'] = np.array('LPS')
    newhdr['pad2'] = np.array('LPS')
    savepath = inpath.replace('.trk','_LPS.trk')
elif vorder.upper().strip('\'') == 'LPS':
    newhdr['voxel_order'] = np.array('LAS')
    newhdr['pad2'] = np.array('LAS')
    savepath = inpath.replace('.trk','_LAS.trk')
else:
    raise('Please use this script for LAS or LPS images only')

newtrk = ((item, None, None) for item in newsls)
nib.trackvis.write(savepath, newtrk, newhdr)
