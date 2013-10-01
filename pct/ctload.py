"""
Tools for loading DICOM images from CT scans.

================

Copyright (C) 2013 Ford Hurley, ford.hurley@gmail.com

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import os

import dicom
import numpy as np

hu_conv = ((0.0, 0.0),
           (800.0, 0.8),
           (900.0, 0.95),
           (1000.0, 1.0),
           (1050.0, 1.05),
           (4095.0, 2.45))

def convertToRSP(hu_value):
    if hu_value <= hu_conv[0][0]:
        return 0
    for i in xrange(len(hu_conv)-1):
        if hu_value < hu_conv[i+1][0]:
            slope = (hu_conv[i+1][1] - hu_conv[i][1]) / (hu_conv[i+1][0] - hu_conv[i][0])
            rsp = slope * (hu_value - hu_conv[i][0]) + hu_conv[i][1]
            return rsp
    return 0

def loadDicomFile(filename, convert_to_rsp=True):
    '''
    Open the named dicom file. Optionally convert to RSP.
    Returns a numpy array containing pixel values.
    '''    
    image = dicom.read_file(filename)
    pixel_array = np.array(image.pixel_array, dtype=float)
    slice_num = image.InstanceNumber
    
    if convert_to_rsp:
        for i in xrange(pixel_array.shape[0]):
            for j in xrange(pixel_array.shape[1]):
                pixel_array[i,j] = convertToRSP(pixel_array[i,j])
    
    return pixel_array, slice_num

def processDicomDirectory(dirname, extension='.dcm', convert_to_rsp=True):
    '''
    Open all files in dirname with extension.
    Returns a 3D array of pixel values. Indices are: [x (horiz)][y (vert)][z (slice)]
    '''
    filelist = os.listdir(dirname)
    num = 0
    for filename in filelist:
        if filename[-len(extension):] == extension:
            num += 1
    print 'Found {} files with extension {}'.format(num, extension)
    
    stack = [0] * num
    for filename in filelist:
        if filename[-len(extension):] == extension:
            pixel_array, slice_num = loadDicomFile(dirname + '/' + filename, convert_to_rsp)
            stack[slice_num-1] = pixel_array
            print 'Loaded slice {}'.format(slice_num)
    
    return np.dstack(stack)

def dumpSlice(pixel_array, filename):
    '''
    Write the pixel data to a text file.
    '''
    np.savetxt(filename, pixel_array)
