'''
Tools for converting x-ray CT DICOM files to RSP

TODO: return a pypct Image object, with sorted slices (need to look at slice number in DICOM file)
'''

import dicom
from numpy import *
import image

hu_conv = ((0.0, 0.0),
           (800.0, 0.8),
           (900.0, 0.95),
           (1000.0, 1.0),
           (1050.0, 1.05),
           (4095.0, 2.45))

def convertToRSP(hu_value):
    for i in range(len(hu_conv)-1):
        if hu_value >= hu_conv[i][0] and hu_value < hu_conv[i+1][0]:
            slope = float((hu_conv[i+1][1] - hu_conv[i][1]) / (hu_conv[i+1][0] - hu_conv[i][0]))
            rsp = slope * (hu_value - hu_conv[i][0]) + hu_conv[i][1]
            return rsp
    return 0

def processDicomFile(filename, create_hu_file=False, create_rsp_file=True):
    '''Open the named dicom file, and create text files containing pixel data. 
    Returns an array containing RSP values.
    '''
    print 'Processing', filename
    
    slice = dicom.read_file(filename)
    im = slice.pixel_array
    slice_num = slice.InstanceNumber

    rsp_data = zeros((im.shape[0], im.shape[1]))

    if create_hu_file: outfile_hu = open('hu-s%d.txt' % slice_num, 'w')
    if create_rsp_file: outfile_rsp = open('rsp-s%d.txt' % slice_num, 'w')
    
    for i in range(im.shape[0]):
        for j in range(im.shape[1]):
            if create_hu_file: outfile_hu.write('%f ' % im[i][j])
            rsp_data[i][j] = convertToRSP(float(im[i][j]))
            if create_rsp_file: outfile_rsp.write('%f ' % rsp_data[i][j])
        if create_hu_file: outfile_hu.write('\n')
        if create_rsp_file: outfile_rsp.write('\n')
    
    if create_hu_file: outfile_hu.close()
    if create_rsp_file: outfile_rsp.close()

    return rsp_data

def processDicomDirectory(dirname, extension='.dcm'):
	'''Open all files in dirname with extension.
	Returns a 3D array of RSP values. Indices are: [x (horiz)][y (vert)][z (slice)]
	'''
	stack = []
	filelist = os.listdir(dirname)
	for filename in filelist:
		if filename[-4:] == extension:
			stack.append(processDicomFile(dirname + '/' + filename))
	stack = dstack(stack)
	return stack
	
