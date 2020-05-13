# -*- coding: UTF-8 -*-

import RPi.GPIO as GPIO
import time
import atexit

class sensor:
    
    def __init__(self):
        atexit.register(GPIO.cleanup)
        GPIO.setmode(GPIO.BCM)#以BCM编码格式
        GPIO.setwarnings(False)
        
    def stop(self):
        GPIO.cleanup()

    
class Servo(sensor): #舵机控制
    
    _max_delay=0.2
    _min_delay=0.04
    _channel=17
    _initposition=90
    _minangle=30
    _maxangle=160
    _position=90
    
    def __init__(self,channel=_channel):
        
        sensor.__init__(self)
        
        self._channel=channel
        GPIO.setup(self._channel,GPIO.OUT,initial=False)
        
        self.pwm=GPIO.PWM(self._channel,50) #PWM
        self.pwm.start(self._initposition/18.+2.5)  # init at 90 angle
        self._position=self._initposition
        time.sleep(self._max_delay)
        self.pwm.ChangeDutyCycle(0)
        time.sleep(self._min_delay)

    def setangle(self,angle):
        
        __steps=20
        
        if type(angle)==float:
            angle=int(angle)
        
        if angle>=self._minangle and angle<=self._maxangle and angle!=self._position:
            
            if angle<self._position:
                __steps=-1*__steps
            
            if abs(self._position-angle)>=abs(__steps):
                for a in range(self._position,angle,__steps):
                    dutyCycle=a/18.+2.5
                    self.pwm.ChangeDutyCycle(dutyCycle)
                    time.sleep(self._min_delay)
                    self.pwm.ChangeDutyCycle(0)
                    time.sleep(self._min_delay)
                
                if a!=angle:
                    dutyCycle=angle/18.+2.5
                    self.pwm.ChangeDutyCycle(dutyCycle)
                    time.sleep(self._min_delay)
                    self.pwm.ChangeDutyCycle(0)
                    time.sleep(self._min_delay)
            else:
                dutyCycle=angle/18.+2.5
                self.pwm.ChangeDutyCycle(dutyCycle)
                time.sleep(self._min_delay)
                self.pwm.ChangeDutyCycle(0)
                time.sleep(self._min_delay)
            
            self._position=angle
            
    def reset(self):
        
        self._position=self._initposition
        self.pwm.start(self._position/18.+2.5)
        time.sleep(self._max_delay)
        self.pwm.ChangeDutyCycle(0)
        time.sleep(self._min_delay)
            

    def stop(self):
        self.pwm.stop()
        time.sleep(self._max_delay)
        GPIO.cleanup()
        
class DHT(sensor): #DHT11 温度湿度传感器
    
    _channel=17  #引脚号16
    _AdaType='DHT11'
    _sensor=None
    _adht=None
    
    def __init__(self,channel=_channel,aType=_AdaType):
        
        sensor.__init__(self)
        self._channel=channel
        self._AdaType=aType
        if self._AdaType!=None:
            
            import Adafruit_DHT as adht
            self._adht=adht
            if self._AdaType=='DHT11':
                self._sensor=self._adht.DHT11
            elif self._AdaType=='DHT22':
                self._sensor=self._adht.DHT22
            else:
                self._sensor=None
                
    def temper(self):
        
        if self._sensor!=None:
            humidity,temperature=self._adht.read_retry(self._sensor, self._channel)
            return humidity,temperature
        
        
        data = []           #温湿度值
        j=0
        
        #传感器初始化
        time.sleep(1)           #时延一秒
        GPIO.setup(self._channel, GPIO.OUT)
        GPIO.output(self._channel, GPIO.LOW)  
        time.sleep(0.02)        #给信号提示传感器开始工作  
        GPIO.output(self._channel, GPIO.HIGH)
        
        GPIO.setup(self._channel, GPIO.IN)
  
        while GPIO.input(self._channel) == GPIO.LOW:  
            continue  
  
        while GPIO.input(self._channel) == GPIO.HIGH:  
            continue  
  
        while j < 40:
            
            k = 0
            
            while GPIO.input(self._channel) == GPIO.LOW:
                continue  
      
            while GPIO.input(self._channel) == GPIO.HIGH:
                k += 1  
                if k > 100:  
                    break  
      
            if k < 16:  
                data.append(0)  
            else:  
                data.append(1)  
  
            j += 1
  
        print ("sensor is working")
        print (data)              #输出初始数据高低电平
        
        humidity_bit = data[0:8]        #分组
        humidity_point_bit = data[8:16]  
        temperature_bit = data[16:24]  
        temperature_point_bit = data[24:32]  
        check_bit = data[32:40]  
        
        humidity = 0  
        humidity_point = 0  
        temperature = 0  
        temperature_point = 0  
        check = 0
        
        for i in range(8):  
            humidity += humidity_bit[i] * 2 ** (7 - i)              #转换成十进制数据  
            humidity_point += humidity_point_bit[i] * 2 ** (7 - i)  
            temperature += temperature_bit[i] * 2 ** (7 - i)  
            temperature_point += temperature_point_bit[i] * 2 ** (7 - i)  
            check += check_bit[i] * 2 ** (7 - i)
            
        tmp = humidity + humidity_point + temperature + temperature_point       #十进制的数据相加  
        
        print(check, tmp,humidity,humidity_point,temperature,temperature_point)
        
        if check == tmp:                                #数据校验，相等则输出
            return humidity,temperature
        else:                                       #错误输出错误信息，和校验数据  
            return False,False
        

