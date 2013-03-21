pyPCT
======

Collection of Python modules for analyzing, processing, and converting reconstructed proton CT images.

### Authors ###

- Ford Hurley (ford.hurley@gmail.com)


### Dependencies ###

- `numpy`: http://numpy.scipy.org/
- `matplotlib`: http://matplotlib.org/
- `pyDICOM`: http://code.google.com/p/pydicom/


### Modules ###

#### image ####

Provides classes for storing pCT images/slices as arrays. Can read in text formatted images (as outputted by the Penfold code). Can produce matplotlib plots of images with RSP level scales, with optional overlaid regions of interest.

#### roi ####

Region of interest classes. Most image analysis is done here.

#### ctconvert ####

Used to convert DICOM formatted x-ray CT images into text images, with values of Hounsfield Units (HU) or relative stopping power (RSP).


### How to use ###

One good way to use the modules would be to check out the repository, then add a symlink to the pypct folder in your python's 'site-packages' directory:

    ln -s pypct /usr/local/lib/python2.7/pypct

This will allow you to 'import pypct' from a script run anywhere on the computer, and still take advantage of any updates you make to to package or get from an update.
