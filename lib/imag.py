#!/usr/bin/env python

import struct

import numpy as np
from PIL import Image

from lib import miasutil, rs5file


# Documentation:
# https://en.wikipedia.org/wiki/S3_Texture_Compression
# http://msdn.microsoft.com/en-us/library/windows/desktop/bb943991(v=vs.85).aspx

class DDSPixelFormat():
    # http://msdn.microsoft.com/en-us/library/windows/desktop/bb943984(v=vs.85).aspx
    class Flags:
        ALPHAPIXELS = 0x00001
        ALPHA = 0x00002
        FOURCC = 0x00004
        RGB = 0x00040
        YUV = 0x00200
        LUMINANCE = 0x20000

    def __init__(self, fp):
        (
            size,
            self.flags,
            four_cc,
            rgb_bit_count,
            r_bit_mask,
            g_bit_mask,
            b_bit_mask,
            a_bit_mask
        ) = struct.unpack('<2I 4s 5I', fp.read(32))

        assert size == 32
        if self.flags & self.Flags.ALPHAPIXELS:  # uncompressed
            self.a_bit_mask = a_bit_mask
        assert not self.flags & self.Flags.ALPHA  # old file
        if self.flags & self.Flags.FOURCC:
            self.four_cc = four_cc
        if self.flags & self.Flags.RGB:  # uncompressed
            self.rgb_bit_count = rgb_bit_count
            self.r_bit_mask = r_bit_mask
            self.g_bit_mask = g_bit_mask
            self.b_bit_mask = b_bit_mask
        assert not self.flags & self.Flags.YUV  # old file
        assert not self.flags & self.Flags.LUMINANCE  # old file


class DDSHeader:
    # http://msdn.microsoft.com/en-us/library/windows/desktop/bb943982(v=vs.85).aspx
    class Flags():
        # Note: Don't rely on these flags - not all writers set them
        CAPS = 0x000001
        HEIGHT = 0x000002
        WIDTH = 0x000004
        PITCH = 0x000008
        PIXELFORMAT = 0x001000
        MIPMAPCOUNT = 0x020000
        LINEARSIZE = 0x080000
        DEPTH = 0x800000
        REQUIRED = CAPS | HEIGHT | WIDTH | PIXELFORMAT

    def __init__(self, fp):
        (
            size,
            self.flags,
            self.height,
            self.width,
            self.pitch_or_linear_size,
            self.depth,
            self.mip_map_count
        ) = struct.unpack('<7I 44x', fp.read(72))
        self.pixel_format = DDSPixelFormat(fp)
        (
            self.caps,
            self.caps2,
            self.caps3,
            self.caps4
        ) = struct.unpack('<4I4x', fp.read(20))
        assert size == 124
        assert self.flags & self.Flags.REQUIRED == self.Flags.REQUIRED

BIT_SHIFT_ARR = np.array([0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30],dtype=np.uint8)
ALPHA_SHIFT_ARR = np.array([0, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45],dtype=np.uint8)

