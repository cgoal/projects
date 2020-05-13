#!/usr/bin/python3

import os
import qrcode
from PIL import Image

def qrcreate(txt='',iconimg=None):
    
    if iconimg!=None and txt!='':
        qr=qrcode.QRCode(
            version=2,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=1)
        qr.add_data(txt)
        qr.make(fit=True)
        img=qr.make_image()
        
        img=img.convert('RGBA')
        img_w,img_h=img.size
        factor=5
        size_w=int(img_w/factor)
        size_h=int(img_h/factor)
        
        #icon=iconimg.copy()
        icon_w,icon_h=iconimg.size
        if icon_w>size_w:
            icon_w=size_w
        if icon_h>size_h:
            icon_h=size_h
        iconimg=iconimg.resize((icon_w,icon_h),Image.ANTIALIAS)
        
        w=int((img_w - icon_w)/2)
        h=int((img_h - icon_h)/2)
        img.paste(iconimg,(w,h),mask=None)
        img.show()
        img.save('qrimg.png')
        return True
        
    elif txt!='':
        qr=qrcode.QRCode(
            version=2,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=1)
        qr.add_data(txt)
        qr.make(fit=True)
        img=qr.make_image()
        img.show()
        img.save('qrimg.png')
        return True
    else:
        return False
        
    #参数 version 表示生成二维码的尺寸大小，取值范围是 1 至 40，最小尺寸 1 会生成 21 * 21 的二维码矩阵，version 每增加 1，生成的二维码就会添加 4 个单位大小，例如 version 是 2，则生成 25 * 25 尺寸大小的二维码。
    #参数 error_correction 指定二维码的容错系数，分别有以下4个系数
        #ERROR_CORRECT_L: 7%的字码可被容错
        #ERROR_CORRECT_M: 15%的字码可被容错
        #ERROR_CORRECT_Q: 25%的字码可被容错
        #ERROR_CORRECT_H: 30%的字码可被容错
    #参数 box_size 表示二维码里每个格子的像素大小,参数 border 表示边框的格子宽度是多少（默认是4）

def main():
    
    info=input('qr code infomation input\n')
    i=Image.open('img2.jpg')
    r=qrcreate(txt=info,iconimg=i)
    print(i,r)

if __name__=="__main__":
    
    main()