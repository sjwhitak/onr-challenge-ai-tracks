import numpy as np
import pandas as pd
import datetime

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

def haversine(longitude1, latitude1, longitude2, latitude2):
    # https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
    from math import radians, cos, sin, asin, sqrt
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    out = []
    for (lon1, lat1, lon2, lat2) in zip(longitude1, latitude1, longitude2, latitude2):
        # convert decimal degrees to radians 
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    
        # haversine formula 
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a)) 
        r = 6371*1000 # Radius of earth in meters. Use 3956 for miles
        out.append(c*r)
    return np.array(out)