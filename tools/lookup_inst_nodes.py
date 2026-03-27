#!/usr/bin/env python

import sys

from lib import inst_header, inst_node, miasutil
from lib.miasmap import Miasmap


def main():
    print("Loading main.rs5...")
    main_rs5 = miasutil.load_rs5_file('main.rs5')
    inst_header_obj = inst_header.open_inst_header_from_rs5(main_rs5)

    inst_node_indices = [idx for _, idx, _ in inst_node.iterate_over_inods(main_rs5)]

    (x, y) = list(map(float, sys.argv[1:3]))
    map_obj = Miasmap()

    # Rotate coord 90 degrees clockwise (transpose then mirror x):
    (x, y) = (inst_header.width - y, x)
    print('Rotated back to inst coordinates: %d x %d' % (x, y))
    map_obj.plot_point(x, y, (255, 255, 255), (230, 230, 230))

    for (n, (x1, y1, z1, x2, y2, z2)) in inst_header.get_points(inst_header_obj):
        assert x2 > x1
        assert y2 > y1
        if x >= int(x1) and x <= int(x2) and \
                y >= int(y1) and y <= int(y2):
            c = r = ''
            exists = 64
            if n not in inst_node_indices:
                c = '\x1b[31m'
                r = '\x1b[0m'
                exists = 0
            print(
                '%sinst_node%-6d | %8.3f %8.3f %9.3f  x  %8.3f %8.3f %8.3f  | '
                ' %4.0f x %-4.0f%s' % \
                (c, n, x1, y1, z1, x2, y2, z2, x2 - x1, y2 - y1, r))
            map_obj.plot_node(x1, y1, z1, x2, y2, z2, 128, 128, exists)
    map_obj.save_image('lookup_nodes.png')


if __name__ == '__main__':
    main()

# vi:noexpandtab:sw=8:ts=8
