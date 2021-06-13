import os, sys, re
import argparse
from fontTools.ttLib import TTFont
from fontTools.pens.basePen import BasePen

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

def get_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("font_path", metavar="FONT_PATH", type=str,
                        help="font path")

    args = parser.parse_args()

    return args

def main():
    args = get_args()

    ttFont = TTFont(args.font_path)
    gs = ttFont.getGlyphSet()
    gorder = ttFont.getGlyphOrder()

    for gid, gname in enumerate(gorder):
        g = gs[gname]
        pen = SpaceOrNotPen(gs)
        try:
            g.draw(pen)
        except StopDraw:
            pass
        if pen.is_space:
            print(gid)

if __name__ == "__main__":
    main()
