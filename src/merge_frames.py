import os 
import re 
import sys 

import numpy as np 

# TODO finish this 

if __name__ == "__main__": 
    out_dir = sys.argv[1]
    dirs = sys.argv[2:] 

    print("Merging {} into {}".format(dirs, out_dir)) 
