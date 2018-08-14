#!/usr/bin/env python

from subprocess import check_call
import os.path as op
from glob import glob


def do_preprocessing(diffdata_path, pa_path, ap_path, acq_textfile_path):
    ap_68 = ap_path.replace('.nii', '_68.nii.gz')
    pa_68 = pa_path.replace('.nii', '_68.nii.gz')

    sc_outpath = diffdata_path.replace('.nii', '_SC.nii')

    avg = glob(op.join(op.dirname(ap_path), 'ave.nii*'))[0]

    check_call(['fslroi', pa_path, pa_68,
                '0', '-1', '0', '-1', '0', '68'])
    check_call(['fslroi', ap_path, ap_68,
                '0', '-1', '0', '-1', '0', '68'])

    check_call(['fslmerge', '-t', 'ave',  pa_68, ap_68])

    check_call(['topup', '--imain=' + avg, '--datain='+acq_textfile_path,
                '--config=b02b0.cnf', '--out=ave_output',
                '--fout=ave_my_field', '–iout=ave_my_unwarped_images'])

    check_call(['applytopup', '--imain=' + diffdata_path, '--inindex=2',
                '--datain=' + acq_textfile_path, '--topup=ave_output',
                '--method=jac', '--out='+sc_outpath])


if __name__ == '__main__':
    import sys

    if len(sys.argv) == 4:
        diffdata_path = op.abspath(sys.argv[1])
        ap_path = op.abspath(sys.argv[2])
        pa_path = op.abspath(sys.argv[3])
        acq_params_path = op.abspath(sys.argv[4])
    else:
        raise("MISSING FILES")

    do_preprocessing(diffdata_path, ap_path, pa_path, acq_params_path)
