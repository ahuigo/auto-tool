#!/usr/bin/env python3
from PIL import Image
import PIL
import os,sys
import glob

if len(sys.argv)<3:
    quit('./compress2webp.py src.png dst.png.webp')
src = sys.argv[1]
dst = sys.argv[2]
pic=Image.open(src)
p.save(dst, 'webp', optimize = True, quality = 88)
