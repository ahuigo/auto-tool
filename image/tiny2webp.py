#!/usr/bin/env python3
from PIL import Image
import sys

if len(sys.argv)<3:
    quit('./tiny2webp.py src.png dst.png.webp')
src = sys.argv[1]
dst = sys.argv[2]
pic=Image.open(src)
pic.save(dst, 'webp', optimize = True, quality = 88)
