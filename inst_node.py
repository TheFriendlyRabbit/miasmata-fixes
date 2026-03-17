#!/usr/bin/env python

import struct
import sys

from lib import inst_header


class Inod():
    def __init__(self, node_name, node_model_idx, u1, x, y, z, u2, rotz, u4, u5, u6):
        self.node_name = node_name # name of object- e.g. MushroomClump4a
        self.node_model_idx = node_model_idx # model index of object - e.g. 457 for plant4
        self.u1 = u1    # unique identifier?
        # Keep in mind that the node map is rotated 90 degrees before being
        # saved as an image file. X and Y are inverted from what you would
        # normally expect them to be, relative to the map.
        self.x = x          # position on up-down axis relative to in-game map
        self.y = y          # position on left-right axis relative to in-game map
        self.z = z          # position on 3D vertical axis
        self.u2 = u2        # float, seems to always be 0...??
        self.rotz = rotz    # z axis rotation in radians
        self.u4 = u4        # integer, seems to always be 0 or 258...??
        self.u5 = u5        # float value
        self.u6 = u6        # float value


def parse_inod_header(f):
    # Basically the same as the RAW. header, looks like this is a common
    # header format, so I should be able to refactor this. Need to confirm
    # if the padding after the filename is consistent with other headers.
    (magic, u1, filename_len, u2, filesize) = struct.unpack('<4s2sB1sI',
                                                            f.read(12))
    if magic != b'INOD':
        raise ValueError()
    assert (u1 == b'\0\0')
    assert (u2 == b'\0')
    filename = f.read(filename_len).rstrip(b'\0')
    # print>>sys.stderr, 'Parsing INOD %s...' % filename
    pad = (8 - ((12 + filename_len) % 8)) % 8
    # print>>sys.stderr, '%i bytes of padding' % pad
    assert (f.read(pad) == b'\0' * pad)
    (num_entries,) = struct.unpack('<I', f.read(4))
    # print>>sys.stderr, '%i entries' % num_entries
    assert (num_entries)
    return (filesize, num_entries)


def enc_inod_header(filename, filesize, num_entries):
    filename_len = len(filename) + 1
    r = struct.pack('<4s2sB1sI', b'INOD', b'\0\0', filename_len, b'\0', filesize)
    r += filename.encode("utf-8") + b'\0'
    pad = (8 - ((12 + filename_len) % 8)) % 8
    r += b'\0' * pad
    r += struct.pack('<I', num_entries)
    return r


def parse_inod(f, name_list=None):
    if name_list is None:
        name_list = inst_header.get_name_list()
    (filesize, num_entries) = parse_inod_header(f)
    for i in range(num_entries):
        (u1, idx, x, y, z, u2, u3, u4, u5, u6) = struct.unpack('<2I5fI2f',
                                                               f.read(4 * 10))
        yield Inod(name_list[idx], idx, u1, x, y, z, u2, u3, u4, u5, u6)
    assert (f.read(4) == b'\0' * 4)


def encode_inod(filename, entries):
    r = b''
    for node in entries:
        r += struct.pack('<2I5fI2f', node.u1, node.node_model_idx, node.x, node.y, node.z, node.u2, node.rotz, node.u4, node.u5, node.u6)
    r += b'\0' * 4
    h = enc_inod_header(filename, len(r), len(entries))
    return h + r


## Find all objects within a node:
# def main():
#	import miasmap
#	for filename in sys.argv[1:]:
#		f = open(filename, 'r')
#		for (name, idx, u1, x, y, z, u2, u3, u4, u5, u6) in parse_inod(f):
#			print '%26s (%.3i) %6i  (%8.3f %8.3f %7.3f)  %.1f %7.3f %3i %6.3f
#			%6.3f' % (name, idx, u1, x, y, z, u2, u3, u4, u5, u6)
#			miasmap.plot_square(int(x), int(y), 20, (128, 128, 128))
#	miasmap.save_image('node.jpg')

# Search for objects matching a pattern in all nodes:
def main():
    from lib import miasmap
    nodes = list(map(str.rstrip, open('inst_list', 'r').readlines()))
    filters = sys.argv[1:]
    colours = ((128, 0, 0), (0, 128, 0), (0, 0, 128), (128, 128, 0),
               (128, 0, 128), (0, 128, 128), (128, 128, 128))
    items = {}

    tmp = miasmap.image
    miasmap.image = tmp.copy()
    miasmap.pix = miasmap.image.load()

    for (i, filename) in enumerate(nodes):
        if i % 100 == 0:
            print('\r%i/%i' % (i, len(nodes)), end=' ', file=sys.stderr)
        f = open('nodes/' + filename, 'r')
        for (name, idx, u1, x, y, z, u2, u3, u4, u5, u6) in parse_inod(f):
            c = (128, 128, 128)
            if filters:
                for (i, f) in enumerate(filters):
                    if f in name:
                        c = colours[i % len(colours)]
                        break
                else:
                    continue
                print(
                    '\r%26s (%.3i) %6i  (%8.3f %8.3f %7.3f)  %.1f %7.3f %3i '
                    '%6.3f %6.3f' % (
                        name, idx, u1, x, y, z, u2,
                        u3, u4, u5, u6))
                miasmap.plot_square(int(x), int(y), 20, c)
            else:
                miasmap.plot_point(int(x), int(y))
                if name not in items:
                    items[name] = []
                items[name].append((int(x), int(y)))
    miasmap.save_image('item_locations.jpg')
    if not filters:
        for name in items:
            miasmap.image = tmp.copy()
            miasmap.pix = miasmap.image.load()
            for (x, y) in items[name]:
                miasmap.plot_square(x, y, 20, c)
            miasmap.save_image('itemmap/%s.jpg' % name)


if __name__ == '__main__':
    main()

# vi:noexpandtab:sw=8:ts=8
