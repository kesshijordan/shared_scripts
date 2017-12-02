#!/usr/bin/env python
import nibabel as nib
import numpy as np
import pylab as pyl
import sys

#define function to calculate end to end length
def calc_end_to_end_len(streamline_array):
    return np.linalg.norm(streamline_array[-1]-streamline_array[0])

trk_file = sys.argv[1]
cutoff = int(sys.argv[2])
cutoff2 = int(sys.argv[3])


if trk_file.find != -1:
    trk_name = trk_file[trk_file.rfind('/')+1:-4]
else:
    trk_name = trk_file[:-4]

# Read trk file from disk
trk, hdr = nib.trackvis.read(trk_file)

# Extract the streamlines from the trk list (first element of each item)
streamlines = [item[0] for item in trk]

#Calculate contour length
contour_len = map(len, streamlines)

# Only keep streamlines of length > 1
good_len_trk = []
good_len_streamlines = []
good_len_contour_len = []
for i in range(len(contour_len)):
    if contour_len[i] != 1:
        good_len_trk.append(trk[i])
        good_len_streamlines.append(streamlines[i])
        good_len_contour_len.append(contour_len[i])

#Calculate end to end length
end2end_len = map(calc_end_to_end_len,streamlines)

contour_len = np.array(contour_len)
end2end_len = np.array(end2end_len)

difference = abs(contour_len-end2end_len)

#establish a cut-off value to define bad track
#cutoff = 120
#cutoff = 90
#cutoff=140
#cutoff2=160

#plot differences
pyl.subplot(211)
pyl.hist(difference)
pyl.axvline(x=cutoff, color='r')

pyl.subplot(212)
pyl.scatter(range(0,len(difference)),difference)
pyl.axhline(y=cutoff, color='r')
fig = pyl.gcf()
fig.canvas.set_window_title(trk_name)
#pyl.show()


#identify the tracks that double back
bad_trk = []
good_trk = []
for j in range(len(difference)):
    if difference[j] > cutoff and difference[j] <=cutoff2:
        bad_trk.append(trk[j])
        #print j
    else:
        good_trk.append(trk[j])

print 'bad:'+str(len(bad_trk))
print 'good:'+str(len(good_trk))

bad_output_file = '/home/kjordan/scripts/trackvis_scripts/testing/testbad_'+trk_name+'.trk'
good_output_file = '/home/kjordan/scripts/trackvis_scripts/testing/testgood_'+trk_name+'.trk'

#bad_output_file = '/home/kjordan/scripts/trackvis_scripts/testing/testbad_'+trk_name+'_th'+str(cutoff)+'to'+str(cutoff2)+'.trk'
#good_output_file = '/home/kjordan/scripts/trackvis_scripts/testing/testgood_'+trk_name+'_th'+str(cutoff)+'to'+str(cutoff2)+'.trk'

#save the bad streamlines to a trk file
nib.trackvis.write(bad_output_file,bad_trk,hdr)
nib.trackvis.write(good_output_file,good_trk,hdr)

pyl.show()
