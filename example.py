#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plot
import os, errno

import pct

nameformat = 'lucy_scan4_newcal_2012-05-25b_i{iteration:02d}_s{slicenum:02d}.txt'
outputdir = 'example'

try: 
	os.mkdir(outputdir)
except OSError as e: 
	if e.errno == errno.EEXIST:
		# directory already exists
		pass 
	else:
		# some other error occured, reraise it
		raise e

iterations = [8]
slicenums = [10]

images = []
for iteration in iterations:
	image = pct.image.Image(iteration)
	for slicenum in slicenums:
		filename = nameformat.format(iteration=iteration, slicenum=slicenum)
		filename = os.path.join(currentpath, filename)
		print filename
		image.addSlice(filename, slicenum)
	images.append(image)
print

imageshape = None
for image in images:
	if imageshape != None and imageshape != image.shape:
		raise Exception("Dimensions of images do not match!")
	imageshape = image.shape

regions = []
regions.append(pct.roi.RectangleROI('poly1', (103, 51), (51, 55), imageshape))
regions.append(pct.roi.RectangleROI('poly2', (103, 148), (51, 55), imageshape))
regions.append(pct.roi.CircleROI('air', (80, 79), 4, imageshape))
regions.append(pct.roi.CircleROI('bone', (176, 175), 4, imageshape))

images[0].plotSlice(slicenums[0], regions).savefig(os.path.join(currentpath, 'example', 'regions.png'))

for region in regions:
	print region.name
	print '%4s %5s %6s %6s' % ('Iter', 'Slice', 'Mean', 'RMS')
	for image in images:
		for slice in image.slices:
			mean, sigma = region.measure(slice.pixels)
			print '%4d %5d %6f %6f' % (image.iteration, slice.num, mean, sigma)
		print
	
line = pct.roi.RectangleROI('line', (0, 77), (256, 3), imageshape)
images[0].plotSlice(slicenums[0], line).savefig(os.path.join(currentpath, 'example', line.name + '.png'))
figname = os.path.join(currentpath, 'example', line.name + '-profile.png')
line.plotLineProfile(images[0].getSlice(slicenums[0]).pixels, axis=0).savefig(figname)

circle = pct.roi.CircleROI('circle', (80, 79), 15, imageshape)
images[0].plotSlice(slicenums[0], circle).savefig(os.path.join(currentpath, 'example', circle.name + '.png'))
figname = os.path.join(currentpath, 'example', circle.name + '-profile.png')
circle.plotRadialProfile(images[0].getSlice(slicenums[0]).pixels).savefig(figname)
