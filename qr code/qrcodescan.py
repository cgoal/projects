#!/usr/bin/env python3
#-*-coding:UTF-8-*-


import cv2
import pyzbar.pyzbar as pyzbar

def decodeDisplay(img):
    
    barcodes=pyzbar.decode(img)
    barData=''
    
    for barcode in barcodes:
        (x,y,w,h)=barcode.rect
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
        
        barData=barcode.data.decode('utf-8')
        barType=barcode.type
        
        text='{}({})'.format(barData,barType)
        cv2.putText(img,text,(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,125),2)
        
        print('[INFO] found {} barcode:{}'.format(barType,barData))
    
    return img, barData

def detect():
    
    cam=cv2.VideoCapture(0)
    barcodelist=[]
    tempData=''
    
    while (cam.isOpened()):
        ret,frame=cam.read()
        
        if not ret:
            break
        
        frm=cv2.flip(frame,-1)
        
        im, data=decodeDisplay(frm)
        
        if data!='':
            if tempData=='':
                barcodelist.append(data)
                tempData=data
            elif tempData!=data:
                barcodelist.append(data)
                tempData=data
        
        cv2.imshow('barcode scan',im)
        
        Key=cv2.waitKey(1)&0xFF
        if Key==ord('q'):
            break
        elif Key==ord('s'):
            with open('barcode.log','a') as savefile:
                for line in barcodelist:
                    savefile.write(line +';\n')
            break
        
    cam.release()
    cv2.destroyAllWindows()
    
if __name__=='__main__':
    detect()
    