import os 
import re 
import sys 

import numpy as np 

def get_yolo_files(prefix: str, start: int, end: int, digits: int): 
    out = [] 

    for i in range(start, end+1): 
        f = "{0}{2:0{1}d}.txt".format(prefix, digits, i)
        if os.path.isfile(f): 
            out.append((i, f)) 

    return out 

def get_requested_yolo_files(prefix: str, start: int, end: int, digits: int): 
    out = [] 

    for i in range(start, end+1): 
        f = "{0}{2:0{1}d}.txt".format(prefix, digits, i)
        out.append((i, f)) 

    return out 

def get_yolo_boxes(files: list): 
    """
    use output of `get_yolo_files`, only uses first box for now 
    """
    out = [] 

    for i, filename in files: 
        f = open(filename)
        line = f.readline() 
        f.close() 

        words = line.split() 
        target = int(words[0]) 
        x = float(words[1]) 
        y = float(words[2]) 
        w = float(words[3]) 
        h = float(words[4]) 
        a = np.array([target, x, y, w, h])
        out.append(a) 

    return out 

def lerp_yolo_files(files: list, out_files: list): 
    """
    use output of `get_[requested_]yolo_files`, only uses first box for now 
    """ 
    start = files[0][0]
    end = files[-1][0]
    print("Interpolating bounding box between frame {} and {}".format(start, end))

    boxes = get_yolo_boxes(files) 

    out_i = 0 
    for i in range(len(files) - 1): 
        ind_s, filename = files[i] 
        ind_e, filename = files[i+1] 
        r = ind_e - ind_s
        save_yolo_box(out_files[out_i][1], boxes[i]) 
        out_i += 1

        for j in range(ind_s+1, ind_e): 
            x = (j - ind_s) / r

            box = boxes[i] * (1-x) + boxes[i+1] * x 

            save_yolo_box(out_files[out_i][1], box) 
            out_i += 1

    save_yolo_box(out_files[out_i][1], boxes[-1]) 

def save_yolo_box(filename: str, box: np.ndarray): 
    f = open(filename, "w+") 
    f.write("{} ".format(int(box[0] + 0.5))) # round in case of lerp errors 
    for i in range(1, 4+1): 
        if i != 1: 
            f.write(" ") 
        f.write("{:0.6f}".format(box[i]))
    f.close()  

if __name__ == "__main__": 
    file_s = sys.argv[1][:-4] 
    file_e = sys.argv[2][:-4]
    out_dir = sys.argv[3]

    print("Starting at {}".format(file_s)) 
    print("Ending at {}".format(file_e)) 
    print("Saving boxes at {}".format(out_dir))

    try: 
        os.makedirs(out_dir)
    except: 
        pass 

    ind_s = re.search(r'\d+$', file_s).group(0)
    ind_e = re.search(r'\d+$', file_e).group(0)
    num_len = len(ind_s) 
    ind_s, ind_e = int(ind_s), int(ind_e) 

    prefix = file_s[:-num_len]

    files = get_yolo_files(prefix, ind_s, ind_e, num_len)

    # TODO use base file name of original images instead of assuming "img" 
    out_files = get_requested_yolo_files("{}/img".format(out_dir), ind_s, ind_e, num_len) 
    lerp_yolo_files(files, out_files) 