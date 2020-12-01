# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 19:27:45 2020
yoloV4 Install script
@author: Evan
"""

#check what GPU is available and use the appropriate compute capability. For the 
#Jetson TX2, I'm not sure...
!nvidia-smi
# Change the number depending on what GPU is listed above, under NVIDIA-SMI > Name.
# Tesla K80: 30
# Tesla P100: 60
# Tesla T4: 75
%env compute_capability=75

!git clone https://github.com/AlexeyAB/darknet


%cd darknet


!sed -i 's/OPENCV=0/OPENCV=1/' Makefile
!sed -i 's/GPU=0/GPU=1/' Makefile
!sed -i 's/CUDNN=0/CUDNN=1/' Makefile
!sed -i 's/CUDNN_HALF=0/CUDNN_HALF=1/' Makefile


# make darknet (builds darknet so that you can then use the darknet executable file to run or train object detectors)
!make



!wget https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.weights