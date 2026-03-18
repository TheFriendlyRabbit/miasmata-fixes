#!/usr/bin/env python

import io
import math

import numpy as np
from PIL import Image

import rs5file


def open_cterr_hmap_from_rs5(main_rs5):
    """
    Retrieves ``cterr_hmap`` from the provided ``main.rs5``, as an array of
    floats.
    :param main_rs5: ``Rs5ArchiveDecoder`` for ``main.rs5``.
    :type main_rs5: ``Rs5ArchiveDecoder``
    :return: ``np.ndarray`` of floats representing height values.
    :rtype: np.ndarray
    """
    f = io.BytesIO(main_rs5['cterr_hmap'].decompress())
    (magic, filename, filesize, u2) = rs5file.parse_rs5file_header(f)
    assert magic == b'RAW.'
    assert filename == 'cterr_hmap'
    assert u2 == 0
    w = h = int(math.sqrt(filesize / 4))
    heights = np.frombuffer(f.read(4 * w * h), dtype='f').reshape(w,h).transpose()
    return heights


def hmap_to_image(main_rs5):
    """
    Exports ``cterr_hmap`` from the provided ``main.rs5`` as an image.
    :param main_rs5: ``Rs5ArchiveDecoder`` for ``main.rs5``.
    :type main_rs5: ``Rs5ArchiveDecoder``
    :return: ``PIL.Image`` object containing the image data
    :rtype: PIL.Image
    """
    mx = 255       # Max "normal" height (excluding orbital launch site)
    mn = -255      # Min "normal" height (excluding some very deep ocean areas)

    mn2 = -32      # Cutoff point for green values
    mn3 = -187     # Bottom of the ocean?

    # Abnormal values - we only normalize against these when the data is
    # outside the normal range (-255 to 255).
    abs_mn = -2047.8125     # Lowest value in the map data
    abs_mx = 1967.375       # Highest value in the map data

    heights = open_cterr_hmap_from_rs5(main_rs5)
    land_mask = heights > 0  # Everything above sea level
    over_max_mask = heights > mx  # Points that are too high (e.g. launch site)
    under_min_mask = heights < mn  # Points that are abnormally low
    bad_mask = np.logical_or(over_max_mask, under_min_mask) # All invalid points
    mn3_mask = heights <= mn3

    # Values normalized against the absolute max or min
    abs_normal = np.where(over_max_mask, heights * 255 / abs_mx, heights * 255 / abs_mn)

    # Red channel:
    # Above water level, red is the height of the terrain.
    # Below water level, red is zero.
    # EXCEPT at bad height values, where red is either normalized against the
    # overall max and min values, or, if greater than mn but less than mn3, is 128.
    red = np.where(land_mask, heights, 0)
    red = np.where(mn3_mask, 128, red)
    red = np.where(bad_mask, abs_normal, red) # Normalize bad values

    # Green channel:
    # Above water level, green is the height of the terrain, except where bad.
    # Below water level, green is the proximity of underwater land to the
    # surface, with mn2 as the zero level, except where the height is <= mn3
    # but greater than mn, in which case it's 128.
    green = np.where(land_mask, heights, (255 - (heights * 255 / mn2)) / 2)
    green = np.where(mn3_mask, 128, green)
    green = np.where(bad_mask, 0, green)
    green = np.clip(green, 0, 255) # Clip below mn2

    # Blue channel:
    # Above water level, blue is the height of the terrain.
    # Below water level, it's the depth of the ocean.
    blue = np.where(land_mask, heights, 255 + heights)
    blue = np.where(bad_mask, 0, blue)  # Mask out bad values

    img_cols = np.dstack((red,green,blue)).astype(np.uint8)
    export_img = Image.fromarray(img_cols)
    return export_img.transpose(Image.FLIP_TOP_BOTTOM)


# vi:noexpandtab:sw=8:ts=8
