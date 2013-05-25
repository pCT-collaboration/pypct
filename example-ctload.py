#!/usr/bin/evn python

"""
Example script for using pypct to load a directory full of DICOM images.

===============

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

import os, errno
import time

import numpy as np
import matplotlib.pyplot as pyplot

import pct.ctload

inputdir = 'Z:/Downloads/handCT_20120724'
convert_to_rsp = True

start = time.time()

numpy_file = '{}/voxels{}.npy'.format(inputdir, '-rsp' if convert_to_rsp else '')
try:
    print 'Loading voxel array from', numpy_file
    voxels = np.load(numpy_file, 'r')
except:
    print 'Loading DICOM images from', inputdir
    if convert_to_rsp:
        print 'This may take a while...'
    voxels = pct.ctload.processDicomDirectory(inputdir, convert_to_rsp=convert_to_rsp)
    np.save(numpy_file, voxels)
    
stop = time.time()
print 'Took {:.4f}s total time'.format(stop - start)

fig = pyplot.figure()
ax = fig.add_subplot(1, 1, 1)
imgplot = pyplot.imshow(voxels[:, :, 100], cmap='gray', interpolation='nearest')
pyplot.xlabel('x (pixel)')
pyplot.ylabel('y (pixel)')
cbar = pyplot.colorbar()
cbar.set_label('RSP' if convert_to_rsp else 'HU')

pyplot.show()
