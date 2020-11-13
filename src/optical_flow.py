import numpy as np
import cv2 as cv
import os
import matplotlib.pyplot as plt

path = "/home/Zach/ONR/data/video/"

cap = cv.VideoCapture(path + "10.mp4")

#feature_params = dict(maxCorners = 20, qualityLevel = 0.5, minDistance = 7,  blockSize = 7)

lk_params = dict(winSize = (10, 10), maxLevel = 2, criteria = (cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03))

color = np.random.randint(0, 255, (100, 3))

ret, old_frame = cap.read()
old_gray = cv.cvtColor(old_frame, cv.COLOR_BGR2GRAY)
#pfoo = cv.goodFeaturesToTrack(old_gray, mask=None, **feature_params)

mask = np.zeros_like(old_frame)

x = 1076.
y = 433.

current_point = np.array([[[x, y]], [[113., 415.]]], dtype=np.float32)

while(1):
	ret, frame = cap.read()
	frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

	new_point, st, err = cv.calcOpticalFlowPyrLK(old_gray, frame_gray, current_point, None, **lk_params)
	#good_new = new_point[st==1]
	#good_old = current_point[st==1]
	"""
	for i, (new, old) in enumerate(zip(good_new, good_old)):
		a, b = new.ravel()
		c, d = old.ravel()
		mask = cv.line(mask, (a, b), (c,  d), color[i].tolist(), 2)
		frame = cv.circle(frame, (a, b), 5, color[i].tolist(), -1)
	img = cv.add(frame, mask)
	"""

	cv.circle(frame, tuple(new_point[0][0]), 10, (0, 255, 255), -1)
	cv.circle(frame, tuple(new_point[1][0]), 10, (255, 0, 255), -1)

	cv.imshow('frame', frame)
	k = cv.waitKey(30) & 0xff
	if k == 27:
		break

	old_gray = frame_gray.copy()
	current_point = new_point #good_new.reshape(-1, 1, 2)


