# -*- coding: utf-8 -*-

import os
import face_recognition
import cv2


class faceDetect:
    
    _red=(0,0,255)
    _white=(255,255,255)
    _font=cv2.FONT_HERSHEY_DUPLEX
    _name='UnknownPerson'
    
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