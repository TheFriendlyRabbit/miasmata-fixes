#!/usr/bin/env python

from lib import miasutil, cterr_hmap


def extract_all():
    """
    Exports various data from ``main.rs5`` to human-readable formats.
    """
    main_rs5 = miasutil.load_rs5_file('main.rs5')
    cterr_hmap.hmap_to_image(main_rs5).save('cterr_hmap.png')


if __name__ == '__main__':
    extract_all()

# vi:noexpandtab:sw=8:ts=8