import sys
import numpy as np
import pandas as pd
import datetime
sys.path.append('../')
import lib.gps

# Location of data folder
dataDir = '../data/'

# Load gpx file's data
gps, time = lib.gps.GetGPS(dataDir+'main_boat_position/onboard_gps_source2/track-93020-124147pm.gpx')


for i in range(7,22):
    # Load up first camera data
    first_camera = pd.read_csv(dataDir+'camera_gps_logs/SOURCE_GPS_LOG_'+str(i)+'_cleaned.csv', delimiter=',')
    
    camera_time = first_camera['UTC Timestamp']
    
    # Generate string of timestamps (hardcode the year, month, day)
    first_frame_time_str = '2020-9-30 '+camera_time[0]
    last_frame_time_str  = '2020-9-30 '+camera_time[len(camera_time)-1]
    
    # Convert to datetime to compare with GPS datetime
    first_frame_time = datetime.datetime.strptime(first_frame_time_str, '%Y-%m-%d %H:%M:%S')
    last_frame_time  = datetime.datetime.strptime(last_frame_time_str, '%Y-%m-%d %H:%M:%S')
    
    # Compare the time of the first frame to see if it exists in the GPS time
    first_frame_position = len(time)-np.sum(time>=last_frame_time)
    last_frame_position  = len(time)-np.sum(time>=first_frame_time)
    
    # GPS mask
    mask = np.logical_and(time>=first_frame_time, time <=last_frame_time)
    
    # Mask out the GPS time for the file
    video_gps = gps[mask]
    video_time = time[mask]
    
    # Write to numpy array
    video = np.hstack((video_gps, np.expand_dims(video_time,1)))
    
    np.save(dataDir+'cleaned_boat_gps/SOURCE_GPS_LOG'+str(i)+'.npy', video)