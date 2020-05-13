# -*- coding: utf-8 -*-

import logging
import os
import face_recognition
import cv2
from sensor import PIR
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import os

def loadFace(path=os.path.join(os.getcwd(),'known'),cv=True):
    faces=[]
    for i in os.listdir(path):
        fp={}
        if cv:
            faceimg=face_recognition.load_image_file(os.path.join(path,i))[:,:,::-1]
        else:
            faceimg=face_recognition.load_image_file(os.path.join(path,i))
           
        facelocation=face_recognition.face_locations(faceimg)
        fp={'name':i.replace('.jpg',''),'face':face_recognition.face_encodings(faceimg,facelocation)[0]}
        
        
        faces.append(fp)
    return faces

def faceDetect(checkframe='',knowfaces='',cv=True):
    red=(0,0,255)
    white=(255,255,255)
    font=cv2.FONT_HERSHEY_DUPLEX
    
    if knowfaces!='':
        if cv:
            checkframe=checkframe[:,:,::-1]
        
        cf_locations=face_recognition.face_locations(checkframe)
        print(cf_locations)
        if cf_locations==None:
            print('no face detect')
            return checkframe
        
        cf_encodings=face_recognition.face_encodings(checkframe,cf_locations)
        
        for (top,right,bottom,left), cf_encoded in zip(cf_locations,cf_encodings):
            
            for i in knowfaces:
                fname=i['name']
                
                match=face_recognition.compare_faces([i['face']],cf_encoded)
                name='UnknownPerson'
                if match[0]:
                    name=fname
                    break
            
            cv2.rectangle(checkframe,(left,top),(right,bottom),red,2)
            cv2.rectangle(checkframe,(left,bottom-35),(right,bottom),red,cv2.FILLED)
            
            cv2.putText(checkframe,name,(left+6,bottom-6),font,1.0,white,1)
    
    return checkframe


def fr(vchannel=0,knowfaces=[]):
    #面部识别模块
    try:
        cam= cv2.VideoCapture(vchannel)
        cam.set(3,640)
        cam.set(4,480)
    except RuntimeError:
        logger.error('Video Open Error')
        
    while(cam.isOpened()):
        ret, frame = cam.read()
        
        if not ret:
            break
        
        frame=cv2.flip(frame,-1)

        #small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        
        #frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        
        frame=faceDetect(frame,knowfaces,False)
        
        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

def CamInit():
    #摄像头初始化
    camera=PiCamera()
    camera.resolution=(320,240)
    camera.framerate=60
    rawCapture=PiRGBArray(camera,size=(320,240))
    

def get_faces(img,face_cascade=cv2.CascadeClassifier('/home/pi/opencv-3.4.1/data/lbpcascades/lbpcascade_frontalface.xml')):
    #获取面部信息
    if img==None:
        return None
    
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces=face_cascade.detectMultiScale(gray)
    return faces,img
    

    
def main():
    
    faces=loadFace(cv=False)
    fr(knowfaces=faces)

if __name__=="__main__":
    
    logging.basicConfig(filename = os.path.join(os.getcwd(), 'frlog.txt'), filemode='a',level = logging.DEBUG, format = '%(asctime)s - %(levelname)s: %(message)s')
    logger=logging.getLogger('root')
    
    main()