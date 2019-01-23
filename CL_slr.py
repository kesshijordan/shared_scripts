#!/usr/bin/env python

import nibabel as nib
import sys
from dipy.align.streamlinear import StreamlineLinearRegistration
from dipy.tracking.streamline import set_number_of_points

'''
This is a quick script to register two bundles rigidly.
(based on http://nipy.org/dipy/examples_built/bundle_registration.html)

Usage: slr_rigid.py fixed_track.trk moving_track.trk

Output: moving_track_in_fixed_track_rigid.trk
'''

fixed_path = sys.argv[1]
moving_path = sys.argv[2]
f_trk,f_hdr = nib.trackvis.read(fixed_path)
m_trk, m_hdr = nib.trackvis.read(moving_path)

f_sls = [item[0] for item in f_trk]
m_sls = [item[0] for item in m_trk]

f_subsamp = set_number_of_points(f_sls, 10)
m_subsamp = set_number_of_points(m_sls, 10)

srr = StreamlineLinearRegistration()

srm = srr.optimize(static=f_subsamp, moving=m_subsamp)

m_sls_in_fsp = srm.transform(m_sls)

savepath = moving_path.replace('.trk','_rigidxfm.trk')

newtrk = ((item, None, None) for item in m_sls_in_fsp)
nib.trackvis.write(savepath, newtrk, m_hdr)
