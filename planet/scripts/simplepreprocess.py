import os
from PIL import Image
import re
from shutil import copy
from osgeo import gdal, gdalconst
import sys

perim = [-1, 0, 1]

in_dir = sys.argv[1]

for f in os.listdir(in_dir):
    im = Image.new('RGB', (50, 50))
    [y, x] = re.split(r"_|\.", f)[0:2]
    temp = Image.open(f"boa_planet/{int(x)}_-{int(y)+1}.tif")
    im.paste(temp, (0, 0))
    im = im.resize((225, 202), resample=Image.BICUBIC)
    print(f"saving boa_lowres/{f}")
    im.save(f"boa_lowres/{f}")
