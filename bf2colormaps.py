#!/usr/bin/python3
import os
import sys
import re
from PIL import Image

pattern = r'tx0(?P<x>\d)x0(?P<y>\d).dds'

def get_colormap_ids(fname):
    idx, idy = re.match(pattern, fname).groups()
    return int(idx), int(idy)

def main(colormaps):
    # get tx0*x0*.dds filenames
    filenames = [item for item in os.listdir(colormaps) if re.match(pattern, item)]

    # get amount of colormaps rows and columns for calculating resulting size
    numx, numy = [max(int(x) for x in nums) + 1 for nums in zip(*[
        [match.group(groupname) for groupname in ['x', 'y']]
        for match in (re.match(pattern, fname) for fname in os.listdir(colormaps)) if match
    ])]

    # get tx0*x0*.dds patch size
    patch = Image.open(os.path.join(colormaps, filenames[0]))

    # combining into new image
    dst = Image.new('RGB', (patch.width * numx, patch.height * numy))
    for fname in filenames:
        colormap = Image.open(os.path.join(colormaps, fname))
        idx, idy = get_colormap_ids(fname)
        dst.paste(colormap, (patch.width * idx, patch.height * idy))
    
    # saving in same directory where colormaps is
    dst.save(os.path.join(colormaps, 'colormap.png'))

if __name__ == '__main__':
    main(sys.argv[1])