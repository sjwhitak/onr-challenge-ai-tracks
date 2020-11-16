"""
Grid test of the homography transform.

NOTE(sjwhitak): Videos: 17 and 8 perform poorly but every other video performs
                pretty well. This is because these videos are the boat driving
                really far away.
                
NOTE(sjwhitak): Using the RANSAC algorithm for the homography transform also
                gets better results.
"""

import sys
import numpy as np
import pandas as pd
import datetime
if '../' not in sys.path:
    sys.path.append('../')
import lib.gps as g, lib.cam, cv2, lib.cam
import os 
import glob
from neec import gps as neec_gps
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 150

dataPath = '../data/'

def homography(data, H):
    p = np.hstack((data, np.ones((data.shape[0], 1)))).T
    matrix_out = H.dot(p)
    px = matrix_out[0]/matrix_out[2]
    py = matrix_out[1]/matrix_out[2]
    return np.vstack((px,py)).T


# Grab data and transform
gps_to_vid, vid_to_gps = lib.cv.generate_homography_transform('all')









# Find complete maximum and minimum of GPS inside the video (not all of GPS)
# so that the bottom subplot can see the 
max_x = -np.inf
min_x = np.inf
max_y = -np.inf
min_y = np.inf
for file in range(7,21):
    file = str(file)
    gps_data = np.load(dataPath+'cleaned_boat_gps/SOURCE_GPS_LOG_'+file+'.npy', allow_pickle=True)
    if len(gps_data) > 0:
        if np.max(gps_data[:,0]) > max_x:
            max_x = np.max(gps_data[:,0])
    
        if np.min(gps_data[:,0]) < min_x:
            min_x = np.min(gps_data[:,0])
    
        if np.max(gps_data[:,1]) > max_y:
            max_y = np.max(gps_data[:,1])
    
        if np.min(gps_data[:,1]) < min_y:
            min_y = np.min(gps_data[:,1])


for file in range(7, 21):
    file = str(file)
    
    """ GRAB THE DATA """
    # Grab GPS data
    gps_data = np.load(dataPath+'cleaned_boat_gps/SOURCE_GPS_LOG_'+file+'.npy', allow_pickle=True)
    gps_data = gps_data[:,:-1].astype('float32')
    if len(gps_data) != 0:
    
        
        # Transformed pixels based off of the GPS
        pixels_ = lib.cv.homography_transform(gps_data, gps_to_vid)
        
        
        plt.figure()
        plt.subplot(211)
        plt.plot(pixels_[:,0], pixels_[:,1], '.')
        plt.title('Video ' + file)
        plt.xlabel('Pixels (x)')
        plt.ylabel('Pixels (y)')
        plt.xlim((-10, 1810))
        plt.ylim((-10, 730))
        plt.gca().invert_yaxis()
        plt.subplot(212)
        plt.plot(gps_data[:,0],gps_data[:,1])
        plt.xlim((min_x, max_x))
        plt.ylim((min_y, max_y))
        plt.tight_layout()
        plt.title('GPS path')
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.tight_layout()
        plt.show()        
        

gps_data, pixels = lib.cam.vid_all()  
pixels_ = lib.cv.homography_transform(gps_data, gps_to_vid)
gps_data_ = lib.cv.homography_transform(pixels, vid_to_gps)

pixel_err = np.linalg.norm( pixels_ - pixels , axis=1)
plt.figure()
plt.plot(pixel_err,'.')
plt.xlabel('Data points')
plt.ylabel('Error in magnitude of pixel range')
plt.show()

# GPS error in meters
gps_err = g.haversine(gps_data[:,1], gps_data[:,0], gps_data_[:,1], gps_data_[:,0])
plt.figure()
plt.plot(gps_err,'.')
plt.xlabel('Data points')
plt.ylabel('Error in meters of GPS')
plt.show()