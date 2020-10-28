There are 4 source files.

--- camera_frames.py ---
This is a file that computes the difference between two frames and shows the difference and original in two different windows.

--- split_gps.py ---
This file requires you download both:
   1. main_boat_position
   2. camera_gps_logs
from the Google Drive. This script will take the .txt file in main_boat_position and split that GPS file into the video's corresponding GPS data found inside camera_gps_logs.
Note: Read issue #1, as the .txt file is a corrupted XML file and needs to be fixed. Otherwise, comment out the line that uses that file, but your data will not be as accurate anymore.

--- split_video.py ---
The script require you download:
   1. video
This script will take an individual .mp4 file and split it into individual frames. I add this into a temp/ folder since there will be 3600 files added to the outFolder directory for a single .mp4 file.

--- gps_affine.py ---
This script requires:
   1. Download: video, main_boat_position, camera_gps_logs
   2. Run split_video.py and split the video into individual frames.
   3. Run split_gps.py and split the GPS into its corresponding videos.
This script shows you the process I used to generate the affine transform in lib/cv.py 
