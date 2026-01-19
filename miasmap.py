#!/usr/bin/env python

import os
import sys

from PIL import Image

import imag
import miasutil
import rs5archive
import rs5file

MINZ = -1815
MAXZ = 1833

WIDTH = 4096
HEIGHT = 4096
SCALE = 2

MAP_FILLEDIN_PATH = 'Map_FilledIn.jpg'

if not os.path.isfile(MAP_FILLEDIN_PATH):
    imag.extract_map_filledin()
    MAP_FILLEDIN_PATH = os.path.join(os.path.dirname(__file__),
                                     MAP_FILLEDIN_PATH)
try:
    image = Image.open(MAP_FILLEDIN_PATH).rotate(270).resize((WIDTH, HEIGHT))
except:
    import traceback

    traceback.print_exc()
    image = Image.new('RGB', (WIDTH, HEIGHT), (0, 0, 0))
image = Image.eval(image, lambda x: x / 3)
pix = image.load()


def save_image(filename):
    print('Saving %s...' % filename, file=sys.stderr)
    image.rotate(90).save(filename)


def plot(x, y, xxx_todo_changeme, additive=True):
    (r, g, b) = xxx_todo_changeme
    x = max(0, min(x / SCALE, WIDTH - 1))
    y = max(0, min(y / SCALE, HEIGHT - 1))

    if additive:
        (r1, g1, b1) = pix[x, y]
        pix[x, y] = (r1 + r, g1 + g, b1 + b)
    else:
        pix[x, y] = (r, g, b)


def plot_rect(x1, y1, c1, x2, y2, c2):
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
        plot(x, y1, rgb1)
        plot(x, y2, rgb2)
    for y in range(y1 + 1, y2, SCALE):
        p = float(y - y1) / yr
        p1 = p / 2.0
        p2 = p1 + 0.5
        rgb1 = interpolate(p1)
        rgb2 = interpolate(p2)
        plot(x1, y, rgb1)
        plot(x2, y, rgb2)


def plot_point(x, y, rgb1=(255, 255, 255), rgb2=(192, 192, 192)):
    plot(x, y, rgb1)
    for (xx, yy) in ((x - 1 * SCALE, y), (x + 1 * SCALE, y), (x, y - 1 * SCALE),
                     (x, y + 1 * SCALE)):
        plot(xx, yy, rgb2)


def plot_cross(x, y, d=20, rgb=(255, 255, 255)):
    for (x1, y1) in zip(list(range(x - d, x + d)), list(range(y - d, y + d))):
        plot(x1, y1, rgb)
    for (x1, y1) in zip(reversed(list(range(x - d, x + d))),
                        list(range(y - d, y + d))):
        plot(x1, y1, rgb)


def plot_square(x, y, d=20, rgb=(255, 255, 255), additive=True):
    for y1 in range(y - d, y + d, SCALE):
        for x1 in range(x - d, x + d, SCALE):
            plot(x1, y1, rgb, additive)

# vi:noexpandtab:sw=8:ts=8
