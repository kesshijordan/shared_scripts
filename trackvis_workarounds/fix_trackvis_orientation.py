#!/usr/bin/env python
import nibabel as nib
import sys
'''
This is a quick script to address a bug in Trackvis. The second time a set of streamlines is saved, the 'pad2' field is changed, which makes the background image flipped AP relative to the streamlines and the labels.
'''
badfile = sys.argv[1]

trk,hdr = nib.trackvis.read(badfile)
new_hdr = hdr.copy()
new_hdr['pad2'] = 'las'
nib.trackvis.write(badfile,trk,new_hdr)
