import numpy as np
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
    
    fd = open(fileName, 'r')
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