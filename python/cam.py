from picamera import PiCamera,Color
from time import sleep
from PIL import Image
import cv2

def P():
    cam=PiCamera()

    cam.rotation=0 #180
    cam.resolution=(320,240)
    cam.framerate=24
    cam.brightness=60
    cam.contrast=50
    cam.annotate_text='framerate: %s' % 24
    cam.annotate_background=Color('blue')
    cam.annotate_foreground=Color('yellow')
    cam.start_preview()
    sleep(3)
    cam.capture('/home/pi/Desktop/img.jpg')
    cam.stop_preview()
    
    
def cvrotation(img,angle):
    (h,w)=img.shape[:2]
    center=(w/2,h/2)
    
    m=cv2.getRotationMatrix2D(center,angle,1)
    return cv2.warpAffine(img,m,(w,h))

def O():

    cam=cv2.VideoCapture(0)
    cam.set(3,640)
    cam.set(4,480)
    
    while (cam.isOpened()):
        ret,frame=cam.read()
        
        if not ret:
            break
        
        frame=cvrotation(frame,180)
        frame=cv2.flip(frame,0)
        cv2.imshow('phote',frame)
        
        Key=cv2.waitKey(1)&0xFF
        if Key==ord('q'):
            break
        elif Key==ord('c'):
            cv2.imwrite('/home/pi/Desktop/img1.jpg',frame)
            break
        
    cam.release()
    cv2.destroyAllWindows()

if __name__=='__main__':
    #P()
    O()