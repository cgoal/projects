# -*- coding: utf-8 -*-

import logging
import os
#import face_recognition
import cv2
from faceDe_PIL import faceDetect

def fr(vchannel=0,fd=''): #fd mean class of faceDetect
    #面部识别模块
    try:
        cam= cv2.VideoCapture(vchannel)
        cam.set(3,320)
        cam.set(4,240)
    except RuntimeError:
        logger.error('Video Open Error')
        
    while(cam.isOpened()):
        ret, frame = cam.read()
        
        if not ret:
            break
        
        frame=cv2.flip(frame,-1)

        #small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        
        #frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        
        frame=fd.Detect(frame)
        
        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()
    
def main():
    
    print('know face loading...')
    fd=faceDetect()
    kn=fd.loadFace()
    fr(fd=fd)

if __name__=="__main__":
    
    logging.basicConfig(filename = os.path.join(os.getcwd(), 'frlog.txt'), filemode='a',level = logging.DEBUG, format = '%(asctime)s - %(levelname)s: %(message)s')
    logger=logging.getLogger('root')
    
    main()