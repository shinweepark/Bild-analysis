# -*- coding: utf-8 -*-
"""
Spyder Editor

This is programmed by Chenwei Piao
Opencv Version 4.1.2
Python Version  3.7.5
"""
import numpy as np
import cv2

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


im = cv2.imread('/Users/shinwee/Desktop/projekt/Gefügebilder/Probe1_rund.jpg')

# convert to graysacale
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

# Obtain Hough Circles
circles = cv2.HoughCircles(closingimg,cv2.HOUGH_GRADIENT,1,
                           500,param1=30,param2=10,minRadius=450,maxRadius=550)
#print(circles)

'''
# draw the Region
# Convert circles to unit 16
circles = np.uint16(np.around(circles))
# draw the outer circle
for i in circles[0,:]:
    # Draw the outer circle on im
    cv2.circle(im,(i[0],i[1]),i[2],(0,255,0),10)
    # Draw the center of the circle on im
    cv2.circle(im,(i[0],i[1]),2,(255,0,0),10)
    cv2.putText(im, "center", (i[0] - 20, i[1] - 20),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
'''

# make Mask
mask = mask = np.zeros(im.shape[:2], dtype=np.uint8)
mask = cv2.circle(mask, (circles[0,0,0],circles[0,0,1]), circles[0,0,2], (255, 255, 255), -1)
#cv2.imshow("mask", mask)
image = cv2.add(im, np.zeros(np.shape(im), dtype=np.uint8), mask=mask)
#cv2.imshow("aftermask", image)

contours,hierarchy = cv2.findContours(closingimg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
c = sorted(contours, key=cv2.contourArea, reverse=True)[0]
rect = cv2.minAreaRect(c)
box = np.int0(cv2.boxPoints(rect))
#print(rect)
# 绘制轮廓
#【box] 轮廓信息list
# -1绘制所有轮廓
# 红色(0, 0, 255)
# 3粗细
cv2.drawContours(im, [box], -1, (0, 0, 255), 3)
cv2.imshow("Image", im)


x = int(circles[0,0,0]-circles[0,0,2])
y = int(circles[0,0,1]-circles[0,0,2])
width = int(2 * circles[0,0,2])
hight = width
cropimg = image[y:y+hight, x:x+width]

#cv2.imwrite("contoursImage2.jpg", image)
#print(len(contours))
cv2.imshow('Crop figure',cropimg)
cv2.imwrite('Crop Figure1.png',cropimg)
#print(cropimg.shape)
cv2.waitKey(0)
cv2.destroyAllWindows()
