import lib.cv

def linspace_gps(gps_prediction,n):
    import numpy as np
    x = np.linspace(1, gps_prediction.shape[0], n) - 1
    return gps_prediction[x]
    

def main(video_path, count, camera_coordinates):
    _, vid_to_gps = lib.cv.generate_homography_transform(camera_coordinates, video='13')



if __name__ == '__main__':
    import sys
    import numpy as np
    
    if len(sys.argv) < 4:
        print("Usage:")
        print("   ./main.py [video] [count] [latitude] [longitude]")
        print("          video: path to video (str)")
        print("          count: count of GPS csv positions (int)")
        print("       latitude: Decimal latitude (float)")
        print("      longitude: Decimal longitude (float)")
        sys.exit()
    else:
        video_path = sys.argv[1]
        count = int(sys.argv[2])
        camera_coordinates = np.array([float(sys.argv[3]), float(sys.argv[4])])
        
        main()