"""
Tools for converting x-ray CT DICOM files to RSP

TODO: return a pypct Image object, with sorted slices (need to look at slice number in DICOM file)

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

def loadDicomFile(filename, convert_to_rsp=False):
    '''
    Open the named dicom file. Optionally convert to RSP.
    Returns a numpy array containing RSP values.
    '''    
    slice = dicom.read_file(filename)
    im = slice.pixel_array
    slice_num = slice.InstanceNumber

    pixel_array = np.zeros((im.shape[0], im.shape[1]))
    
    for i in range(im.shape[0]):
        for j in range(im.shape[1]):
            if convert_to_rsp:
                pixel_array[i][j] = convertToRSP(float(im[i][j]))
            else:
                pixel_array[i][j] = float(im[i][j])
    
    return rsp_data

def processDicomDirectory(dirname, extension='.dcm'):
    '''Open all files in dirname with extension.
    Returns a 3D array of RSP values. Indices are: [x (horiz)][y (vert)][z (slice)]
    '''
    stack = []
    filelist = os.listdir(dirname)
    for filename in filelist:
        if filename[-4:] == extension:
            stack.append(loadDicomFile(dirname + '/' + filename))
    stack = np.dstack(stack)
    return stack
    
