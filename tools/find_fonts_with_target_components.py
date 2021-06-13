import os, sys, re
import glob
import argparse
import json
from fontTools.ttLib import TTFont

chn_decomposition_path = "../data/chn_decomposition.json"

def get_psname(ttFont):
    return ttFont["name"].getName(nameID=6, platformID=3, platEncID=1).toStr()

def find_fonts(font_dir, chn_decomposition):
    """find fonts containing components defined in 'chn_decomposition.json'
    """

    psname2unis = {}
    for file in glob.glob(os.path.join(font_dir, "*.*tf")):
        ttFont =TTFont(file)
        psname = get_psname(ttFont)
        cmap = ttFont.getBestCmap()
        all_unis = set(cmap.keys())

        # find chars whose components are in given font
        for uni, comps in chn_decomposition.items():
            if ord(uni) not in all_unis or not set([ord(uni) for uni in comps]) < all_unis:
                continue
            psname2unis.setdefault(psname, set()).add(ord(uni))
    return psname2unis

def find_common_unis(psname2unis):
    """find common component unis among given fonts
    """

    all_kanji_unis = set(range(0x2E80, 0x2FDF+1)) | {0x3005, 0x3007, 0x303B} | set(range(0x4E00, 0x9FFF+1)) | set(range(0xF900, 0xFAFF+1)) | set(range(0x20000, 0x2FFFF+1))

    common_unis = all_kanji_unis

    for psname, unis in psname2unis.items():
        common_unis = common_unis & unis

    return common_unis

def get_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("font_dir", metavar="FONT_DIR", type=str,
                        help="fonts directory")

    args = parser.parse_args()

    return args

def main():
    args = get_args()

    with open(chn_decomposition_path) as fin:
        chn_decomposition = json.load(fin)

    psname2unis = find_fonts(args.font_dir, chn_decomposition)
    common_unis = find_common_unis(psname2unis)

    print(len(common_unis))

if __name__ == "__main__":
    main()
