#!/usr/bin/env python

import os
import sys

import numpy as np

from PIL import Image

from lib import imag

MINZ = -1815
MAXZ = 1833

# The map is always square; this is used for both width and height.
SIZE = 4096

SCALE = 2

MAP_FILLEDIN_PATH = 'Map_FilledIn.png'


def add_and_clamp(target, add_arr):
    """
    Adds ``add_arr`` to ``target``. ``target`` must be a view of a Numpy
    array of the ``uint8`` data type, and therefore have a maximum value of 255.
    This function ensures the result of the addition does not overflow 255.

    Performs addition in place, so it's necessary for ``target`` to be a view.
    :param target: A view of the target Numpy array.
    :type target: np.ndarray
    :param add_arr: An array to add to ``target``.
    :type add_arr: np.ndarray
    """
    # todo: is it faster to do this, or just use a uint16?
    target += add_arr
    target[target < add_arr] = 255


def clamp_and_scale(val):
    """
    Scales a given value by SCALE, clamps it to the range [0, SIZE - 1],
    and converts it to an ``int16``.
    This converts a given number to map pixel coordinates.
    :param val: The value to clamp and scale.
    :type val: float
    :return: Clamped and scaled value.
    :rtype: np.int16
    """
    return max(0, min(np.int16(np.rint(val / SCALE)), SIZE - 1))


def np_interpolate_cols(c1, c2, length):
    """
    Constructs an array of colors forming a gradient between ``c1`` and ``c2``.
    :param c1: First color
    :type c1: np.ndarray
    :param c2: Second color
    :type c2: np.ndarray
    :param length: The length of the color gradient in pixels
    :type length: int
    :return: An array of colors representing the gradient between ``c1`` and ``c2``.
    :rtype: np.ndarray
    """
    return np.rint(np.repeat(np.reshape(np.arange(0, length) / length, (-1, 1)), 3, 1) * (c2 - c1) + c1).astype(np.uint8)

