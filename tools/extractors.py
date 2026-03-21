#!/usr/bin/env python
"""
Extracts a variety of assets from the game into human-readable formats:
- Exports the game's height map, ``cterr_hmap``, as an image (``cterr_hmap.png``)
- Exports island's shoreline overlaid on top of the game's map (``smap_out.png``)
"""

from lib import imag, miasutil, cterr_hmap, smap


def extract_all():
    """
    Exports various data from ``main.rs5`` to human-readable formats.
    """
    print("Loading main.rs5...")
    main_rs5 = miasutil.load_rs5_file('main.rs5')
    print("Extracting images...")
    imag.load_rs5file_imag("Map_FilledIn", mode='RGB', archive=main_rs5).save("Map_FilledIn.png")
    imag.load_rs5file_imag("Coulise_Leafy1Transparent", mode='RGBA', archive=main_rs5).save("alpha_test.png")
    print("Extracting height map...")
    cterr_hmap.hmap_to_image(main_rs5).save('cterr_hmap.png')
    # It seems that player_map_achievements is the only SMAP file in the game.
    print("Extracting shoreline...")
    smap.smap_to_image(main_rs5, 'player_map_achievements').save('smap_out.png')


if __name__ == '__main__':
    extract_all()

# vi:noexpandtab:sw=8:ts=8
