import cv2
import glob

dataPath = '../data/'
outFolder = '../temp/'

files = sorted(glob.glob(dataPath+'video/*.mp4'))

stream = cv2.VideoCapture(files[2])
print(files[2])

i = 0
while stream.isOpened():
    i +=1
    # Read frame
    ret, frame = stream.read()
    if not ret:
        break
    
    cv2.imwrite(outFolder+str(i)+'.png', frame)
    if i % 20 == 0:
        print(str(i))
        
stream.release()