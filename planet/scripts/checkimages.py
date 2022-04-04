import os
from PIL import Image
import re

perim = [-1, 0, 1]

for f in os.listdir("boa_images"):
    [y, x] = re.split(r"_|\.", f)[0:2]
    context = True
    for i in perim:
        for j in perim:
            context &= os.path.exists(f"boa_planet/{int(x)+i}_-{int(y)+1+j}.tif")
#    exists = os.path.exists(f"boa_planet/{x}_-{int(y)+1}.tif")
    print(f"{f}: {context}")
