#!/usr/bin/env python

'''This script calculates the PCVA; a percent volume overlap calculation
defined as [intersection/sum]*200%'''

import nibabel as nib
import numpy as nm


def return_pcva(bin1_path, bin2_path):

    bin1_img = nib.load(bin1_path)
    bin2_img = nib.load(bin2_path)

    bin1_data = bin1_img.get_data()
    bin2_data = bin2_img.get_data()

    bool1_data = (bin1_data == 1)
    bool2_data = (bin2_data == 1)

    yes_yes = bool1_data & bool2_data
    # no_no = ~(bool1_data | bool2_data)
    # yes_no = bool1_data & (~bool2_data)
    # no_yes = bool2_data & (~bool1_data)

    volvx1 = sum(sum(sum(bool1_data)))
    volvx2 = sum(sum(sum(bool2_data)))

    yyvolvx = sum(sum(sum(yes_yes)))
    # nnvolvx = sum(sum(sum(no_no)))
    # ynvolvx = sum(sum(sum(yes_no)))
    # nyvolvx = sum(sum(sum(no_yes)))

    PCVA = nm.multiply(nm.true_divide(yyvolvx, nm.add(volvx1, volvx2)), 200)

    return PCVA, volvx1, volvx2


if __name__ == '__main__':
    import sys

    if len(sys.argv) != 3:
        print("need two arguments")
        exit(1)

    bin1_path = sys.argv[1]
    bin2_path = sys.argv[2]

    PCVA, volvx1, volvx2 = return_pcva(bin1_path, bin2_path)
    print('PCVA:')
    print(PCVA)
    print('# voxels in ' + bin1_path+':')
    print(volvx1)
    print('# voxels in ' + bin2_path+':')
    print(volvx2)
