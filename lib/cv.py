# -*- coding: utf-8 -*-
import cv2, numpy as np
from scipy import interpolate


def get_affine_points():
    gps = np.array([[  32.703545, -117.232574],
       [  32.703503, -117.23284 ],
       [  32.703453, -117.233025],
       [  32.703403, -117.233116],
       [  32.703373, -117.23314 ],
       [  32.703335, -117.233154],
       [  32.70287 , -117.23314 ],
       [  32.702682, -117.233116],
       [  32.7026  , -117.23309 ],
       [  32.702564, -117.23306 ],
       [  32.702526, -117.23296 ],
       [  32.70251 , -117.23274 ],
       [  32.702515, -117.2326  ],
       [  32.70255 , -117.232285],
       [  32.702568, -117.23225 ],
       [  32.70264 , -117.23219 ],
       [  32.702675, -117.23219 ],
       [  32.70272 , -117.23221 ],
       [  32.70275 , -117.23225 ],
       [  32.70278 , -117.23233 ],
       [  32.702763, -117.23237 ],
       [  32.702766, -117.23244 ],
       [  32.702744, -117.23252 ],
       [  32.70276 , -117.232796],
       [  32.7028  , -117.2331  ],
       [  32.70282 , -117.23319 ],
       [  32.70292 , -117.23336 ],
       [  32.702953, -117.23338 ],
       [  32.703003, -117.23338 ],
       [  32.703087, -117.23335 ],
       [  32.70311 , -117.233315],
       [  32.703117, -117.23326 ]], dtype='float32')
    
    pixels = np.array([[ 599.,  431.],
       [ 588.,  433.],
       [ 588.,  435.],
       [ 613.,  436.],
       [ 627.,  436.],
       [ 663.,  438.],
       [ 997.,  437.],
       [1117.,  435.],
       [1153.,  432.],
       [1164.,  430.],
       [1163.,  429.],
       [1141.,  428.],
       [1129.,  426.],
       [1096.,  426.],
       [1083.,  427.],
       [1050.,  427.],
       [1035.,  428.],
       [1019.,  429.],
       [1011.,  429.],
       [1004.,  430.],
       [1004.,  430.],
       [1011.,  430.],
       [1023.,  431.],
       [1035.,  432.],
       [1035.,  437.],
       [1027.,  438.],
       [ 959.,  441.],
       [ 934.,  441.],
       [ 891.,  442.],
       [ 840.,  441.],
       [ 829.,  441.],
       [ 830.,  441.]], dtype='float32')
    
    return gps, pixels

def generate_affine_transform():
    gps, pixels = get_affine_points()
    
    gps_to_vid, inliers_1 = cv2.estimateAffine2D(gps, pixels)    
    vid_to_gps, inliers_2 = cv2.estimateAffine2D(pixels, gps)
    
    return gps_to_vid, vid_to_gps, (inliers_1, inliers_2)
    
    

def frame_difference(imgList,threshold):
    """
    Parameters
    ----------
    imgList : List of individual frames [n]
    threshold : Integer
        Threshold that the pixel magnitude must exceed to return white, 
        else black

    Returns
    -------
    imgThresh : List of monocolor individual frames [n-1]
        Frames that are now black (below threshold) or white (above threshold) 
        at certain pixels as a difference between the two frames.

    """
    frame_thresh_list = []
    
    # Differences between frame 0 and frame 1
    # Then frame 1 <> frame 2, frame 2 <> frame 3, etc.
    for n in range(len(imgList)-1):
        pic0 = cv2.cvtColor(imgList[n], cv2.COLOR_BGR2GRAY)
        pic1 = cv2.cvtColor(imgList[n+1], cv2.COLOR_BGR2GRAY)
        
        # Difference of frames
        img_diff = abs(pic0.astype(np.int8) - pic1.astype(np.int8)).astype(np.uint8)
    
        # Threshold this difference
        thresh = np.full_like(img_diff, 0)
        thresh[img_diff>=threshold] = 255
        thresh[img_diff<threshold] = 0
        frame_thresh_list.append(thresh)
    
    # If it's just one frame, remove the list
    if len(frame_thresh_list) == 1:
        frame_thresh_list = frame_thresh_list[0]
        
    return frame_thresh_list

