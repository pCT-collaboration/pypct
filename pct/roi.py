"""
Region of interest objects. 

A region of interest (ROI) is a geometric area of an image that should 
be analyzed. Most of the work is done by creating "array masks" that can 
be applied to images (numpy arrays) to select only specific pixels.

More types of regions need to be added (e.g., rotated rectangle) along 
with more analysis methods. If many analysis methods are added, it may 
make more sense to move those out of the ROI objects to keep them from 
getting too cluttered.

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
from math import sqrt

class ROI(object):
	'''Generic ROI'''
	
	def __init__(self, name, location, size, imageshape):
		self.name = name
		self.location = location
		self.size = size
		self.imageshape = imageshape
		self.mask = None
	
	def calculateArea(self):
		if self.mask == None:
			self.mask = self.makeArrayMask()
		area = 0
		for p in self.mask.flat:
			if p: area += 1
		return area
	
	def measure(self, pixel_array):
		if self.mask == None:
			self.mask = self.makeArrayMask()
		mean = pixel_array[self.mask].mean()
		sigma = pixel_array[self.mask].std()
		return mean, sigma
	
	def plotHistogram(self, pixel_array, bins=100):
		if self.mask == None:
			self.mask = self.makeArrayMask()
		plot.hist(pixel_array[self.mask], histtype='step', bins=bins)
		plot.xlabel('RSP')
		plot.title(self.name)
		plot.show()
	
	def makeArrayMask(self):
		raise NotImplementedError
	
	def getOverlayPatch(self):
		raise NotImplementedError

class CircleROI(ROI):
	'''Circular ROI
	location: tuple of coordinates of its center (x, y)
	size: radius
	'''
	
	def __init__(self, name, location, size, imageshape):
		ROI.__init__(self, name, location, size, imageshape)
		self.mask = self.makeArrayMask()
		self.area = self.calculateArea()
	
	def makeArrayMask(self):
		x, y = self.location
		r = self.size
		mask = np.zeros(self.imageshape, bool)
		for row in range(y - r, y + r + 1):
			if row >= 0 and row < self.imageshape[1]:
				for column in range(x - r, x + r + 1):
					if column >= 0 and column < self.imageshape[0]:
						distance = (row - y)**2 + (column - x)**2
						if distance <= r**2:
							mask[row][column] = True
		return mask
	
	def getOverlayPatch(self, color='red'):
		return mpl.patches.Circle(self.location, radius=self.size, facecolor='none', edgecolor=color, label=self.name)
	
	def getRadialProfile(self, pixels):
		if self.mask == None:
			self.mask = self.makeArrayMask()
		values = []
		points = range(self.size)
		indices = np.indices(pixels.shape)
		xs = indices[0][self.mask]
		ys = indices[1][self.mask]
		for r in points:
			values_at_r = []
			min_dist_sq = max(r - 1, 0)**2
			max_dist_sq = r**2
			for x, y in zip(xs, ys):
				dist_sq = (x - self.location[0])**2 + (y - self.location[1])**2
				if dist_sq <= max_dist_sq and dist_sq >= min_dist_sq:
					values_at_r.append(pixels[x][y])
			values.append(np.mean(values_at_r))
		return points, values
	
	def plotRadialProfile(self, pixels):
		points, values = self.getRadialProfile(pixels)
		fig = plot.figure()
		ax = fig.add_subplot(1, 1, 1)
		plot.plot(points, values)
		plot.title(self.name + ' - Radial Profile')
		plot.xlabel('r (pixel)')
		plot.ylabel('RSP')
		return fig

class RectangleROI(ROI):
	'''Rectangular ROI
	location: tuple of coordinates of its upper left corner (x, y)
	size: tuple of dimensions (w, h)
	'''
	
	def __init__(self, name, location, size, imageshape):
		ROI.__init__(self, name, location, size, imageshape)
		self.mask = self.makeArrayMask()
		self.area = self.calculateArea()
		
	def makeArrayMask(self):
		x, y = self.location
		w, h = self.size
		mask = np.zeros(self.imageshape, bool)
		for row in range(y, y + h):
			if row >= 0 and row < self.imageshape[1]:
				for column in range(x, x + w):
					if column >= 0 and column < self.imageshape[0]:
						mask[row][column] = True
		return mask
		
	def getOverlayPatch(self, color='red'):
		return mpl.patches.Rectangle(self.location, self.size[0], self.size[1], facecolor='none', edgecolor=color, label=self.name)
	
	def getLineProfile(self, pixels, axis=0):
		if self.mask == None:
			self.mask = self.makeArrayMask()
		masked_pixels = pixels[self.mask]
		masked_pixels.shape = self.size[::-1]
		values = masked_pixels.mean(axis=axis)
		points = range(self.location[axis], self.location[axis] + len(values))
		return points, values
	
	def plotLineProfile(self, pixels, axis=0):
		points, values = self.getLineProfile(pixels, axis)
		fig = plot.figure()
		ax = fig.add_subplot(1, 1, 1)
		plot.plot(points, values)
		plot.title(self.name + ' - Line Profile')
		plot.xlabel('x (pixel)' if axis == 0 else 'y (pixel)')
		plot.ylabel('RSP')
		return fig
