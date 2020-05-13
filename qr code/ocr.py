#!/usr/bin/python3

import pytesseract as pt
from PIL import Image

def ocr(img=None,l='chi_sim'):
    
    if img!=None:
        try:
            return pt.image_to_string(img,lang=l)
        except Exception as e:
            print('error %s' %e)

