# -*- coding: utf-8 -*-
import sys
import numpy as np
if '../' not in sys.path:
    sys.path.append('../')
import cv2
import lib.cv
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 150


# Constants
dataPath = '../data/'
camera_gps = [32.70297,	-117.234631]

def generate_affine_transform(dataPath, verbose=False):
    # Grab GPS data
    data = np.load(dataPath+'cleaned_boat_gps/SOURCE_GPS_LOG12.npy', allow_pickle=True)
    
    # Grab 4 GPS points
    pts = []
    pts.append(data[5,:])
    pts.append(data[6,:])
    pts.append(data[8,:])
    pts.append(data[-2,:])
    pts = np.array(pts)
    gps = pts[:,:-1].astype('float32') # Grab only GPS points
    
    # Grab corresponding pixels to frames: 613, 1007, 1244, 3552 in video 12
    pixels = np.array([[658,439],[997,438],[1152,435],[831,443]]).astype('float32')
    
    
    if verbose:
        camera_gps = [32.70297,	-117.234631]
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

    # GPS-to-video homography transform
    gps_to_vid, inliers = cv2.estimateAffine2D(gps, pixels)
    vid_to_gps, inliers = cv2.estimateAffine2D(pixels, gps)
    
    return gps_to_vid, vid_to_gps

# Generate affine transform
gps_to_vid, vid_to_gps = generate_affine_transform(dataPath, verbose=True)

# Test affine transform
data = np.load(dataPath+'cleaned_boat_gps/SOURCE_GPS_LOG13.npy', allow_pickle=True)
gps = data[:,:-1].astype('float32')
time = data[:,-1]

vid_pts = lib.cv.affine_transform(gps, gps_to_vid)