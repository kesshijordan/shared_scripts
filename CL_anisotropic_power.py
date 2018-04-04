#!/usr/bin/env python

'''This script is a command-line implementation to calculate anisotropic power
using DIPY (https://github.com/nipy/dipy).

Flavio Dell’Acqua,  Luis Lacerda,  Marco Catani,  Andrew Simmons. Anisotropic
Power Maps: A diffusion contrast to reveal low anisotropy tissues from HARDI
data, Proceedings Joint Annual Meeting ISMRM-ESMRMB, ISMRM2014, Milan , 2014pg.
0730

'''

from dipy.reconst import shm
from dipy.data import get_sphere
from dipy.data.fetcher import gradient_table
from dipy.reconst.peaks import peaks_from_model
import nibabel as nb
import numpy as np
from glob import glob
import os.path as op


def loadnii(path):
    im = nb.load(path)
    data = im.get_data()
    aff = im.affine
    return data, aff


def savenii(data, affine, savename):
    nb.Nifti1Image(data.astype("float32"), affine).to_filename(savename)


def calculate_anisotropic_power_map(data, gtab, mask):
    # Fit Qball model
    model = shm.QballModel(gtab, 8)
    sphere = get_sphere('symmetric724')
    peaks = peaks_from_model(model=model, data=data,
                             relative_peak_threshold=.5,
                             min_separation_angle=25,
                             sphere=sphere, mask=mask)
    # return anisotropic power
    apm = shm.anisotropic_power(peaks.shm_coeff)
    return apm


def process_CL(data_path, bval_path, bvec_path, mask_path):
    data, aff = loadnii(data_path)
    mask, maff = loadnii(mask_path)
    # check that mask is in same space as diffusion data
    assert(np.all(aff == maff))
    gtab = gradient_table(bval_path, bvec_path)
    apm = calculate_anisotropic_power_map(data, gtab, mask)
    savename = data_path.replace('.nii', '_APqball.nii')
    print('SAVING TO %s' % (savename))
    savenii(apm, aff, savename)
    return savenii


if __name__ == '__main__':
    import sys

    if len(sys.argv) == 2:
        print("Looking for matches to template")
        input_path = op.abspath(sys.argv[1])
        basename = input_path.split('.')[0]
        print('processing %s' % (basename))

        # make sure there aren't multiple file names that fit template
        nii_path = glob(basename + '.nii*')
        bval_path = glob(basename + '.bval')
        bvec_path = glob(basename + '.bvec')
        mask_path = glob(basename + '_mask.nii*')

        if len(nii_path) == 1 and len(bval_path) == 1 and len(bvec_path) == 1:
            nii_path = nii_path[0]
            bval_path = bval_path[0]
            bvec_path = bvec_path[0]
            mask_path = mask_path[0]
        else:
            print(nii_path)
            print(bval_path)
            print(bvec_path)
            print(mask_path)
            raise('Please ensure that exactly one filename matches your '
                  'template in each category: diff data, bval, bvec, mask')
    elif len(sys.argv) == 5:
        nii_path = sys.argv[1]
        bval_path = sys.argv[2]
        bvec_path = sys.argv[3]
        mask_path = sys.argv[4]
    else:
        raise('Input not recognized as valid combination')
    process_CL(nii_path, bval_path, bvec_path, mask_path)
