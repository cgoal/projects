#!/usr/bin/python3  

# the modules, using the PIR sensor to detect if person close and show the
# Temperature. It just to test the gpio function


import logging
import os

logging.basicConfig(filename = os.path.join(os.getcwd(), 'log.txt'), filemode='a',level = logging.DEBUG, format = '%(asctime)s - %(levelname)s: %(message)s')
logger=logging.getLogger('root')



try:
    import RPi.GPIO as GPIO
except RuntimeError:
    logger.error('gpio error')
    
import time
import sensor as sr


def main():
    
    while True:
        
        pir=sr.PIR()
        
        if pir==1:
            print('some one incoming')
            Temperature,Humidity=sr.TH()
            if Temperature!=False:
                print("Time:",time.asctime(time.localtime(time.time())))
                print("temperature:", Temperature)
                print("humidity:",Humidity)
                logger.info("temperature: %.2f - humidity: %.2f", Temperature,Humidity)
        
        time.sleep(1.5)
        
            

if __name__=="__main__":
    
    main()
    
