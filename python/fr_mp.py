# -*- coding: UTF-8 -*-

import logging
import os
import time
#import face_recognition
import picamera
from picamera.array import PiRGBArray
import multiprocessing as mp
import cv2
from faceDetect import faceDetect




def fr(fd=''): #fd mean class of faceDetect
    #face detect moduls
    try:
        print('know face loading...')
        #global kn
        
        #kn=loadFace()
        
        cam=picamera.PiCamera()
        cam.rotation=0 #180
        cam.resolution=(320,240)
        #cam.hfilp=True
        #cam.vflip=True
        rawCap=PiRGBArray(cam,size=(320,240))
        time.sleep(0.1)
        
        cam.capture(rawCap,format='bgr')
        
        pool=mp.Pool(processes=4)
        fcount=0
        
        r1=pool.apply_async(fd.Detect,(rawCap.array,))
        r2=pool.apply_async(fd.Detect,(rawCap.array,))
        r3=pool.apply_async(fd.Detect,(rawCap.array,))
        r4=pool.apply_async(fd.Detect,(rawCap.array,))
        
        f1=r1.get()
        f2=r2.get()
        f3=r3.get()
        f4=r4.get()
        
        rawCap.truncate(0)
                
        for frame in cam.capture_continuous(rawCap,format='bgr',use_video_port=True):
            
            img=frame.array
            
            if fcount==1:
                r1=pool.apply_async(fd.Detect,(img,))
                f2=r2.get()
                cv2.imshow('Video',f2)
                
            elif fcount==2:
                r2=pool.apply_async(fd.Detect,(img,))
                f3=r3.get()
                cv2.imshow('Video',f3)
                
            elif fcount==3:
                r3=pool.apply_async(fd.Detect,(img,))
                f4=r4.get()
                cv2.imshow('Video',f4)
                
            elif fcount==4:
                r4=pool.apply_async(fd.Detect,(img,))
                f1=r1.get()
                cv2.imshow('Video',f1)
                fcount=0
            
            fcount+=1
                
            #img=fd.Detect(img)
            #cv2.imshow('Video',img)
            
            rawCap.truncate(0)
            
            if cv2.waitKey(1) & 0xFF==ord('q'):
                break
            
        cv2.destroyAllWindows()
        
    except RuntimeError:
        logger.error('Video Open Error')

    
def main():
    
    fd=faceDetect()
    fd.loadFace()
    fr(fd=fd)

if __name__=="__main__":
    
    logging.basicConfig(filename = os.path.join(os.getcwd(), 'frlog.txt'), filemode='a',level = logging.DEBUG, format = '%(asctime)s - %(levelname)s: %(message)s')
    logger=logging.getLogger('root')
    
    main()
