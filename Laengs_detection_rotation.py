# -*- coding: utf-8 -*-
"""
Spyder Editor
This is programmed by Chenwei Piao.
Opencv Version 4.1.2
Python Version  3.7.5
"""
import numpy as np
import cv2
import os
from PIL import Image
from skimage import io
import shutil


path = '/Users/shinwee/Desktop/projekt/Gefügebilder/'

def dobinaryzation(img):
    '''
    二值化处理函数
    '''
    maxi=float(img.max())
    mini=float(img.min())

    x=maxi-((maxi-mini)/2)
    #二值化,返回阈值ret  和  二值化操作后的图像thresh
    ret,thresh=cv2.threshold(img,x,255,cv2.THRESH_BINARY)
    #返回二值化后的黑白图像
    return thresh

def subimage(image, center, theta, width, height):

   ''' 
   根据theta 旋转图片image
   根据rect的旋转方向，顺时针/逆时针旋转
   以中心为基准，用width和height 来剪切图片
   '''
   # Uncomment for theta in radians
   #theta *= 180/np.pi
   #width 和 height 比较大小，因为minAreaRect得到的矩形宽和高数值大小不一定标准
   #根据theta顺时针/逆时针旋转
   if(height > width):
       width,height = height,width
   if(abs(theta)>45):
       theta = 90 - abs(theta)
   shape = ( image.shape[1], image.shape[0] ) # cv2.warpAffine expects shape in (length, height)
   
   matrix = cv2.getRotationMatrix2D( center=center, angle=theta, scale=1 )
   image = cv2.warpAffine( src=image, M=matrix, dsize=shape )

   x = int( center[0] - width/2  )
   y = int( center[1] - height/2 )
   width = int(width)
   height = int(height)

   image = image[ y:y+height,x:x+width ]

   return image

def image_preprocess(im):
    # translate to BGRGRAY
    gray_img=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    # Binary
    binaryimg=dobinaryzation(gray_img)
    
    # noise delete
    kernel=np.ones((11,19),np.uint8)
    openingimg=cv2.morphologyEx(binaryimg,cv2.MORPH_OPEN,kernel)
    kernel=np.ones((15,23),np.uint8)
    closingimg=cv2.morphologyEx(openingimg,cv2.MORPH_CLOSE,kernel)
    kernel=np.ones((23,25),np.uint8)
    closingimg=cv2.morphologyEx(closingimg,cv2.MORPH_CLOSE,kernel)
    
    # contours finding
    # RETR_EXTERNAL 只检测外轮廓
    # CHAIN_APPROX_SIMPLE 压缩水平方向，垂直方向，对角线方向的元素，保留该方向的终点坐标
    # cv2.findContours()函数返回两个值，一个是轮廓本身，还有一个是每条轮廓对应的属性
    contours,hierarchy = cv2.findContours(closingimg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    c = sorted(contours, key=cv2.contourArea, reverse=True)[0]
    # returns a Box2D structure which contains following detals - ( center (x,y), (width, height), angle of rotation )
    rect = cv2.minAreaRect(c)
    #print(rect)
    box = np.int0(cv2.boxPoints(rect))
    
    # 绘制轮廓
    # -1绘制所有轮廓
    # 红色(0, 0, 255)
    # 3粗细
    cv2.drawContours(im, [box], -1, (0, 0, 255), 3)
    cv2.imshow('contour figure',im)
    
    
    #crop in original image
    Xs = [i[0] for i in box]
    Ys = [i[1] for i in box]
    x1 = min(Xs)
    x2 = max(Xs)
    y1 = min(Ys)
    y2 = max(Ys)
    hight = y2 - y1
    width = x2 - x1
    cropimg = im[y1:y1+hight, x1:x1+width]
    cv2.imshow('Original Crop',cropimg)
    
    
    #subimage after rotation and croping
    r_img = subimage(im,rect[0],rect[2],rect[1][0],rect[1][1])
    return r_img



im = cv2.imread(path + 'Probe1_längs.jpg')
r_img = image_preprocess(im)
cv2.imshow('rotation image längs',r_img)



    
'''
# 创建文件夹存储所有剪切后图片   
if not os.path.exists(path):
    print("false path")
if not os.path.exists(path + 'laengs'):
    os.mkdir(path + 'laengs')
for dirpath, dirnames,filenames in os.walk(path, topdown = False):
        for filename in filenames:
            fullPath = [os.path.join(dirpath,filename) for  filename in os.listdir(path) if filename.endswith('ngs.jpg')]
for i in range(len(fullPath)):
    shutil.copy(fullPath[i] ,path+'laengs')
    
if not os.path.exists(path + 'laengsCrop'):
    os.mkdir(path + 'laengsCrop')
for dirpath, dirnames,filenames in os.walk(path + 'laengs', topdown = False):
        for filename in filenames:
            image = cv2.imread(os.path.join(dirpath,filename))
            r_img = image_preprocess(image)
            cv2.imwrite(os.path.join(path + 'laengsCrop','%s.png'%(filename)),r_img)

'''           
  
#for i in range(len(fullPath)):
#    image = cv2.imread(fullPath[i])
#    array_of_images.append(image)
#coll = io.ImageCollection(array_of_images,load_func=image_preprocess)    
#    #cv2.imwrite(os.path.join(path_write,'%s' %(filenames),coll[i])
#
#for i in range(len(coll)):
#    cv2.imwrite(os.path.join(path_write,'Croplaeng'+np.str(i+1)+'.png'),coll[i])

#imlist = [os.path.join(path,f) for f in os.listdir(path) if f.endswith('ngs.jpg')]
#print(len(imlist))

#oll = io.ImageCollection(imlist,load_func=image_preprocess) 
  
cv2.waitKey(0)
cv2.destroyAllWindows()
