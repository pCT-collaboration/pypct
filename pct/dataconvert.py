#!/usr/bin/env python
"""
dataconvert.py

Convert pCT scan data between formats.
"""

import struct
import argparse
import glob
import os, errno
import time
import sys

class Data(object):
    '''Basic data container.'''
    pass

def readFile(filename):
    print 'Reading data from file:', filename
    root, ext = os.path.splitext(filename)
    if ext == '.bin':
        with open(filename, 'rb') as f:
            magic_number, = struct.unpack('4s', f.read(4))
            if magic_number != 'PCTD':
                raise Exception('Unknown data format')
            
            version_id, = struct.unpack('i', f.read(4))
            print 'File contains data in version %d format' % version_id
            data = loadData(f, version_id)
    
    elif ext == '.dat':
        raise Exception('Reading of old binary files is not yet implemented.')
    
    elif ext == '.txt':
        raise Exception('Reading of old text files is not yet implemented.')
    
    return data

def loadData(f, version_id):
    if version_id == 0:
        return loadData_v0(f)
    else:
        raise Exception('Unknown data format version')

def loadData_v0(f):
    data = Data()
    
    data.num_events, = struct.unpack('i', f.read(4))
    print 'Found %d events' % data.num_events
    
    data.projection_angle, data.beam_energy = struct.unpack('ff', f.read(8))
    print 'Projection angle:', data.projection_angle
    print 'Beam energy:', data.beam_energy
    
    data.generation_date, data.preprocess_date = struct.unpack('ii', f.read(8))
    data.generation_date = time.localtime(data.generation_date)
    data.preprocess_date = time.localtime(data.preprocess_date)
    print 'Generation date:', time.strftime('%Y-%m-%d', data.generation_date)
    print 'Preprocess date:', time.strftime('%Y-%m-%d', data.preprocess_date)
    
    length, = struct.unpack('i', f.read(4))
    data.phantom_name, = struct.unpack('%ds' % length, f.read(length))
    print 'Phantom name:', data.phantom_name
    
    length, = struct.unpack('i', f.read(4))
    data.data_source, = struct.unpack('%ds' % length, f.read(length))
    print 'Data source:', data.data_source
    
    length, = struct.unpack('i', f.read(4))
    data.prepared_by, = struct.unpack('%ds' % length, f.read(length))
    print 'Prepared by:', data.prepared_by
    
    length = 4 * data.num_events
    
    data.t = []
    data.t.append(struct.unpack('%df' % data.num_events, f.read(length)))
    data.t.append(struct.unpack('%df' % data.num_events, f.read(length)))
    data.t.append(struct.unpack('%df' % data.num_events, f.read(length)))
    data.t.append(struct.unpack('%df' % data.num_events, f.read(length)))
    
    data.v = []
    data.v.append(struct.unpack('%df' % data.num_events, f.read(length)))
    data.v.append(struct.unpack('%df' % data.num_events, f.read(length)))
    data.v.append(struct.unpack('%df' % data.num_events, f.read(length)))
    data.v.append(struct.unpack('%df' % data.num_events, f.read(length)))
    
    data.u = []
    data.u.append(struct.unpack('%df' % data.num_events, f.read(length)))
    data.u.append(struct.unpack('%df' % data.num_events, f.read(length)))
    data.u.append(struct.unpack('%df' % data.num_events, f.read(length)))
    data.u.append(struct.unpack('%df' % data.num_events, f.read(length)))
    
    data.wepl = struct.unpack('%df' % data.num_events, f.read(length))
    
    print 'First event:'
    for i in range(4):
        print '%f %f %f' % (data.t[i][0], data.v[i][0], data.u[i][0])
    print '%f' % data.wepl[0]
    
    return data

def writeTextFile(filename, data, max=None):
    print 'Writing data to text file:', filename
    raise Exception('Writing text files is not yet implemented.')

