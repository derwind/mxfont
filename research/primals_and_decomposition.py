# check primals' definition. They seem to be characters without sub-glyphs.

import json

def load_json(json_path):
    with open(json_path) as fin:
        return json.load(fin)

def main():
    chn_primals = load_json("../data/chn_primals.json")
    chn_decomposition = load_json("../data/chn_decomposition.json")

    chars_wo_comps = set()
    for c, comps in chn_decomposition.items():
        if len(comps) <= 1 and comps[0] == c:
            chars_wo_comps.add(c)
    print(set(chn_primals) == chars_wo_comps)

if __name__ == "__main__":
    main()
