from glob import glob
from os.path import splitext
from PIL import Image
import os

def resize(data_dir):
    pnglist = glob( data_dir+"*.[j][p][g]" )
    print(pnglist)
    for png in pnglist:
        im = Image.open(png)
        png = splitext(png)[0]+".JPG"	
        nim = im.resize((480,320), Image.BILINEAR)
        nim.save(png)
