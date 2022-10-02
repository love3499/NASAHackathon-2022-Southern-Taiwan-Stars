from glob import glob
from os.path import splitext
from os.path import split
from PIL import Image
import os

def jpg2png(data_dir):
    jpglist = glob( data_dir+"*.[J][P][G]" )

    for jpg in jpglist:
        im = Image.open(jpg)
        png = splitext(jpg)[0]+".png"
        '''
        png = split(png)[1]
        '''
        im.save(png)
    os.system("rm "+data_dir+"*.[J][P][G]")
           
