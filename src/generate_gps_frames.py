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
picturePath = '../video_frames/17/'
camera_gps = [32.70297,	-117.234631]
file = '17'

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
# TODO(sjwhitak): The first few frames are not found due to 'estimated_time' 
# column in the 
individual_frames = [np.sum(frames)//len(frames) for frames in matched_frames]


# Remove additional frames
_,unique_mask = np.unique(individual_frames, return_index=True)
stacked_data = np.hstack((np.expand_dims(individual_frames,1), gps))[unique_mask]

# Reduce count by 1/3rd
stacked_data = stacked_data[::3]

# Revert stack and map to string
individual_frames = stacked_data[:,0].astype('int')
gps = stacked_data[:,1:]
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

