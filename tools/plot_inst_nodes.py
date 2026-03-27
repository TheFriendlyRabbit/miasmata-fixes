#!/usr/bin/env python

from lib import miasmap, miasutil, inst_header, inst_node


def main():
    map_obj = miasmap.Miasmap()
    main_rs5 = miasutil.load_rs5_file('main.rs5')
    inst_header_obj = inst_header.open_inst_header_from_rs5(main_rs5)
    nodes = [idx for _, idx, _ in inst_node.iterate_over_inods(main_rs5)]
    for (n, (x1, y1, z1, x2, y2, z2)) in inst_header.get_points(inst_header_obj):
        if n % 1000 == 0:
            print(n, '...')

        # def fmt_flt(f):
        #	return '%f' % f
        # print '\t'.join(map(fmt_flt, (x, y, z)))

        # if z1 == 10000000.0 or z2 == -1000000.0:
        # 	assert(not os.path.exists('nodes/inst_node%d' % n))

        # if not os.path.exists('nodes/inst_node%d' % n):
        #	continue
        if not n in nodes:
            continue

        map_obj.plot_node(x1, y1, z1, x2, y2, z2)
    map_obj.save_image('all_nodes_exists.png')


if __name__ == '__main__':
    main()

# vi:noexpandtab:sw=8:ts=8
