import os
import json
import tarfile
import subprocess
import rasterio
import cv2

import sys
sys.path.append('/home/vri/Projects/research/Flood-detection')

from utils import utils_dirs


#----------------
# PREPROCESS DATASET
#   - remove null vals
#-------------


band_list = ['B02.tif' , 'B03.tif' , 'B04.tif' , 'B08.tif']
ROOT_DIR = '../data/transformer_data/sen12floods_s2_source'

flist = utils_dirs.get_img_folders(lag='total', root_path = ROOT_DIR)
utils_dirs.create_image(flist)

utils_dirs.get_img_folders(flag='valid', root_path = ROOT_DIR)