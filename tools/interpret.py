#!/usr/bin/env python

import struct
import sys


def main():
    with open(sys.argv[1], 'r') as f:
        fmt = sys.argv[2]
        size = struct.calcsize(fmt)
        while True:
            d = f.read(size)
            if len(d) < size:
                rem = [c.encode('hex_codec') for c in d]
                print()
                print(' '.join(['--'] * len(rem)))
                print(' '.join(rem))
                return
            print('\t'.join(map(str, struct.unpack(fmt, d))))


if __name__ == '__main__':
    main()

# vi:noexpandtab:sw=8:ts=8