def writeOldBinaryFile(filename, data, max=None):
    print 'Writing data to old format binary file:', filename
    
    if max is None:
        num_events = data.num_events
    else:
        num_events = min(data.num_events, max)
        print 'Limiting output to %d events' % num_events
    
    # create the u-coordinate look-up table
    u_coords = []
    for i in range(4):
        u_set = list(set(data.u[i]))
        if len(u_set) != 2:
            if len(u_set) > 2:
                raise Exception('Error converting u-coordinate arrays to look-up table')
            elif len(u_set) == 1:
                u_set *= 2
        u_coords.extend(u_set)
    
    config_filename = os.path.join(os.path.dirname(filename), 'scan.cfg')
    with open(config_filename, 'w') as f:
        for i in range(8):
            f.write('%f\n' % u_coords[i])
    
    with open(filename, 'wb') as f:
        for i in range(num_events):
            data_word = []
            for n in range(4):
                f.write(struct.pack('f', data.v[n][i]))
            for n in range(4):
                f.write(struct.pack('f', data.t[n][i]))
            for n in range(4):
                f.write(struct.pack('B', u_coords.index(data.u[n][i])))
            f.write(struct.pack('ffI', data.wepl[i], data.projection_angle, 0)) # last int is a dummy for alignment
    
    print 'Done writing to file'
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert pCT scan data between formats')
    parser.add_argument('-t', '--text', dest='text', action='store_true', default=False, help='Output to text format (default is binary)')
    parser.add_argument('-v', dest='version', type=int, help='Update to VERSION (default is to downgrade)')
    parser.add_argument('-m', '--max', type=int, help='Maximum number of histories per projection to output')
    parser.add_argument('inputdir', help='Input directory')
    parser.add_argument('outputdir', help='Output directory')
    
    args = parser.parse_args()
    
    print 'Input directory:', args.inputdir
    file_types = 0
    
    new_filelist = glob.glob(os.path.join(args.inputdir, '*.bin'))
    if len(new_filelist) > 0:
        file_types += 1
        print 'Found %d file%s in the new format' % (len(new_filelist), '' if len(new_filelist) == 1 else 's')
        
    old_binary_filelist = glob.glob(os.path.join(args.inputdir, '*.dat'))
    if len(old_binary_filelist) > 0:
        file_types += 1
        print 'Found %d file%s in the old binary format' % (len(old_binary_filelist), '' if len(old_binary_filelist) == 1 else 's')
        
    old_text_filelist = glob.glob(os.path.join(args.inputdir, '*.txt'))
    if len(old_text_filelist) > 0:
        file_types += 1
        print 'Found %d file%s in the old text format' % (len(old_text_filelist), '' if len(old_text_filelist) == 1 else 's')
    
    if file_types == 0:
        raise Exception('No pCT data files found!')
    elif file_types > 1:
        print '-> More than one file type found.'
        print 'Which type should be used for input?'
        
        choices = []
        if len(new_filelist) > 0:
            choices.append('New files')
        if len(old_binary_filelist) > 0:
            choices.append('Old binary files')
        if len(old_text_filelist) > 0:
            choices.append('Old text files')
        
        inputs = [str(i+1) for i in range(len(choices))]
        inputs.extend(['a', 'q'])
        
        for i, choice in enumerate(inputs):
            try:
                choice_name = choices[i]
            except IndexError:
                if choice == 'a':
                    choice_name = 'All'
                if choice == 'q':
                    choice_name = 'Quit'
            print '%s) %s' % (choice, choice_name)
        
        user_input = ''
        while user_input not in inputs:
            user_input = raw_input('--> ')
            user_input.lower()
        
        if user_input == 'q':
            sys.exit()
        if user_input == 'a':
            filelist = new_filelist + old_binary_filelist + old_text_filelist
        else:
            filelist = [new_filelist, old_binary_filelist, old_text_filelist]
            filelist = filelist[int(user_input) - 1]
    else:
        # only one file type found, so the other lists are just empty 
        # (and it won't hurt to join them together)
        filelist = new_filelist + old_binary_filelist + old_text_filelist
        
    print 'Output directory:', args.outputdir
    try: 
        os.mkdir(args.outputdir)
    except OSError as e: 
        if e.errno == errno.EEXIST:
            pass 
        else:
            raise
    
    for filename in filelist:
        data = readFile(filename)
        filename = os.path.join(args.outputdir, os.path.basename(filename))
        if args.version is None:
            filename, ext = os.path.splitext(filename)
            if args.text:
                filename += '.txt'
                writeTextFile(filename, data, args.max)
            else:
                filename += '.dat'
                writeOldBinaryFile(filename, data, args.max)
        else:
            raise Exception('Writing to new data formats is not yet implemented.')
        print
    
    print 'Done'
