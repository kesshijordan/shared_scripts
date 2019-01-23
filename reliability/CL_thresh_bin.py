#!/usr/bin/env python

import sys
import nibabel as nib


def thresh_and_bin(density_map_nifti, thresh, save_file):
    thresh = int(thresh)
    dens_map = nib.load(density_map_nifti)
    dens_map_data = dens_map.get_data()
    dens_map_hdr = dens_map.get_header()
    dens_map_aff = dens_map.get_affine()
    thresh_bin = 1*(dens_map_data > thresh)
    print("volume = " + str(sum(sum(sum(thresh_bin)))) + " voxels")

    save_img = nib.Nifti1Image(thresh_bin, dens_map_aff, header=dens_map_hdr)
    save_img.to_filename(save_file)


if __name__ == '__main__':
    print(sys.argv)
    density_map_nifti = sys.argv[1]
    thresh = sys.argv[2]
    save_file = sys.argv[3]

    thresh_and_bin(density_map_nifti, thresh, save_file)
