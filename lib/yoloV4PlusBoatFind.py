# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 19:42:39 2020
imgPath
@author: Evan
"""
import os
import re
import numpy as np
import cv2

def findTargetBoat(imgPath):


    #this is the run command for yolov4 that saves the bounding boxes of each object detected 
    !./darknet detector test cfg/coco.data cfg/yolov4.cfg yolov4.weights $imgPath -ext_output > result.txt

      
      
    #now open the result file and work with it
    path='./result.txt'
    myfile=open(path,'r')
    lines=myfile.readlines()

    img = cv2.imread(imgPath)
    #loop through all detected objects
    for line in range(12,len(lines)):
        Cord_Raw=lines[line]

        Cord=re.split(r'\W+',Cord_Raw)
        #print(Cord)

        x_min=int(Cord[3])
        x_max=x_min + int(Cord[7])
        y_min=int(Cord[5])
        y_max=y_min+ int(Cord[9])

        crop_img = img[y_min:y_max, x_min:x_max]
        vidName = re.split(r'/',imgStr)
        #create cropped file name that includes all relevant information and save the cropped image
        fileNameStr = './crops/' + vidName[2] + '_' + vidName[3] + Cord[0] + Cord[1] + '_' + str(line-12) + '.png'
        #print(fileNameStr)
        cv2.imwrite(fileNameStr,crop_img)
        
        
    #clean up directory after use    
    !rm -r '/crops'
    
    #return targetXmin, targetXmax, targetYmin, targetYmax