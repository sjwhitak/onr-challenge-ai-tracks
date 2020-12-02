import glob 
import os 
import re 
import sys 

import cv2 
import numpy as np 

out_index = 1 

def get_next_index(out_dir: str): 
    global out_index
    while os.path.isfile("{}/{:05d}.png".format(out_dir, out_index)): 
        out_index += 1 

def save_extracted_boxes(files: list, img_dir: str, out_dir: str, skip: int=10): 
    global out_index 

    for i in range(0, len(files), skip): 
        filename = files[i] 
        f = open(filename)
        line = f.readline() 
        f.close() 

        img_file = "{}/{}.png".format(img_dir, re.split(r"[/\\]", filename)[-1][:-4])

        img = cv2.imread(img_file) 

        words = line.split() 
        target = int(words[0]) 
        x = float(words[1]) 
        y = float(words[2]) 
        w = float(words[3]) 
        h = float(words[4]) 
        a = np.array([target, x, y, w, h])

        x0 = int(np.round((x - w/2) * img.shape[1])) 
        x1 = int(np.round((x + w/2) * img.shape[1])) 
        y0 = int(np.round((y - h/2) * img.shape[0])) 
        y1 = int(np.round((y + h/2) * img.shape[0])) 

        index = get_next_index(out_dir) 

        out_file = "{}/{:05d}.png".format(out_dir, out_index)

        cv2.imwrite(out_file, img[y0:y1,x0:x1]) 

        print(filename, out_file, a) 

if __name__ == "__main__": 
    in_dir = sys.argv[1] 
    img_dir = sys.argv[2]
    out_dir = sys.argv[3]

    print("Extracting boxes from {}".format(in_dir)) 
    print("Loading images from {}".format(img_dir)) 
    print("Saving subimages to {}".format(out_dir))

    try: 
        os.makedirs(out_dir)
    except: 
        pass 

    files = glob.glob("{}/*.txt".format(in_dir))

    files = [f for f in files if not f.endswith('classes.txt')]

    save_extracted_boxes(files, img_dir, out_dir) 