#!/usr/bin/env python

import os
import sys

from PIL import Image

from lib import imag

MINZ = -1815
MAXZ = 1833

WIDTH = 4096
HEIGHT = 4096
SCALE = 2

MAP_FILLEDIN_PATH = 'Map_FilledIn.png'

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
            self.image = imag.load_rs5file_imag("Map_FilledIn", (1024, 1024), 'RGB', game_path)
            print('Saving image...')
            self.image.save(MAP_FILLEDIN_PATH)
        else:
            try:
                self.image = Image.open(MAP_FILLEDIN_PATH).rotate(270).resize((WIDTH, HEIGHT))
            except:
                import traceback
                print(f"Failed to load image {MAP_FILLEDIN_PATH}.")
                traceback.print_exc()
                self.image = Image.new('RGB', (WIDTH, HEIGHT), (0, 0, 0))
        self.image = Image.eval(self.image, lambda x: x / 3)
        self.pix = self.image.load()


    def save_image(self, filename):
        print('Saving %s...' % filename, file=sys.stderr)
        self.image.rotate(90).save(filename)


    def plot(self, x, y, col, additive=True):
        (r, g, b) = col
        x = max(0, min(x / SCALE, WIDTH - 1))
        y = max(0, min(y / SCALE, HEIGHT - 1))

        if additive:
            (r1, g1, b1) = self.pix[x, y]
            self.pix[x, y] = (r1 + r, g1 + g, b1 + b)
        else:
            self.pix[x, y] = (r, g, b)


    def plot_rect(self, x1, y1, c1, x2, y2, c2):
        xr = x2 - x1
        yr = y2 - y1

        def interpolate(p):
            return [int(p * v1 + (1.0 - p) * v2) for (v1, v2) in zip(c1, c2)]

        for x in range(x1, x2 + 1, SCALE):
            p = float(x - x1) / xr
            p1 = p / 2.0
            p2 = p1 + 0.5
            rgb1 = interpolate(p1)
            rgb2 = interpolate(p2)
            self.plot(x, y1, rgb1)
            self.plot(x, y2, rgb2)
        for y in range(y1 + 1, y2, SCALE):
            p = float(y - y1) / yr
            p1 = p / 2.0
            p2 = p1 + 0.5
            rgb1 = interpolate(p1)
            rgb2 = interpolate(p2)
            self.plot(x1, y, rgb1)
            self.plot(x2, y, rgb2)


    def plot_point(self, x, y, rgb1=(255, 255, 255), rgb2=(192, 192, 192)):
        self.plot(x, y, rgb1)
        for (xx, yy) in ((x - 1 * SCALE, y), (x + 1 * SCALE, y), (x, y - 1 * SCALE),
                         (x, y + 1 * SCALE)):
            self.plot(xx, yy, rgb2)


    def plot_cross(self, x, y, d=20, rgb=(255, 255, 255)):
        for (x1, y1) in zip(list(range(x - d, x + d)), list(range(y - d, y + d))):
            self.plot(x1, y1, rgb)
        for (x1, y1) in zip(reversed(list(range(x - d, x + d))),
                            list(range(y - d, y + d))):
            self.plot(x1, y1, rgb)


    def plot_square(self, x, y, d=20, rgb=(255, 255, 255), additive=True):
        for y1 in range(y - d, y + d, SCALE):
            for x1 in range(x - d, x + d, SCALE):
                self.plot(x1, y1, rgb, additive)

    def plot_node(self, x1, y1, z1, x2, y2, z2, r=64, wierd=8, exists=64):
        l1 = int((z1 - MINZ) * 255.0 / (MAXZ - MINZ))
        l2 = int((z2 - MINZ) * 255.0 / (MAXZ - MINZ))

        if z1 == 10000000.0 or z2 == -1000000.0:
            rgb1 = rgb2 = (0, 0, wierd)
        elif exists:
            rgb1 = (exists, l1, 0)
            rgb2 = (exists, l2, 0)
        else:
            rgb1 = (r, 0, 0)
            rgb2 = (r, 0, 0)

        self.plot_rect(int(x1), int(y1), rgb1, int(x2), int(y2), rgb2)

# vi:noexpandtab:sw=8:ts=8
