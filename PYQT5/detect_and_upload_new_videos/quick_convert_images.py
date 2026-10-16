# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 23:46:41 2026

@author: alexm


"""
import os
from Config import VIDEOSHEET_FOLDER
#from VideoSheet import VideoSheet 
from VideoFileManager_DetectFiles import get_files_just_in_folder

from VideoSheet.utils_pysheet3v4 import  save_pil_image_with_metadata, read_pil_image_with_metadata
from PIL import Image


def convert_mdata_string_to_dict(mdata):
    lines = [e.split(':',1) for e in mdata.splitlines()]
    return {e[0]:e[1].strip().removeprefix(e[0]+':').strip() for e in lines} 


def find_small_filepath(filepath1, folder_small='small_90x90', new_file_suffix = '.vs_small.jpg'):
    import os
    folder_1, filename1 = os.path.split(filepath1)    
    folder_2 = os.path.join(folder_1, folder_small)
    filename2 = filename1.replace('.vs.jpg', new_file_suffix)
    filepath2 = os.path.join(folder_2, filename2)
    return filepath2

def print_debug(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)

#%%  

FOLDER_SMALL = os.path.join(VIDEOSHEET_FOLDER,'small_90x90')
FOLDER_SMALL2 = os.path.join(VIDEOSHEET_FOLDER,'small2_90x90')
OVERWRITE_EXISTING = False
DEBUG = True


filepaths = get_files_just_in_folder(VIDEOSHEET_FOLDER)



for i,filepath in enumerate(filepaths):
    filepath2 = find_small_filepath(filepath)
    filepath_mid = find_small_filepath(filepath, folder_small='small2_90x90', new_file_suffix = '.mid_small.jpg')  
    
    if (not os.path.exists(filepath2)) or (not os.path.exists(filepath_mid)) or OVERWRITE_EXISTING:    
        img, mdata = read_pil_image_with_metadata(filepath)
        print_debug('Reading In File:',i,filepath)

    
    
    if not os.path.exists(filepath2) or OVERWRITE_EXISTING:
        img2 = img.resize([90, 90], Image.Resampling.LANCZOS)
        save_pil_image_with_metadata(filepath2, img2, mdata)
        print_debug('    Saving Smaller Version of VS')        
        
    if not os.path.exists(filepath_mid) or OVERWRITE_EXISTING:     
        print_debug('    Saving Smaller Version of Mid-Image')            
        mdata_dic = convert_mdata_string_to_dict(mdata)
        mid_loc = mdata_dic['Middle Image Pixel Loc']
        mid_loc = eval(mid_loc)
        img_mid = img.crop(mid_loc)
        img_mid = img_mid.resize([90, 90], Image.Resampling.LANCZOS)
        save_pil_image_with_metadata(filepath_mid, img_mid, '')    
              















    













