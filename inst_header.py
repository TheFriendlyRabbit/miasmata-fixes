#!/usr/bin/env python

import io
import struct

from lib import miasmap
import rs5file


def parse_inst_header_header(f):
    assert f.read(6) == b'\0\x47\0\0\0\x46'
    (nodes,) = struct.unpack('<I', f.read(4))
    return nodes


def get_points(f=None):
    if f is None:
        f = open('inst_header')
    rs5file.parse_raw_header(f)
    nodes = parse_inst_header_header(f)
    for i in range(nodes):
        yield (i, struct.unpack('<6f', f.read(4 * 6)))


def open_inst_header_from_rs5(main_rs5):
    decompressed = main_rs5['inst_header'].decompress()
    return io.BytesIO(decompressed)


def _get_name_list(f=None):
    if f is None:
        f = open('inst_header')
    filesize = rs5file.parse_raw_header(f)
    nodes = parse_inst_header_header(f)
    seek = nodes * 6 * 4
    f.seek(seek, 1)
    (num_entries,) = struct.unpack('<I', f.read(4))
    return f.read(filesize - 14 - seek).rstrip(b'\0').split(b'\0')


names = None


def get_name_list(f=None):
    global names
    if names is None:
        names = _get_name_list(f)
    for idx, val in enumerate(names):
        if not isinstance(val, str):
            names[idx] = val.decode('ascii')
    return names

# vi:noexpandtab:sw=8:ts=8
