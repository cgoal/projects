# -*- coding: utf-8 -*-

import logging
import os
import time
#import face_recognition
#import cv2
import picamera
from picamera.array import PiRGBArray
import cv2
from faceDetect import faceDetect

def fr(fd=''): #fd mean class of faceDetect
    #面部识别模块
    try:
        cam=picamera.PiCamera()
        cam.rotation=180
        cam.resolution=(320,240)
        #cam.hfilp=True
        #cam.vflip=True
        rawCap=PiRGBArray(cam,size=(320,240))
        time.sleep(0.1)
        for frame in cam.capture_continuous(rawCap,format='bgr',use_video_port=True):
            img=frame.array
            
            img=fd.Detect(img)
            
            cv2.imshow('Video',img)
            
            rawCap.truncate(0)
            
            if cv2.waitKey(1) & 0xFF==ord('q'):
                break
            
        cv2.destroyAllWindows()
        
    except RuntimeError:
        logger.error('Video Open Error')

    
def main():
    
    print('know face loading...')
    fd=faceDetect()
    kn=fd.loadFace()
    fr(fd=fd)

if __name__=="__main__":
    
    logging.basicConfig(filename = os.path.join(os.getcwd(), 'frlog.txt'), filemode='a',level = logging.DEBUG, format = '%(asctime)s - %(levelname)s: %(message)s')
    logger=logging.getLogger('root')
    
    main()