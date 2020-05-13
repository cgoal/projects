# -*- coding: UTF-8 -*-

from imageai.Prediction import ImagePrediction
from imageai.Detection import ObjectDetection
import os

class ImagePredict:
    
    _prediction=ImagePrediction()
    _detection=ObjectDetection()
    _ModeType='SN'
    _ModePath=os.path.join(os.getcwd(),'model')
    _ImgPath=os.getcwd()
    _outputname='oimg.jpg'
    
    def __init__(self,ModeType='',ModePath='',ImgPath=''):
        
        if ModeType in ['SN','RN','IV','DN','RNO']:
            self._ModeType=ModeType
        
        if ModePath!='':
            self._ModePath=ModePath
            
        if ImgPath!='':
            self._ImgPath=ImgPath
    
    def detect(self,Img=None,Type='array'):
        
        if Img is None:
            return
        
        try:
            if Type=='file' or type(Img)==str:
                detections=self._detection.detectObjectsFromImage(
                    input_image=os.path.join(self._ImgPath,imgname),
                    output_image_path=os.path.join(os.getcwd(),self._outputname))
                
                for eachObject in detections:
                    print(eachObject['name']+':'+eachObject['percentage_probability'])
        
                return detections
        
            elif Type=='array' or Type=='stream':
                
                detected_image_array, detections=self._detection.detectObjectsFromImage(
                    input_type=Type,
                    input_image=Img,
                    output_type='array')
                
                return detected_image_array, detections
            
            return
        
        except BaseException as e:
            print(e)


    def predict(self,Img=None,Type='array'):
        
        if Img is None:
            return
        
        try:
            if Type=='file' or type(Img)==str:
                predictions, probabilities = self._prediction.predictImage(
                    os.path.join(self._ImgPath, Img),
                    result_count=5,
                    input_type=Type)
                
                for eachPrediction, eachProbability in zip(predictions, probabilities):
                    print(eachPrediction, " : " , eachProbability)
                
                return predictions, probabilities
            
            elif Type=='array' or Type=='stream':
                predictions, probabilities=self._prediction.predictImage(
                    Img,
                    result_count=5,
                    input_type=Type)
                
                return predictions, probabilities
            
            return
        
        except BaseException as e:
            print(e)
    
    def loadmodel(self):
        
        if self._ModeType=='SN': #SqueezeNet
            self._prediction.setModelTypeAsSqueezeNet()
            self._prediction.setModelPath(os.path.join(self._ModePath,'squeezenet_weights_tf_dim_ordering_tf_kernels.h5'))
            try:
                self._prediction.loadModel()
            except BaseException:
                print('can not find the mode')     
            
        if self._ModeType=='RN': #ResNet50
            self._prediction.setModelTypeAsResNet()
            self._prediction.setModelPath(os.path.join(self._ModePath,'resnet50_weights_tf_dim_ordering_tf_kernels.h5'))
            try:
                self._prediction.loadModel()
            except BaseException:
                print('can not find the mode')
            
        if self._ModeType=='IV': #InceptionV3
            self._prediction.setModelTypeAsInceptionV3()
            self._prediction.setModelPath(os.path.join(self._ModePath,'inception_v3_weights_tf_dim_ordering_tf_kernels.h5'))
            try:
                self._prediction.loadModel()
            except BaseException:
                print('can not find the mode')
            
        if self._ModeType=='DN': #DenseNet121
            self._prediction.setModelTypeAsDenseNet()
            self._prediction.setModelPath(os.path.join(self._ModePath,'DenseNet-BC-121-32.h5'))
            try:
                self._prediction.loadModel()
            except BaseException:
                print('can not find the mode')
            
        if self._ModeType=='RNO': #RetinaNet
            self._detection.setModelTypeAsRetinaNet()
            self._detection.setModelPath(os.path.join(self._ModePath,'resnet50_coco_best_v2.0.1.h5'))
            try:
                self._detection.loadModel(detection_speed='fast')
            except BaseException:
                print('can not find the mode')
        