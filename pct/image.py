"""
Proton CT image objects. Provides Slice and Image (array of Slices) classes.

These are very imcomplete, but could be extended to be pretty powerful with a little work.

=================

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

import numpy as np
import matplotlib.pyplot as plot
import matplotlib as mpl
import roi as pctroi

def iterable(y):
	try: iter(y)
	except: return 0
	return 1

class Slice(object):
	def __init__(self, filename, num):
		self.filename = filename,
		self.num = num
		self.pixels = self._readSliceFile(filename)
		self.shape = self.pixels.shape
	
	def _readSliceFile(self, filename):
		pixel_data = []
		with open(filename) as file:
			for line in file:
				row = line.strip().split(' ')
				row = [float(p) for p in row]
				pixel_data.append(row)
		return np.array(pixel_data)
	
	def plot(self, regions=None, window=None, level=None):
		'''Plot the slice.
		Accepts a region or list of regions, and window and level options.
		Returns a matplotlib figure that can then be displayed or saved.
		'''
		fig = plot.figure()
		ax = fig.add_subplot(1, 1, 1)
		imgplot = plot.imshow(self.pixels, cmap='gray', interpolation='nearest')
		plot.xlabel('x (pixel)')
		plot.ylabel('y (pixel)')
		cbar = plot.colorbar()
		cbar.set_label('RSP')
		
		if window != None and level != None:
			imgplot.set_clim(level - window/2, level + window/2)
		
		if regions:
			colors = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black', 'white']
			i = 0
			
			if not iterable(regions):
				if isinstance(regions, pctroi.ROI):
					regions = [regions]
				else:
					raise ValueError('region is not a valid ROI object')
			
			for roi in regions:
				patch = roi.getOverlayPatch(colors[i])
				if patch: ax.add_patch(patch)
				i += 1
				if i >= len(colors): i = 0
			plot.legend()
		
		return fig
	
class Image(object):
	def __init__(self, iteration=None):
		self.slices = []
		self.shape = None
		self.iteration = iteration
	
	def addSlice(self, filename, slicenum=None):
		slice = Slice(filename, slicenum)
		if self.shape is None:
			self.shape = slice.shape
		elif self.shape != slice.shape:
			raise Exception("Dimensions of slices in image do not match!")
		self.slices.append(slice)
	
	def plotSlice(self, slicenum, regions=None, window=None, level=None):
		return self.getSlice(slicenum).plot(regions, window, level)
	
	def getSlice(self, slicenum):
		slicenums = [slice.num for slice in self.slices]
		try:
			sliceindex = slicenums.index(slicenum)
		except ValueError:
			raise ValueError('Slice %d is not in image.' % slicenum)
		return self.slices[sliceindex]
