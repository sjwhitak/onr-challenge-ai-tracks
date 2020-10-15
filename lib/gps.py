import numpy as np
def GetGPS(fileName, trackName=None):
    from datetime import timedelta
    import gpxpy
    import gpxpy.gpx
    
    fd = open(fileName, 'r')
    gpx = gpxpy.parse(fd)
    GPSList = []
    TimeList = []
    
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                GPSList.append([point.latitude, point.longitude])
                TimeList.append((point.time).replace(tzinfo=None))     
    
    return np.array(GPSList), np.array(TimeList)
