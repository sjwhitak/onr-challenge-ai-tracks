import numpy as np
import sys
if '../' not in sys.path:
    sys.path.append('../')
import lib.gps, lib.cv
import cv2
import glob

def watch_video(file_name, fps=30):
    # https://www.learnopencv.com/read-write-and-display-a-video-using-opencv-cpp-python/
    
    # Open video stream
    stream = cv2.VideoCapture(file_name)

    # Read frames while the stream is open (video not over)
    while stream.isOpened():
        ret, frame = stream.read()
        if ret:
            # Individual frames here
            cv2.imshow('Frame', frame)
            
            # Quit if you press q
            if cv2.waitKey(int(1/fps*1000)) & 0xFF == ord('q'):
                break
        else:
            break
        
    # Window clean up
    stream.release()
    cv2.destroyAllWindows()
    return True

def watch_both_videos(frame1, frame2, fps=30):
    cv2.imshow('Differences', frame1)
    cv2.imshow('Original Video', frame2)
    
    # Quit if you press q (wait 25 ms)
    if cv2.waitKey(int(1/fps*1000)) & 0xFF == ord('q'):
        stream.release()
        cv2.destroyAllWindows()

dataPath = '../data/'

files = sorted(glob.glob(dataPath+'video/*.mp4'))

# Just do the first file for now
stream = cv2.VideoCapture(files[0])

i = 0
while stream.isOpened():
    
    # Set up from first frame
    if i == 0:
        ret, frame_first = stream.read()
        if not ret:
            break
    

    # Read frames after this
    ret, frame_second = stream.read()
    if ret:
        # TODO(sjwhitak): frame_difference() does not get good results,
        # if you run "watch_both_videos()" you'll see that the boat is really 
        # really small. Having a larger threshold removes both the water and 
        # the boat itself, so it doesn't really do too much at all. 
        
        # Get the difference between two frames for object detection
        frame_thresh = lib.cv.frame_difference([frame_first, frame_second], 10)
        
        watch_both_videos(frame_thresh, frame_second, 30)

    # Move to the next frame
    frame_first = frame_second
    i += 1
        
stream.release()
cv2.destroyAllWindows()