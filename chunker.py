#!/usr/bin/python

import os
import sys
import argparse


def chunk_file(filename, chunk_size):
    basename = os.path.splitext(filename)[0]

    # create dir to hold chunk files
    dirname = basename + '-chunks'
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    else:
        sys.exit('Directory already exists! Exiting.')

    with open(filename) as rh:
        line = rh.read(chunk_size)

        count = 1
        while line:
            chunk_name = '{0}-{1:02}.chunk'.format(basename, count)
            chunk_file = os.path.join(dirname, chunk_name)

            with open(chunk_file, 'w') as wh:
                wh.write(line)

            line = rh.read(chunk_size)
            count += 1


def parser():
    parser = argparse.ArgumentParser()

    parser.add_argument( "filename",
        help="The fullpath name of the file you wish to chunk.")

    parser.add_argument( "--size",
        type=int,
        default=100,
        help='''Default is 100 bytes.
             The size in byte of chunks that the file will be split into.''')

    return parser


if __name__ == "__main__":

    args = parser().parse_args()
    chunk_file(args.filename, args.size)
