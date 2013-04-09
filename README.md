pyPCT
======

Collection of Python modules for analyzing, processing, and converting reconstructed 
proton CT images.

### Authors ###

- Ford Hurley (ford.hurley@gmail.com)


### Dependencies ###

- `numpy`: http://numpy.scipy.org/
- `matplotlib`: http://matplotlib.org/
- `pyDICOM`: http://code.google.com/p/pydicom/


### Modules ###

#### [image](pct/image.py) ####

Provides classes for storing pCT images/slices as arrays. Can read in text formatted 
images (as outputted by the Penfold code). Can produce matplotlib plots of images with 
RSP level scales, with optional overlaid regions of interest.

#### [roi](pct/roi.py) ####

Region of interest classes. Most image analysis is done here.

#### [ctconvert](pct/ctconvert.py) ####

Used to convert DICOM formatted x-ray CT images into text images, with values of 
Hounsfield Units (HU) or relative stopping power (RSP).

#### [dataconvert](pct/dataconvert.py) ####

Generally used as a command line tool, this module converts proton history data between 
formats. For help, run:

    python dataconvert.py -h


### How to use ###

One good way to use the modules would be to check out the repository, then add a symlink 
to the pct folder in your python's 'site-packages' directory:

    git clone https://github.com/fordhurley/pypct.git
    cd pypct
    ln -s pct /usr/local/lib/python2.7/pct

This will allow you to 'import pct' from a script run anywhere on the computer, and still 
take advantage of any updates you make to to package or get from an `git pull`.
