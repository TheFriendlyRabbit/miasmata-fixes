#!/usr/bin/env python

"""
Functions for decoding SMAP type files, and overlaying them on the game map
image.
(The only known SMAP file is ``player_map_achievements``, which encodes the
shoreline data for the achievement "The Bored Cartographer".
"""

from PIL import Image

from lib import rs5file

from lib.miasmap import Miasmap


def smap_iter(f, width=1024):
    """
    Generator. Yields tuples of coordinates which are encoded in the provided
    shoreline data.
    :param f: ``Rs5ChunkedFileDecoder`` for a decompressed ``SMAP`` chunk.
    :type f: ``Rs5ChunkedFileDecoder``
    :param width: Width of the shoreline data. Presumably always 1024?
    :type width: ``int``
    """
    smap = f['SMAP'].data
    offset = 0
    for inc in smap:
        offset += inc
        if inc < 0xff:
            yield (offset % width, offset / width)


def smap_to_image(main_rs5, smap):
    """
    Overlays ``SMAP`` data onto the map of the island.
    :param main_rs5: ``Rs5ArchiveDecoder`` for ``main.rs5``.
    :type main_rs5: ``Rs5ArchiveDecoder``
    :param smap: The ``SMAP`` to be overlaid.
    :type smap: str
    :return: ``PIL.Image`` object containing the image data
    :rtype: ``PIL.Image``
    """
    map_img = Miasmap()
    img_out = map_img.image.resize((1024, 1024)).rotate(90)
    img_out = Image.eval(img_out, lambda x: x / 8)
    pix = img_out.load()

    shoreline = rs5file.Rs5ChunkedFileDecoder(main_rs5[smap].decompress())

    for (x, y) in smap_iter(shoreline):
        pix[x, y] = (255, 255, 255)

    return img_out


# vi:noexpandtab:sw=8:ts=8
