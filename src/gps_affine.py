# -*- coding: utf-8 -*-
"""
This python script will generate an affine transform and shows the results of
such method.

--- HOW TO USE ---
sjwhitak: (1)   You manually find GPS points that seem far apart (minimum 3).

sjwhitak: (2)   You take note of the time for those GPS points.

sjwhitak: (3)   Find the center frame that those GPS points correspond.
          Note: Your GPS time will have multiple frames ~30 or so.
                I chose the middle frame. This was done arbitrarily, but
                here is nothing that we can do about it.
                  
sjwhitak: (4)   Find where the boat is in that frame and find a point on the 
                boat you want to use as a frame.
          Note: I grabbed the center-bottom of the boat.

sjwhitak: (5)   Then, use openCV's estimateAffine2D() to generate data. 
       Warning: If your inlier array has a 0 in it, that means 
                estimateAffine2D() did NOT use that value, AKA 
                That value is BAD and you should FIX IT.
"""
import sys
import numpy as np
if '../' not in sys.path:
    sys.path.append('../')
import cv2
import lib.cv
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
from datetime import datetime as dt
import shutil
import os 
mpl.rcParams['figure.dpi'] = 150


# Constants
dataPath = '../data/'
picturePath = '../temp/'
camera_gps = [32.70297,	-117.234631]
file = '12'

""" GRAB THE DATA """
# Grab GPS data
data = np.load(dataPath+'cleaned_boat_gps/SOURCE_GPS_LOG_'+file+'.npy', allow_pickle=True)

# Grab csv data and map out datetime
csv_data = pd.read_csv(dataPath+'camera_gps_logs/SOURCE_GPS_LOG_'+file+'_cleaned.csv', delimiter=',')
camera_time = csv_data['estimated_time']
frame_time  = csv_data['Frame No.'].index.values
camera_datetime = np.array([dt.strptime(x, '%Y-%m-%d %H:%M:%S') for x in '2020-9-30 '+camera_time])



""" FILTER THE DATA """
# sjwhitak: (1) Grab GPS points
gps = data[:,:-1].astype('float32') # Grab only GPS points

# Here is the time
time = data[:,-1] # sjwhitak: (2)

# Then, go to the csv files inside the data/ directory to do --
# sjwhitak: (3)
matched_frames = [frame_time[np.where(camera_datetime == t)] for t in time]

# Grab the middle frame
individual_frames = [np.sum(frames)//len(frames) for frames in matched_frames]
individual_images = [picturePath+str(x)+'.png' for x in individual_frames]

""" OUTPUT THE DATA FOR MANUAL WORK """
# Copy files to manually add points
[shutil.copy2(image, './') for image in individual_images]


# Plot so you can see the path your boat is driving
plt.figure()
plt.plot(data[:,1], data[:,0], label='GPS data')
plt.plot(gps[:,1], gps[:,0], '.', label='Chosen GPS points')
plt.plot(camera_gps[1], camera_gps[0],'o', label='Position of camera')
plt.title('Position of points chosen for affine transform')
plt.legend()
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.ticklabel_format(useOffset=False) # Remove exponents
plt.show()


# sjwhitak: (4)
# Grab corresponding pixels to each frame in GIMP or Paint or something

# This is an example from file 12!
pixels = np.array([[599, 431],      # 94.png
                   [588, 433],      # 304.png
                   [588, 435],      # 432.png
                   [613, 436],      # 536.png
                   [627, 436],      # 563.png
                   [663, 438],      # 613.png
                   [997, 437],      # ...
                   [1117, 435],
                   [1153, 432],
                   [1164, 430],
                   [1163, 429],
                   [1141, 428],
                   [1129, 426], 
                   [1096, 426],
                   [1083, 427],
                   [1050, 427],
                   [1035, 428],
                   [1019, 429],
                   [1011, 429],
                   [1004, 430],
                   [1004, 430],
                   [1011, 430],
                   [1023, 431],
                   [1035, 432],
                   [1035, 437],
                   [1027, 438], 
                   [959, 441],
                   [934, 441],
                   [891, 442],      # ... 
                   [840, 441],      # 3498.png
                   [829, 441],      # 3552.png
                   [830, 441]]).astype('float32') # 3593.png


""" Actual homography transform """
# GPS-to-video homography transform

# TODO(sjwhitak): The transform from gps -> pixel doesn't seem to do well,
#                 but the transform from pixel -> gps works really well.
#                 Notice the difference between inliers_1 and inliers_2.
gps_to_vid, inliers_1 = lib.cv.generate_affine_transform()
vid_to_gps, inliers_2 = cv2.estimateAffine2D(pixels, gps)



# TODO(sjwhitak): Once the transform works for gps -> pixel, interpolate
#                 GPS positions for every single frame, and then generate 
#                 pixels for every single frame. Then, add them to the csv
#                 file. Use this to start up the camera bounding boxes.


# =============================================================================
# Testing above code, dont need to run it
# """ Tests """
# # Test gps -> pixel transfor
# import lib.cam
# pixels, _ = lib.cam.video_13()
# 
# file = '13'
# picturePath = '../temp2/'
# 
# """ GRAB THE DATA """
# # Grab GPS data
# data = np.load(dataPath+'cleaned_boat_gps/SOURCE_GPS_LOG'+file+'.npy', allow_pickle=True)
# 
# # Grab csv data and map out datetime
# csv_data = pd.read_csv(dataPath+'camera_gps_logs/SOURCE_GPS_LOG_'+file+'_cleaned.csv', delimiter=',')
# camera_time = csv_data['estimated_time']
# frame_time  = csv_data['Frame No.'].index.values
# camera_datetime = np.array([dt.strptime(x, '%Y-%m-%d %H:%M:%S') for x in '2020-9-30 '+camera_time])
# 
# 
# 
# """ FILTER THE DATA """
# # sjwhitak: (1) Grab GPS points
# gps = data[2:,:-1].astype('float32') # Grab only GPS points
# 
# # Here is the time
# time = data[2:,-1] # sjwhitak: (2)
# 
# # Then, go to the csv files inside the data/ directory to do --
# # sjwhitak: (3)
# matched_frames = [frame_time[np.where(camera_datetime == t)] for t in time]
# 
# # Grab the middle frame
# individual_frames = [np.sum(frames)//len(frames) for frames in matched_frames]
# individual_images = [picturePath+str(x)+'.png' for x in individual_frames]
# 
# """ OUTPUT THE DATA FOR MANUAL WORK """
# # Copy files to manually add points
# [shutil.copy2(image, './test') for image in individual_images]
# 
# 
# 
# # Get data from video 12
# gps_to_vid1, vid_to_gps1 = lib.cv.generate_affine_transform(video='both')
# gps_to_vid2, vid_to_gps2 = lib.cv.generate_affine_transform(video='12')
# gps_to_vid3, vid_to_gps3 = lib.cv.generate_affine_transform(video='13')
# 
# # Test on video 13
# gps, pixels = lib.cam.video_13()
# vid_pts = lib.cv.affine_transform(gps, gps_to_vid2[0])
# gps_pts = lib.cv.affine_transform(pixels, vid_to_gps2[0])
# =============================================================================

