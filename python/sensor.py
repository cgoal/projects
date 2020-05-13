#!/usr/bin/python3  
  

#import logging
#import os

#logging.basicConfig(filename = os.path.join(os.getcwd(), 'log.txt'), filemode='a',level = logging.DEBUG, format = '%(asctime)s - %(levelname)s: %(message)s')
#logger=logging.getLogger(__name__)

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print('gpio error')
    #logging.error('gpio error')
    #return 'gpio error'

import time  
  
def TH(channel=17): #DH11温度湿度检测
    #channel = 2          #引脚号16  
    data = []           #温湿度值  
    j = 0               #计数器  
  
    GPIO.setmode(GPIO.BCM)      #以BCM编码格式
    
    GPIO.setwarnings(False)
  
    time.sleep(1)           #时延一秒  
  
    GPIO.setup(channel, GPIO.OUT)  
  
    GPIO.output(channel, GPIO.LOW)  
    time.sleep(0.02)        #给信号提示传感器开始工作  
    GPIO.output(channel, GPIO.HIGH)  
  
    GPIO.setup(channel, GPIO.IN)  
  
    while GPIO.input(channel) == GPIO.LOW:  
        continue  
  
    while GPIO.input(channel) == GPIO.HIGH:  
        continue  
  
    while j < 40:  
        k = 0  
        while GPIO.input(channel) == GPIO.LOW:  
            continue  
      
        while GPIO.input(channel) == GPIO.HIGH:  
            k += 1  
            if k > 100:  
                break  
      
        if k < 8:  
            data.append(0)  
        else:  
            data.append(1)  
  
        j += 1  
  
    #print ("sensor is working")
    #print (data)              #输出初始数据高低电平  
  
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
  
    if check == tmp:                                #数据校验，相等则输出  
        #print ("temperature : ", temperature, ", humidity : " , humidity)  
        GPIO.cleanup()
        return temperature, humidity
    else:                                       #错误输出错误信息，和校验数据  
        #print ("wrong")  
        #print ("temperature : ", temperature, ", humidity : " , humidity, " check : ", check, " tmp : ", tmp)
        #logger.info('check %s',check)
        GPIO.cleanup()
        return False,False
    
    #GPIO.cleanup()
    
    
    
def PIR(channel=4): #红外人体检测
    
    GPIO.setmode(GPIO.BCM)      #以BCM编码格式
    
    GPIO.setwarnings(False)
  
    GPIO.setup(channel, GPIO.IN)
    
    pir=GPIO.input(channel)
    
    GPIO.cleanup()
    
    #print(pir)
    
    return pir
    
if __name__=="__main__":
    
    main()
    
