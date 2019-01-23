#!/usr/bin/env python

import nibabel as nib
from dipy.tracking import utils
import sys
import re


def safesavenii(array, aff, path):
    saveim = nib.Nifti1Image(array.astype("int16"), aff)
    saveim.set_qform(aff, 1)
    saveim.set_sform(aff, 1)
    saveim.to_filename(path)


def save_dmap(trkpath, refnii, savepath):
    trk, hdr = nib.trackvis.read(trkpath)
    new_hdr = hdr.copy()

    sls = [item[0] for item in trk]

    refimg = nib.load(refnii)
    refdata = refimg.get_data()
    refaff = refimg.get_affine()

    print('orig_vorder')
    orig_vorder = str(hdr['voxel_order'])
    print(orig_vorder)

    regex_vorder = re.compile('[LlRr][AaPp][SsIi]')
    vorder = re.search(regex_vorder, orig_vorder).group(0)
    print('new_vorder')
    print(vorder)
    new_hdr['voxel_order'] = vorder

    print(new_hdr)

    grid2trk_aff = utils.flexi_tvis_affine(vorder, refaff, hdr['dim'],
                                           hdr['voxel_size'])
    dmap = utils.density_map(sls, refdata.shape, affine=grid2trk_aff)

    safesavenii(dmap, refaff, savepath)


if __name__ == '__main__':
    print(sys.argv)
    trkpath = sys.argv[1]
    niipath = sys.argv[2]
    save_dmap(trkpath, niipath, trkpath.replace('.trk', '_dmap.nii.gz'))