class Miasmap:
    """
    An image of the game's map, which can have points plotted on it.

    When initialized, attempts to load ``Map_FilledIn`` from ``main.rs5``.
    If this fails, the base image is blank.
    """

    def __init__(self, game_path=None):
        self.load_map(game_path)

    def load_map(self, game_path=None):
        if not os.path.isfile(MAP_FILLEDIN_PATH):
            self.image = imag.load_rs5file_imag("Map_FilledIn", (SIZE, SIZE),
                                                'RGB', game_path)
            print('Saving image...')
            self.image.save(MAP_FILLEDIN_PATH)
            self.image = self.image.rotate(270)
        else:
            try:
                self.image = Image.open(MAP_FILLEDIN_PATH).rotate(270).resize(
                    (SIZE, SIZE))
            except:
                import traceback
                print(f"Failed to load image {MAP_FILLEDIN_PATH}.")
                traceback.print_exc()
                self.image = Image.new('RGB', (SIZE, SIZE), (0, 0, 0))
        self.image = Image.eval(self.image, lambda x: x / 3)
        self.pix = np.array(self.image)

    def save_image(self, filename):
        print('Saving %s...' % filename, file=sys.stderr)
        self.image = Image.fromarray(self.pix)
        self.image.rotate(90).save(filename)

    def plot(self, x, y, col, additive=True):
        (r, g, b) = col
        x = max(0, min(x / SCALE, SIZE - 1))
        y = max(0, min(y / SCALE, SIZE - 1))

        if additive:
            (r1, g1, b1) = self.pix[x, y]
            self.pix[x, y] = (r1 + r, g1 + g, b1 + b)
        else:
            self.pix[x, y] = (r, g, b)

    def plot_rect(self, in_x1, in_y1, c1, in_x2, in_y2, c2):
        """
        Plots a rectangle outline between corners ``[x1,y1]`` and ``[x2,y2]``.
        The outline has a color gradient between the two provided colors.
        This function always uses additive blending.
        :param in_x1: X coordinate of the first corner
        :type in_x1: float
        :param in_y1: Y coordinate of the first corner
        :type in_y1: float
        :param c1: Color of the first corner
        :type c1: list
        :param in_x2: X coordinate of the second corner
        :type in_x2: float
        :param in_y2: Y coordinate of the second corner
        :type in_y2: float
        :param c2: Color of the second corner
        :type c2: list
        """
        # uint16 here so the average calculates correctly
        c1 = np.array(c1, dtype=np.uint16)
        c2 = np.array(c2, dtype=np.uint16)

        # Average of the two colors
        midpoint_col = (c1 + c2) * 0.5

        # Swap the input "x" and "y" coordinates here to respect the
        # PIL -> Numpy conversion
        # (TODO: fix the other plot functions to also respect this)
        x1 = clamp_and_scale(in_y1)
        y1 = clamp_and_scale(in_x1)
        x2 = clamp_and_scale(in_y2)
        y2 = clamp_and_scale(in_x2)

        add_and_clamp(self.pix[x1, y1:y2 + 1],
                      np_interpolate_cols(c2, midpoint_col, abs(y1 - (y2 + 1))))
        add_and_clamp(self.pix[x2, y1:y2 + 1],
                      np_interpolate_cols(midpoint_col, c1, abs(y1 - (y2 + 1))))

        add_and_clamp(self.pix[(x1 + 1):x2, y1],
                      np_interpolate_cols(c2, midpoint_col, abs(x1 + 1 - x2)))
        add_and_clamp(self.pix[(x1 + 1):x2, y2],
                      np_interpolate_cols(midpoint_col, c1, abs(x1 + 1 - x2)))

    def plot_point(self, x, y, rgb1=(255, 255, 255), rgb2=(192, 192, 192)):
        self.plot(x, y, rgb1)
        for (xx, yy) in ((x - 1 * SCALE, y), (x + 1 * SCALE, y),
                         (x, y - 1 * SCALE),
                         (x, y + 1 * SCALE)):
            self.plot(xx, yy, rgb2)

    def plot_cross(self, x, y, d=20, rgb=(255, 255, 255)):
        for (x1, y1) in zip(list(range(x - d, x + d)),
                            list(range(y - d, y + d))):
            self.plot(x1, y1, rgb)
        for (x1, y1) in zip(reversed(list(range(x - d, x + d))),
                            list(range(y - d, y + d))):
            self.plot(x1, y1, rgb)

    def plot_square(self, x, y, d=20, rgb=[255, 255, 255], additive=True):
        """
        Plots a square of width ``2d`` and color ``rgb`` at coordinates ``(x,y)``.
        :param x: X coordinate of the center of the square.
        :type x: float
        :param y: Y coordinate of the center of the square.
        :type y: float
        :param d: One half the width of the square, in map units.
        :type d: int
        :param rgb: The color of the square.
        :type rgb: list
        :param additive: Whether additive blending should be used.
        :type additive: bool
        """
        rgb = np.array(rgb, dtype=np.uint8)
        # Swap the input "x" and "y" coordinates here to respect the
        # PIL -> Numpy conversion
        x1 = clamp_and_scale(y - d)
        x2 = clamp_and_scale(y + d)
        y1 = clamp_and_scale(x - d)
        y2 = clamp_and_scale(x + d)
        if additive:
            add_and_clamp(self.pix[x1:x2, y1:y2], rgb)
        else:
            self.pix[x1:x2, y1:y2] = rgb

    def plot_node(self, x1, y1, z1, x2, y2, z2, r=64, wierd=8, exists=64):
        l1 = np.rint((z1 - MINZ) * 255.0 / (MAXZ - MINZ))
        l2 = np.rint((z2 - MINZ) * 255.0 / (MAXZ - MINZ))

        if z1 == 10000000.0 or z2 == -1000000.0:
            rgb1 = rgb2 = [0, 0, wierd]
        elif exists:
            rgb1 = [exists, l1, 0]
            rgb2 = [exists, l2, 0]
        else:
            rgb1 = [r, 0, 0]
            rgb2 = [r, 0, 0]

        self.plot_rect(np.rint(x1), np.rint(y1), rgb1, np.rint(x2), np.rint(y2),
                       rgb2)

# vi:noexpandtab:sw=8:ts=8