class PIR(sensor):#红外人体检测
    
    _channel=4
    
    def __init__(self,channel=_channel):
        
        sensor.__init__(self)
        self._channel=channel
        GPIO.setup(self._channel, GPIO.IN)
        
    def detect(self):
        
        return GPIO.input(self._channel)

class Stepper(sensor): #步进电机控制
    
    _StepPins=[17,27,22,23] #GPIO信号通道
    
    # Define advanced sequence
    # as shown in manufacturers datasheet
    _Sep=[[1,0,0,0],
          [0,1,0,0],
          [0,0,1,0],
          [0,0,0,1]]
    
    def __init__(self,SP=_StepPins):
        
        sensor.__init__(self)
        self._StepPins=SP
        
        # set all pins as output
        for pin in self._StepPins:
            GPIO.setup(pin,GPIO.OUT)
            GPIO.output(pin,False)
            
    def setStep(self,step=[0,0,0,0]):
        
        for pin,s in zip(self._StepPins,step):
            GPIO.output(pin,s)
            print(pin,s)
            
    def stop(self):
        self.setStep()
        
        
        
    def run(self,ward='f',delay=0.005,steps=512): #减速比1:64 步进角度5.625度，转一周需4096个信号，512转45度
        
        if ward=='f':
            for i in range(0,steps):
                for s in self._Sep:
                    self.setStep(s)
                    time.sleep(delay)
        elif ward=='b':
            tmpSep=self._Sep.copy()
            tmpSep.reverse()
            for i in range(0,steps):
                for s in tmpSep:
                    self.setStep(s)
                    time.sleep(delay)
            
        
class UltraSM(sensor):#超声波测距
    
    _channel_Tr=17
    _channel_Ec=27
    _temperature=20 #空气温度
    _soundspeed=33100 #音速 厘米/秒
    
    def __init__(self,Tr=_channel_Tr,Ec=_channel_Ec,Tp=_temperature):
        
        sensor.__init__(self)
        self._channel_Tr=Tr
        self._channel_Ec=Ec
        self._temperature=Tp
        self._soundspeed=self._soundspeed+(0.6*self._temperature)
        GPIO.setup(self._channel_Tr, GPIO.OUT)
        GPIO.setup(self._channel_Ec,GPIO.IN)
        
    def measure(self):
        
        GPIO.output(self._channel_Tr,True)
        time.sleep(0.00001)
        GPIO.output(self._channel_Tr,False)
        
        start=time.time()
        
        while GPIO.input(self._channel_Ec)==0:
            start=time.time()
            
        while GPIO.input(self._channel_Ec)==1:
            stop=time.time()
            
        dis=(stop -start)*self._soundspeed/2
        
        
        return dis 
    
    def ave_m(self):
        
        dis1=self.measure()
        time.sleep(0.1)
        dis2=self.measure()
        time.sleep(0.1)
        dis3=self.measure()
        return int((dis1+dis2+dis3)/3)
        