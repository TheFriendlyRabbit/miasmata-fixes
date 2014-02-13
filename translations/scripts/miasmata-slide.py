#!/usr/bin/env python

from gimpfu import *

# font = 'Times New Roman,'
# font = 'Gentium' # Closer
# font = 'Nimbus Roman No9 L' # Closer, h still not tall enough
# font = 'STIXGeneral' # No
# font = 'URW Palladio L Medium' # Still not quite right, shape is off
# font = 'Liberation Serif'
# font = 'Georgia' # Close
# font = 'Gentium Book Basic' # Close
# font = 'Gentium Basic'
# font = 'Droid Serif'
# font = 'DejaVu Serif'
# font = 'cmr10' # <-- Pretty close, letters aren't quite well enough defined
# font = 'Century Schoolbook L Medium'  # close
# font = 'Bitstream Charter'
# font_size = 40.0
# line_spacing = 27.0
# line_spacing = 31.0

font = 'perpetua' # Closest yet for shape. Letters not quite thick enough. Still not quite right - e.g. shape of 'g' slightly off
font_size = 40.0
line_spacing = 20.0

width = height = 1024

def add_slide_text(image, txt):
    gimp.set_foreground(255, 255, 255)
    text = pdb.gimp_text_fontname(image, None, 0, 0, txt, 0, True, font_size, PIXELS, font)
    text.name = 'Text'
    pdb.gimp_text_layer_set_line_spacing(text, line_spacing)
    pdb.gimp_text_layer_set_hint_style(text, TEXT_HINT_STYLE_NONE)

    return text

def enlarge_first_letter(text):
    # XXX: Requires a patched GIMP to set text markup
    # See https://bugzilla.gnome.org/show_bug.cgi?id=724101
    markup = '<span size=\"61440\">%s</span>%s' % (txt[0], txt[1:])
    pdb.gimp_text_layer_set_markup(text, markup)

def scale_text(image, text):
    try:
        pdb.gimp_context_set_interpolation(INTERPOLATION_LANCZOS)
    except:
        pdb.gimp_context_set_interpolation(INTERPOLATION_NOHALO)
    text.scale(width - 2*170, text.height)
    text.translate(170, (image.height - text.height) / 2)

def center_layer(image, layer):
    layer.translate((image.width - layer.width) / 2, (image.height - layer.height) / 2)

def blur_layer(image, layer):
    pdb.plug_in_gauss_rle2(image, layer, 1.0, 1.0)

def save_dds(image, filename, alpha):
    alpha = alpha and 3 or 1
    pdb.file_dds_save(
            image,
            image.active_layer,
            filename, # filename
            filename, # raw_filename
            alpha, # 1 = DXT1 (no alpha), 3 = DXT5 (alpha)
            0, # 1 = generate mipmaps
            0, # 0 = save current layer
            0, # format
            -1, # transparent-index
            0, # DXT compression color-type (Tweaking may help in some cases)
            0, # Dither
            0, # mipmap-filter - maybe try tweaking this for in-game objects
            0, # gamma-correct
            2.2, # gamma
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

def add_background(image, opacity=100.0):
    background = gimp.Layer(image, 'Background', width, height, RGB_IMAGE, opacity, NORMAL_MODE)
    image.add_layer(background, -1)

    gimp.set_background(0, 0, 0)
    background.fill(BACKGROUND_FILL)

    return background

def display_image(image):
    try:
        gimp.Display(image)
    except:
        pass

def render_end_slide(source_txt_file, output_basename):
    txt = open(source_txt_file, 'rb').read().decode('utf-8').strip()

    image = gimp.Image(width, height, RGB)
    background = add_background(image)
    display_image(image)
    text = add_slide_text(image, txt)
    enlarge_first_letter(text)
    scale_text(image, text)
    blur_layer(image, text)

    # image.active_layer = background
    save_xcf(image, '%s.xcf' % output_basename)

    image2 = pdb.gimp_image_duplicate(image)
    image2.flatten()

    save_dds(image2, '%s.dds' % output_basename, False)
    save_png(image2, '%s.png' % output_basename)

def render_intro_slide(source_txt_file, output_basename):
    txt = open(source_txt_file, 'rb').read().decode('utf-8').strip()

    image = gimp.Image(width, height, RGB)
    background = add_background(image, 0.0)
    display_image(image)
    text = add_slide_text(image, txt)
    pdb.gimp_text_layer_set_justification(text, TEXT_JUSTIFY_CENTER)
    center_layer(image, text)
    blur_layer(image, text)

    save_xcf(image, '%s.xcf' % output_basename)

    image2 = pdb.gimp_image_duplicate(image)
    image2.merge_visible_layers(CLIP_TO_IMAGE)
    save_dds(image2, '%s.dds' % output_basename, True)
    save_png(image2, '%s.png' % output_basename)

    background.opacity = 100.0
    image.flatten()
    save_jpg(image, '%s.jpg' % output_basename)

register(
    "miasmata_end_slide",
    "Generate an image for Miasmata's end sequence",
    "Generate an image for Miasmata's end sequence",
    "Ian Munsie",
    "Ian Munsie",
    "2014",
    "<Toolbox>/_Miasmata/_End",
    None,
    [
        (PF_FILE, "source_txt_file", "utf-8 encoded file with the text to place on the slide", None),
        (PF_STRING, "output_basename", "Base output filename", None),
    ],
    [],
    render_end_slide,
)

register(
    "miasmata_intro_slide",
    "Generate an image for Miasmata's intro sequence",
    "Generate an image for Miasmata's intro sequence",
    "Ian Munsie",
    "Ian Munsie",
    "2014",
    "<Toolbox>/_Miasmata/_Intro",
    None,
    [
        (PF_FILE, "source_txt_file", "utf-8 encoded file with the text to place on the slide", None),
        (PF_STRING, "output_basename", "Base output filename", None),
    ],
    [],
    render_intro_slide,
)

main()
