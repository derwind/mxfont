"""
MX-Font
Copyright (c) 2021-present NAVER Corp.
MIT license
"""

from fontTools.ttLib import TTFont
from fontTools.pens.basePen import BasePen
from PIL import Image, ImageFont, ImageDraw
import numpy as np


class StopDraw(Exception):
    pass

class SpaceOrNotPen(BasePen):
    def __init__(self, glyphSet=None):
        super().__init__(glyphSet)
        self.is_space = True

    def _moveTo(self, pt):
        pass

    def _lineTo(self, pt):
        self.is_space = False
        raise StopDraw

    def _curveToOne(self, pt1, pt2, pt3):
        self.is_space = False
        raise StopDraw


def get_defined_chars(fontfile):
    ttf = TTFont(fontfile)
    chars = [chr(y) for y in ttf["cmap"].tables[0].cmap.keys()]
    return chars


def is_space_char(char, ttFont):
    cmap = ttFont.getBestCmap()
    gs = ttFont.getGlyphSet()

    uni = ord(char)
    gname = cmap[uni]
    g = gs[gname]
    pen = SpaceOrNotPen(gs)
    try:
        g.draw(pen)
    except StopDraw:
        pass
    return pen.is_space

def get_filtered_chars(fontpath):
    # ttf = read_font(fontpath)
    defined_chars = get_defined_chars(fontpath)
    avail_chars = []

    ttFont = TTFont(fontpath)

    for char in defined_chars:
        # img = np.array(render(ttf, char))
        # if img.mean() == 255.:
        #     pass

        is_space = is_space_char(char, ttFont)
        if is_space:
            pass
        else:
            avail_chars.append(char.encode('utf-16', 'surrogatepass').decode('utf-16'))

    return avail_chars


def read_font(fontfile, size=150):
    font = ImageFont.truetype(str(fontfile), size=size)
    return font


def render(font, char, size=(128, 128), pad=20):
    width, height = font.getsize(char)
    max_size = max(width, height)

    if width < height:
        start_w = (height - width) // 2 + pad
        start_h = pad
    else:
        start_w = pad
        start_h = (width - height) // 2 + pad

    img = Image.new("L", (max_size+(pad*2), max_size+(pad*2)), 255)
    draw = ImageDraw.Draw(img)
    draw.text((start_w, start_h), char, font=font)
    img = img.resize(size, 2)
    return img
