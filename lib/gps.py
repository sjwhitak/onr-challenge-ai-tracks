def GetGPS(fileName, trackName=None):
    from datetime import timedelta
    import gpxpy
    import gpxpy.gpx
    
    fd = open(fileName, 'r')
    gpx = gpxpy.parse(fd)
    GPSList = []
    TimeList = []
    
    if trackName is None:
        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    GPSList.append([point.latitude, point.longitude])
                    
                    # UTC to EST, then remove timezone info
                    TimeList.append((point.time - timedelta(hours=4)).replace(tzinfo=None))
    else:
        i = 0
        while gpx.tracks[i].name != trackName:
            i = i + 1
        for segment in gpx.tracks[i].segments:
            for point in segment.points:
                GPSList.append([point.latitude, point.longitude])
                
                # UTC to EST, then remove timezone info
                TimeList.append((point.time - timedelta(hours=4)).replace(tzinfo=None))        
    
    return np.array(GPSList), np.array(TimeList)
