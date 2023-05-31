import os
import json
import tarfile
import subprocess
import rasterio
import cv2

def extract_tar(SOURCE_DIR, SAVE_DIR):
    """function to extract data from a tar.gz file

    Args:
        SOURCE_DIR (path.path): path of tar file
        SAVE_DIR (path.path): path to save extracted data
    """
    SOURCE_DIR = tarfile.open(SOURCE_DIR)
    SOURCE_DIR.extractall(SAVE_DIR)
    SOURCE_DIR.close()


def is_empty_img (path):
    """ 
    Function to check if image is empty (0-filled file)

    Args:
        path (path.path): path to image subfolder

    Returns:
        bool
    """
    img = cv2.imread (path + '/B01.tif', 0)
    return True if (cv2.countNonZero(img) == 0) else False


def remove_empty_folders(path):
    """function to remove empty image subfolders (subfolders with no spectral band data)

    Args:
        path (path.path) : path to image subfolder
    """
    subprocess.run(['rm', '-r', path])
    return



def stack_bands(path, dirname, bands):
    """
    function to stack different spectral bands.
    For the scope of this project, the selected bands are: 2, 3, 4, 8 (B, G, R, Near-infrared)

    Args:
        path (path.path): path to image subfolder
        bands (list): list of bands to be stacked together.
    """
    
    try:
        with rasterio.open(f"{path}/{bands[0]}") as src0:
            meta = src0.meta
        meta.update(count = len(bands))

        with rasterio.open(f"{path}/stack.tif", 'w', **meta) as dst:
            for id, layer in enumerate(bands, start=1):
                with rasterio.open(f"{path}/{layer}") as src1:
                    dst.write_band(id, src1.read(1))
    
    except:
        print(f"{dirname} is an empty folder")
        remove_empty_folders(path)

        pass


def get_dirname(path):
    """function to retrieve dirname of image subfolder

    Args:
        path (path.path): path to image subfolder

    Returns:
        data['id'] (string): dirname of image subfolder
    """
    json_data = open (f"{path}/stac.json", "rb")
    data = json.load (json_data)

    return data['id']


def get_img_folders(flag:str, root_path):
    """iterate through root folder to get image subfolders

    Args:
        root_path (path.path): path to root directory. Defaults to ROOT_DIR.
    """
    folders_list = []
    for file in os.listdir(root_path):
        d = os.path.join(root_path, file)
        if os.path.isdir(d):
            folders_list.append(d)
    print(f"The number of {flag} image subfolders are: {len(folders_list)}")
    return folders_list



def create_image(flist):
    """function call for deleting empty subfolders, stacking bands and creating new image files for further processing

    Args:
        flist (lsit): liat of image subfolders
    """
    for fpath in flist:
        empty = is_empty_img(fpath)
        remove_empty_folders(fpath) if empty else stack_bands(fpath, get_dirname(fpath), bands=band_list)
