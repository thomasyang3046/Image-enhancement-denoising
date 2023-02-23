# In[]
import cv2 
import numpy as np
import random
# In[]
def histogram_equalization(img): 
    g=img[:,:,0]
    b=img[:,:,1]
    r=img[:,:,2]
    his_g=np.zeros((256,),dtype=np.float16)
    his_b=np.zeros((256,),dtype=np.float16)
    his_r=np.zeros((256,),dtype=np.float16)
    height,width=img.shape[:2]
    #find histogram
    for i in range(width):
        for j in range(height):
            his_g[g[j,i]]=his_g[g[j,i]]+1
            his_b[b[j,i]]=his_b[b[j,i]]+1
            his_r[r[j,i]]=his_r[r[j,i]]+1
    
    cmf_g=np.zeros((256,),dtype=np.float16)
    cmf_b=np.zeros((256,),dtype=np.float16)
    cmf_r=np.zeros((256,),dtype=np.float16)
    buffer=1.0/(height*width)
    #histogram equalization
    #compute pmf&cmf
    for i in range(256):
        for j in range(i+1):
            cmf_g[i]+=his_g[j]*buffer
            cmf_b[i]+=his_b[j]*buffer
            cmf_r[i]+=his_r[j]*buffer
        cmf_g[i]=round(cmf_g[i]*255)
        cmf_b[i]=round(cmf_b[i]*255)
        cmf_r[i]=round(cmf_r[i]*255)
    cmf_g=cmf_g.astype(np.uint8)
    cmf_b=cmf_b.astype(np.uint8)
    cmf_r=cmf_r.astype(np.uint8)
    img1=np.zeros((512,512,3),dtype=np.uint8)
    #Remap the value into new image(img1)
    for i in range(width):
        for j in range(height):
            img1[j,i,0]=cmf_g[img[j,i,0]]
            img1[j,i,1]=cmf_b[img[j,i,1]]
            img1[j,i,2]=cmf_r[img[j,i,2]]   
    return img1
# In[]
def Gamma_corrections(img,gamma_green,gamma_blue,gamma_red):
    height,width=img.shape[:2]
    #img1=np.zeros((512,512,3),dtype=np.uint8)
    #把img的值轉給img1
    img1=np.array(img,dtype=np.uint8)  
    #do gamma_corrections
    for i in range(width):
        for j in range(height):
            img1[j,i,0]=((img[j,i,0]/255.0)**gamma_green)*255
            img1[j,i,1]=((img[j,i,1]/255.0)**gamma_blue)*255
            img1[j,i,2]=((img[j,i,2]/255.0)**gamma_red)*255
    return img1
# In[]
def salt_and_pepper(img):
    height,width=img.shape[:2]
    img1=np.zeros((512,512,3),dtype=np.uint8)
    salt=0.01
    pepper=0.99
    for i in range(width):
        for j in range(height):
            r = random.random()
            if r<salt:
                img1[i,j,:]=255
            elif r<pepper:
                img1[i,j,:]=img[i,j,:]
    return img1
# In[]
def Median_filter(img):
    height,width=img.shape[:2]
    img1=np.zeros((512,512,3),dtype=np.uint8)
    #設filter為3*3
    for i in range(width):
        for j in range(height):
            if i==0 or i==width-1 or j==0 or j==height-1:
                img1[j,i,:]=img[j,i,:]
            else:
                green=sorted(img[i-1:i+2,j-1:j+2,0].flatten('C'))
                blue=sorted(img[i-1:i+2,j-1:j+2,1].flatten('C'))
                red=sorted(img[i-1:i+2,j-1:j+2,2].flatten('C'))
                img1[i,j,0]=green[4]
                img1[i,j,1]=blue[4]
                img1[i,j,2]=red[4]
    return img1
# In[]
img=cv2.imread('dark3.jpg')
img=cv2.resize(img,(512,512))
#要使用那些效果就把'#'去掉
img2=salt_and_pepper(img)
#img1=histogram_equalization(img)
#img1=Gamma_corrections(img, 0.7,0.7,0.7)#img,g,b,r
img1=Median_filter(img2)
# In[]
cv2.imshow('before', img)
cv2.imshow('after', img1)
cv2.imshow('noise',img2)
cv2.waitKey(0)
cv2.destroyAllWindows()

