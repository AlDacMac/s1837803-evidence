import os
from PIL import Image
import re
from shutil import copy
import sys

perim = [-1, 0, 1]

in_dir = sys.argv[1]
out_dir = sys.argv[2]

if not os.path.exists(out_dir):
    os.makedirs(out_dir)

for f in os.listdir(in_dir):
    im = Image.new('RGB', (150, 150))
    [y, x] = re.split(r"_|\.", f)[0:2]
    for i in perim:
        for j in perim:
            temp = Image.open(f"{in_dir}/{int(x)+i}_{-(int(y)+1+j)}.tif")
            im.paste(temp, ((i+1)*50, (j+1)*50))
    im = im.resize((225, 202), resample=Image.BILINEAR)
    im.save(f"{out_dir}/{f}")

