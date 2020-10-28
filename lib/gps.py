import numpy as np
import pandas as pd
import datetime

def split_gps(dataDir):
    """
    Function of split_gps.py in src/
    """
    
    # Load gpx file's data
    gps, time = get_gps_data(dataDir+'main_boat_position/track-93020-124147pm.gpx')
    gps, time = get_gps_data(dataDir+'main_boat_position/AI Tracks at Sea High Frequency GPS_train.txt')
    
    
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
        
        # GPS mask
        mask = np.logical_and(time>=first_frame_time, time <=last_frame_time)
        
        # Mask out the GPS time for the file
        video_gps = gps[mask]
        video_time = time[mask]
        
        # Write to numpy array
        video = np.hstack((video_gps, np.expand_dims(video_time,1)))
        
        np.save(dataDir+'cleaned_boat_gps/SOURCE_GPS_LOG_'+str(i)+'.npy', video)

def get_gps_data(fileName):
    """
    Parameters
    ----------
    fileName : STRING

    Returns
    -------
    gps : [2 x n] numpy array float32
        [Latitude, Longitude]
    time : [1 x n] numpy array float32
        [UTC Time]
    """
    import gpxpy
    
    with open(fileName, 'r') as fd:
        gpx = gpxpy.parse(fd)
    GPSList = []
    TimeList = []
    
    # Note: If you have multiple tracks in this gpx file, it will combine ALL
    # the tracks together. 
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                GPSList.append([point.latitude, point.longitude])
                TimeList.append((point.time).replace(tzinfo=None))     
    
    return np.array(GPSList), np.array(TimeList)