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
voxel_size = (270.0 / 512, 270.0 / 512, 0.625)
slicenum = 110

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
imgplot = pyplot.imshow(voxels[:, :, slicenum], cmap='gray', interpolation='nearest')
pyplot.xlabel('x (pixel)')
pyplot.ylabel('y (pixel)')
cbar = pyplot.colorbar()
cbar.set_label('RSP' if convert_to_rsp else 'HU')
#pyplot.show()


outfile = '{}/slice{}-{:03d}.txt'.format(inputdir, '-rsp' if convert_to_rsp else '', slicenum)
print 'Dumping slice {} to {}'.format(slicenum, outfile)
start = time.time()
pct.ctload.dumpSlice(voxels[:, :, slicenum], outfile)
stop = time.time()
print 'Took {:.4f}s total time'.format(stop - start)


print 'Creating projection along y-axis'
start = time.time()
mask = np.loadtxt(inputdir + '/mask.txt', dtype=bool)
projection = np.empty((voxels.shape[2], voxels.shape[0]))
for slicenum in xrange(voxels.shape[2]):
    slice = voxels[:, :, slicenum]
    for row in xrange(slice.shape[0]):
        total = 0.0
        for col in xrange(slice.shape[1]):
            if mask[col, row]:
                total += slice[col, row] * voxel_size[1]
        projection[slicenum, row] = total
stop = time.time()
print 'Took {:.4f}s total time'.format(stop - start)

fig = pyplot.figure()
ax = fig.add_subplot(1, 1, 1)
imgplot = pyplot.imshow(projection, cmap='gray', interpolation='nearest')
pyplot.xlabel('x (pixel)')
pyplot.ylabel('z (pixel)')
cbar = pyplot.colorbar()
cbar.set_label('WEPL (mm)' if convert_to_rsp else '')


outfile = '{}/projection{}.txt'.format(inputdir, '-rsp' if convert_to_rsp else '')
print 'Dumping projection to {}'.format(outfile)
start = time.time()
pct.ctload.dumpSlice(projection, outfile)
stop = time.time()
print 'Took {:.4f}s total time'.format(stop - start)

pyplot.show()