def open_dds(fp, mipmap=None, mode='RGBA'):
    if fp.read(4) != b'DDS ':
        raise ValueError('Not a DDS file')
    header = DDSHeader(fp)

    assert header.pixel_format.four_cc in (b'DXT5', b'DXT1')
    if header.pixel_format.four_cc == b'DXT1':
        block_size = 8
        fmt = [('c0', '<u2'), ('c1', '<u2'), ('clookup', '<u4')]
    else:
        block_size = 16
        fmt = [('alpha', '<u8'), ('c0', '<u2'), ('c1', '<u2'),
               ('clookup', '<u4')]

    # Base width and height of the image
    width, height = header.width, header.height

    # Number of 4x4 pixel squares along the height and width of the image
    h_count, w_count = height // 4, width // 4

    if mipmap:
        while mipmap < (width, height):
            fp.seek(width * height * block_size // 16, 1)
            (width, height) = (width // 2, height // 2)

    l = width * height // 16 * block_size
    buf = np.frombuffer(fp.read(l), fmt)

    def rgb565(c):
        r = (c & 0xf800) >> 8
        g = (c & 0x07e0) >> 3
        b = (c & 0x001f) << 3
        return np.dstack((r, g, b))

    c0 = buf['c0'].reshape([h_count, w_count])
    c1 = buf['c1'].reshape([h_count, w_count])
    ct = (c0 <= c1).reshape([h_count, w_count, 1])

    np_cols = np.empty([4, h_count, w_count, 3], np.uint16)
    np_cols[0] = rgb565(c0)
    np_cols[1] = rgb565(c1)
    np_cols[2] = np.choose(ct, ((2 * np_cols[0] + np_cols[1]) / 3, (np_cols[0] + np_cols[1]) / 2))
    np_cols[3] = np.choose(ct, ((np_cols[0] + 2 * np_cols[1]) / 3, 0))
    del ct
    cl = buf['clookup'].reshape([h_count, w_count, 1])

    channels = 3
    if header.pixel_format.four_cc == b'DXT5' and mode == 'RGBA':
        channels = 4
        alpha = buf['alpha'].reshape(h_count, w_count)
        a = np.empty([8, h_count, w_count], dtype=np.uint64)
        aa = np.empty([8, h_count, w_count], dtype=np.uint64)
        ab = np.empty([8, h_count, w_count], dtype=np.uint64)
        # Byte swapped due to reading in LE
        al = ((alpha & 0xffffffffffff0000) >> 16).reshape([h_count, w_count, 1])
        a[0] = alpha & 0xff
        a[1] = (alpha & 0xff00) >> 8
        at = a[0] <= a[1]
        for i in range(1, 7):
            aa[i + 1] = ((7 - i) * a[0] + i * a[1]) / 7
        for i in range(1, 5):
            ab[i + 1] = ((5 - i) * a[0] + i * a[1]) / 5
        ab[6] = np.zeros_like(a[0], dtype=np.uint64)
        ab[7] = np.full_like(a[0], 255, dtype=np.uint64)
        for i in range(2, 8):
            a[i] = np.choose(at, [aa[i], ab[i]])
        del aa, ab, at

    out = np.empty([height, width, channels], np.float64)

    # Parse the packed CLUT into a set of 16 2-bit color lookup tables,
    # then swap the lookup indices for actual colors via np.choose
    cl = np.choose((cl >> BIT_SHIFT_ARR & 0x3).transpose(2, 0, 1).reshape(16, h_count, w_count, 1), np_cols)

    # Do the same with the alpha lookup table, if present, and append the
    # alpha channel to the color array.
    if channels == 4:
        cl = np.insert(cl, 3, np.choose(np.uint8(al >> ALPHA_SHIFT_ARR & 0x7).transpose(2, 0, 1), a), 3)

    # Copy the pixels to the target image.
    # Envision a 4x4 pixel grid. Each of the following 16 iterations corresponds
    # to an x,y coordinate in that pixel grid. If that pixel grid is tiled
    # across the entire image, that represents the pixels which are filled
    # in each iteration of this loop.
    idx = 0
    for y in range(4):
        for x in range(4):
            out[y::4,x::4,:] = cl[idx]
            idx += 1

    # Finally cast to uint8 here - too early causes overflows in the DXT
    # calculations and any time after that actually slows things down
    image = Image.fromarray(np.array(out, np.uint8))
    return image


def open_rs5file_imag(file, mipmap=None, mode='RGBA'):
    return open_dds(file['DATA'].get_fp(), mipmap, mode)


def load_rs5file_imag(file, mipmap=None, mode='RGBA', rs5_dir=None, archive=None):
    """
    Loads a texture from main.rs5.
    :param file: The name of the texture to load (e.g. "Map_FilledIn" for the map)
    :ptype file: str
    :param mipmap: Mipmap of the texture to load (e.g. (1024, 1024) for the map)
    :ptype mipmap: int tuple
    :param mode: The color space of the texture. 'RGBA' or 'RGB'.
    :ptype mode: str
    :param rs5_dir: (optional) The directory for the rs5 file.
    :ptype rs5_dir: str
    :param archive: (optional) An already-loaded rs5 file.
    :ptype archive: ``Rs5ArchiveDecoder``
    :return: A PIL ``Image`` containing the loaded texture.
    :rtype: ``PIL.Image``
    """
    if not archive:
        print('Opening main.rs5...')
        archive = miasutil.load_rs5_file('main.rs5', rs5_dir)
    print(f'Extracting image {file}...')
    file_out = rs5file.Rs5ChunkedFileDecoder(archive[f'TEX\\{file}'].decompress())
    print(f'Decoding image {file}...')
    return open_rs5file_imag(file_out, mipmap, mode)


# vi:noexpandtab:sw=8:ts=8
