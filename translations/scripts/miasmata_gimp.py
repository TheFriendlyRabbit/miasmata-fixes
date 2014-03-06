#!/usr/bin/env python

from gimpfu import *

def add_text_layer(image, txt, font, font_size, line_spacing = None, colour = (0, 0, 0), name = 'Text', pos = (0, 0)):
    gimp.set_foreground(*colour)
    pdb.gimp_image_set_active_layer(image, image.layers[0])
    text = pdb.gimp_text_fontname(image, None, pos[0], pos[1], txt, 0, True, font_size, PIXELS, font)
    text.name = name
    if line_spacing is not None:
        pdb.gimp_text_layer_set_line_spacing(text, line_spacing)
    pdb.gimp_text_layer_set_hint_style(text, TEXT_HINT_STYLE_NONE)

    return text

def bold_text(layer, txt):
    # XXX: Requires a patched GIMP to set text markup
    # See https://bugzilla.gnome.org/show_bug.cgi?id=724101
    markup = '<b>%s</b>' % txt
    pdb.gimp_text_layer_set_markup(layer, markup)

def bold_word_wrap(layer, text, width, start_tag='<b>', end_tag='</b>'):
    # This is a workaround for the lack of a fixed-width + dynamic-height
    # setting for text boxes in the GIMP - otherwise there is no easy way to
    # wrap the text AND have it vertically centered.
    words = text.split(' ')
    if not len(words):
        return
    txt = words[0]
    for word in words[1:]:
        txt1 = '%s %s' % (txt, word)
        markup = '%s%s%s' % (start_tag, txt1, end_tag)
        pdb.gimp_text_layer_set_markup(layer, markup)
        if layer.width > width:
            txt1 = '%s\n%s' % (txt, word)
            markup = '%s%s%s' % (start_tag, txt1, end_tag)
            pdb.gimp_text_layer_set_markup(layer, markup)
            width = max(width, layer.width)
        txt = txt1

def blur_layer(image, layer, radius = 1.0):
    pdb.plug_in_gauss_rle2(image, layer, radius, radius)

def save_dds(image, filename, alpha):
    alpha = alpha and 3 or 1
    try:
        pdb.file_dds_save(
                image,
                image.active_layer,
                filename, # filename
                filename, # raw_filename
                alpha, # 1 = DXT1 (no alpha), 3 = DXT5 (alpha)
                0, # 1 = generate mipmaps <--- XXX Set this for in-game objects
                0, # 0 = save current layer
                0, # format
                -1, # transparent-index
                0, # DXT compression color-type (Tweaking may help in some cases)
                0, # Dither
                0, # mipmap-filter - maybe try tweaking this for in-game objects
                0, # gamma-correct
                2.2, # gamma
        )
    except:
        # Try newer API
        pdb.file_dds_save(
                image,
                image.active_layer,
                filename, # filename
                filename, # raw_filename
                alpha, # 1 = DXT1 (no alpha), 3 = DXT5 (alpha)
                0, # 1 = generate mipmaps <--- XXX Set this for in-game objects
                0, # 0 = save current layer
                0, # format
                -1, # transparent-index
                0, # mipmap-filter - maybe try tweaking this for in-game objects
                0, # mipmap-wrap
                0, # gamma-correct
                0, # use srgb colorspace for gamma correction
                2.2, # gamma
                0, # use perceptual error metric during DXT compression
                0, # preserve alpha coverage
                0.5, # alpha test threshold
        )

def save_png(image, filename):
    pdb.file_png_save2(image, image.active_layer, filename, filename,
            0, # interlace
            9, # compression
            0, # save background colour
            0, # save gamma
            0, # save layer offset
            1, # save pHYs (resolution?)
            1, # save creation time
            1, # save comment
            1, # preserve colour of transparent pixels
    )

def save_jpg(image, filename):
    pdb.file_jpeg_save(image, image.active_layer, filename, filename,
            0.9, # quality
            0.0, # smoothing
            1, # optimize
            0, # progressive
            "Generated by DarkStarSword's Miasmata translation scripts", # comment
            0, # Subsampling option number. 0 = 4:4:4?
            1, # baseline
            0, # restart
            1, # dct algorithm. 1 = Integer?
    )

def save_xcf(image, filename):
    pdb.gimp_xcf_save(0, image, image.active_layer, filename, filename)
    image.clean_all()