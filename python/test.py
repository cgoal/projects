import multiprocessing as mp
import time



def loadFace(path=os.path.join(os.getcwd(),'known'),cv=False):
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

def drawName(results='',img=''):
    red=(0,0,255)
    white=(255,255,255)
    font=cv2.FONT_HERSHEY_DUPLEX
    
    if results=='' or img=='':
        return None
    
    for i in results:
        (top,right,bottom,left)=i['location']
        name=i['name']
        cv2.rectangle(img,(left,top),(right,bottom),red,2)
        cv2.rectangle(img,(left,bottom-35),(right,bottom),red,cv2.FILLED)
        cv2.putText(img,name,(left+6,bottom-6),font,1.0,white,1)
        
    return img
    


def faceDetect(checkframe='',knowfaces=''):
    
    results=[]
    result={}
    
    if checkframe!=None and knowfaces!=None:
        cf_locations=face_recognition.face_locations(checkframe)
        
        print(cf_locations)
        
        if cf_locations==None:
            print('no face detect')
            return None
        
        cf_encodings=face_recognition.face_encodings(checkframe,cf_locations)
        
        for (top,right,bottom,left), cf_encoded in zip(cf_locations,cf_encodings):
            
            for i in knowfaces:
                fname=i['name']
                
                match=face_recognition.compare_faces([i['face']],cf_encoded)
                name='UnknownPerson'
                if match[0]:
                    result={'location':(top,right,bottom,left),'name':fname}
                    break
                
            results.append(result)
            
        print(results)
        return results
    
    return None, None







class f:
    
    def __init__(self):
        pass
    
    def func(self,msg):
        return mp.current_process().name+'-'+msg

if __name__=='__main__':
    pool=mp.Pool(processes=4)
    results=[]
    t=f()
    for i in range(20):
        msg='hello %d' %(i)
        results.append(pool.apply_async(t.func,(msg,)))
        
    pool.close()
    pool.join()
    print('sub-process done')
    
    for res in results:
        print(res.get())

