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



class faceDetect:
    
    _red=(0,0,255)
    _white=(255,255,255)
    _font=cv2.FONT_HERSHEY_DUPLEX
    _name='UnknownPerson'
    _classifier=cv2.CascadeClassifier('/home/pi/opencv-3.4.1/data/lbpcascades/lbpcascade_frontalface.xml')
    
    def __init__(self,path=os.path.join(os.getcwd(),'known'),cv=False):
        self.path=path
        self.cv=cv
        self.faces=[]
        
    def loadFace(self):
        
        for i in os.listdir(self.path):
            fp={}
            if self.cv:
                faceimg=face_recognition.load_image_file(os.path.join(self.path,i))[:,:,::-1]
            else:
                faceimg=face_recognition.load_image_file(os.path.join(self.path,i))
           
            facelocation=face_recognition.face_locations(faceimg)
            fp={'name':i.replace('.jpg',''),'face':face_recognition.face_encodings(faceimg,facelocation)[0]}
        
            self.faces.append(fp)
        return self.faces

    def Detect(self,checkframe=''):
    
        if self.faces!='':
            if self.cv:
                checkframe=checkframe[:,:,::-1]
        
            cf_locations=face_recognition.face_locations(checkframe)
            
            if cf_locations==[]:
                return checkframe
        
            cf_encodings=face_recognition.face_encodings(checkframe,cf_locations)
        
            for (top,right,bottom,left), cf_encoded in zip(cf_locations,cf_encodings):
            
                for i in self.faces:
                    fname=i['name']
                
                    match=face_recognition.compare_faces([i['face']],cf_encoded)
                    self._name='UnknownPerson'
                    if match[0]:
                        self._name=fname
                        break
                            
                cv2.rectangle(checkframe,(left,top),(right,bottom),self._red,2)
                cv2.rectangle(checkframe,(left,bottom-20),(right,bottom),self._red,cv2.FILLED)
            
                cv2.putText(checkframe,self._name,(left+6,bottom-6),self._font,0.5,self._white,1)
    
        return checkframe
    
    def find_faces(self,img='',face_class=_classifier):
        
        #获取面部信息
        if img==None:
            return None
    
        gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        faces=face_class.detectMultiScale(gray)
        return faces,img



def CamInit():
    #摄像头初始化
    camera=PiCamera()
    camera.resolution=(320,240)
    camera.framerate=60
    rawCapture=PiRGBArray(camera,size=(320,240))


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
