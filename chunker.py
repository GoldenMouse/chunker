#!/usr/bin/python3

import os
import sys
import argparse


def chunk_file(filename, dirname, chunk_size):
    '''
        reads in file and creates chunks in dirname of chunk_size
    '''
    basename = os.path.splitext(filename)[0]

    with open(filename) as rh:
        chunk = rh.read(chunk_size)
        filecount = 1
        while chunk:
            chunk_name = '{0}-{1}.chunk'.format(basename, filecount)
            chunk_file = os.path.join(dirname, chunk_name)

            # check if broken word
            diff = check_broken_word(chunk, rh)
            if diff:
                chunk = chunk[:diff]
            
            with open(chunk_file, 'w') as wh:
                wh.write(chunk)

            chunk = rh.read(chunk_size)
            filecount += 1


def check_broken_word(chunk, fh):
    ''' 
        Checks if end of chunk is a broken word. 
        Broken means if current character is alphnumeric and next word is alphanumeric. 
        If broken, move the file pointer to beginning of word.
    '''
    start_pos = fh.tell()
    current_char = chunk[-1]
    next_char = fh.read(1)
    diff = 0

    if current_char.isalnum() and next_char.isalnum():
        while current_char.isalnum():
            fh.seek(fh.tell() - 2, os.SEEK_SET)
            current_char = fh.read(1)
        diff = fh.tell() - start_pos
    else:
      # move back to original position
      fh.seek(start_pos)

    return diff
  

def parser():
    parser = argparse.ArgumentParser()

    parser.add_argument( "filename",
        help="The name of the file you wish to chunk.")

    parser.add_argument( "--size",
        type=int,
        default=100,
        help='''Default is 100 bytes.
             The size, in bytes, of chunks that the file will be split into.''')

    return parser


if __name__ == "__main__":

    args = parser().parse_args()
    filename = args.filename
    size = args.size

    # avoids infinite loop
    if size < 10:
      sys.exit('Size too small. Please enter larger size')

    # create dir to hold chunk files
    basename = os.path.splitext(filename)[0]
    dirname = basename + '-chunks'
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    else:
        sys.exit('Directory already exists! Exiting.')

    chunk_file(filename, dirname, size)