def find_contours(frame_list, area_size):
    """
    Grabs contours based off of each frame.
    
    Parameters
    ----------
    frame_list : List [n]
        The image should be denoised and thresholded for better performance.
        Each frame is generated separately from another.
    area_size : Integer
        Minimum area of pixels that the contour mapping can have

    Returns
    -------
    contours: List [n]
        List of contours determined by openCV. Each "contour" corresponds to
        a list of pixels, so 1 contour = X points, another contour = Y points.
    """
    for n in range(len(frame_list)):

        # Grab all contours
        _, contours, _ = cv2.findContours(frame_list[n], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Create bounding boxes around the contours
        boundingBoxes = [cv2.boundingRect(c) for c in contours]
        
        # Sort contours from right-to-left 
        contours, boundingBoxes = zip(*sorted(zip(contours, boundingBoxes), key=lambda b: b[1][0], reverse=True))
        
        # Only use contours greater than area_size 
        area = [cv2.contourArea(c) for c in contours]        
        contours = [c for (a,c) in zip(area,contours) if a >= area_size]
    return contours

""" Find moving object positions """
def find_coords(frame_list,area_size, H):
    """
    Grabs coordinates based off of contours in each frame.
    
    Parameters
    ----------
    frame_list : List [n]
        The image should be denoised and thresholded for better performance.
        Each frame is generated separately from another.
    area_size : Integer
        Minimum area of pixels that the contour mapping can have
    H : [3x3] numpy array
        Homography matrix to transform the contour pixels from pixel plane to
        homography plane.

    Returns
    -------
    Coordinates: Numpy array [2 x n]
        [x,y] value corresponding to the homography matrix codomain
    """
    coords = []
    
    # Look through every picture
    for n in range(len(frame_list)):

        # Find all contours 
        cnts = find_contours(frame_list, area_size)
        
        pixels = np.zeros((len(cnts),3))
        positions = np.zeros((len(cnts),3))
        # Look through every contour 
        for c in range(len(cnts)):
            
            # Find bottom-center of bounding box of contour
            (x, y, w, h) = cv2.boundingRect(cnts[c])
            pixels[c] = [x + w/2, y + h/2, 1]
            
            # Transform from pixel plane to real-world plane 
            positions[c] = H.dot(pixels[c])
            positions[c,:] /= positions[c,2]
        
        # Remove homogeneous coordinate
        positions = positions[:,:-1]
        
        # Append ice plane coordinates to list 
        coords.append(positions)
    return np.concatenate(coords)

def homography_transform(x, H):
    """
    Converts R^2 to R^2 with H, homography transform
    
    Parameters
    ----------
    x : [3 x n] numpy array
        Input locations at [x_1, y_1, 1], [x_2, y_2, 1] ...
    H : [3 x 3] numpy array
        Homography transform matrix 

    Returns
    -------
    y : [2 x n] numpy array
        Output locations at [x_1', y_1'], [x_2', y_2'] ...

    """
    y = np.zeros((len(x),3))
    for i in range(len(x)):
        y[i] = H.dot(x[i])
        y[i,:] /= y[i,2]
    return y[:,:-1]

def affine_transform(x, H):
    """
    Converts R^2 to R^2 with H, affine transform with a rotate and offset:
        y = H_{11,22}*x + H_{31,32}
    
    Parameters
    ----------
    x : [n x 2] or [2 x n] numpy array
        Input locations at [x_1, y_1, 1], [x_2, y_2, 1] ...
    H : [2 x 3] numpy array
        Homography transform matrix 

    Returns
    -------
    y : [2 x n] numpy array
        Output locations at [x_1', y_1'], [x_2', y_2'] ...

    """    
    rotation_matrix = H[:,:-1]
    offset_matrix = H[:,-1]
    
    try:
        # [n x 2]
        y = np.matmul(rotation_matrix,x.T).T + offset_matrix
    except:
        # [2 x n]
        y = np.matmul(rotation_matrix,x) + offset_matrix
    
    return y

