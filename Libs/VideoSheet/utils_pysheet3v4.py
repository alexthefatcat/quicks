# -*- coding: utf-8 -*-
"""Created on Wed Jul  1 02:54:50 2026@author: Alexm"""

from types import SimpleNamespace
from subprocess import Popen, PIPE, STDOUT
from itertools import product, accumulate 
from PIL import Image 
import os  
import datetime


colors = SimpleNamespace()
# colors.black = (0,0,0,0)
# colors.white = (0,0,255,0)
# colors.blue = (255,255,255,0)
# colors.biege = (247,247,217,0)
colors.black = (0, 0, 0, 255)
colors.white = (255, 255, 255, 255)
colors.blue  = (0, 0, 255, 255)
colors.beige = (247, 247, 217, 255)


multiply_lists = lambda l1,l2: [ e1*e2 for e1,e2 in zip(l1,l2)]


def find_unused_filepath(fp, maker='<>', limit=100 ):
    import itertools
    for i in itertools.count():
        replacement = '' if i == 0 else f'({i})'
        new_fp = fp.replace(maker, replacement)
        if not os.path.isfile(new_fp):
            return new_fp
        if i ==limit:
            return

def get_todays_date():
    from datetime import date
    today = date.today().isoformat()
    return today


def Popen2(command,decode=False): # subrocss run is meant to be better
    p = Popen(command, stdout=PIPE, stderr=STDOUT)
    p1,p2 = p.communicate()  
    if decode:
        return p1.decode(), p2.decode() #utf-8?? #other subprocess
    return p1,p2


def cut(string,start=None,finish=None,start_no=0,finish_no=0): # snip
     if start is not None:
         string = string.split(start)[start_no+1]
     if finish is not None:
         string = string.split(finish)[finish_no]
     return string
 
    
def tryify(func,default=None,args=None,kwargs=None):
    def wrapper(*args,**kwargs):
        try:
            return func(*args,**kwargs)
        except Exception:
            return default
    return wrapper    
    

def ImageConcat(images, border=3, color=colors.black, get_middle_image_ltrb=False):
    row0, col0 = images[0], [img[0] for img in images]
    nimgs = [len(row0), len(col0)]
    heights, widths = [img.height for img in col0 ], [img.width  for img in row0 ]
    *heights, hieght = accumulate([e+border for e in [0]+heights])
    *widths, width = accumulate([e+border for e in [0]+widths]) 
    if get_middle_image_ltrb:
        from math import floor
        locs = floor(nimgs[0]/2), floor(nimgs[1]/2)
        middle_image_ltrb = [widths[locs[1]], heights[locs[0]], widths[locs[1]+1]-border, heights[locs[0]+1]-border,]
        # out2 = out.crop(index)
    
    out = Image.new(images[0][0].mode, (width, hieght),color)
    for x,y in product(range(nimgs[0]), range(nimgs[1])):    
        loc =  widths[x], heights[y]
        try:
            img = images[y][x]
            if img is not None:
                out.paste(img, loc)
        except IndexError:
            pass
    if get_middle_image_ltrb:
        return out, middle_image_ltrb
    return out

def batcher(container,ngroups):
    lcontainer = len(container)
    for row in range(0,lcontainer,ngroups):
        yield container[row:min(row+ngroups, lcontainer)]


def hash_file(filename, parts = 60, seg_len = 2_000_000):
    '''
    Parameters
    ----------
    filename : Srt
        filepath of the file to find sha256[256],
        if file bigger than 120Mb finds hash of 60 
        smaller evenly spaced parts of it

    Returns
    -------
    out : Str
        hash string.
    '''
    import os, hashlib
    
    def find_location_of_small_segemnts(data_len, parts, seg_len):
        parts2 = 2*parts
        value2 = data_len/parts2
        out = []
        for e in range(parts2+1):
            mid_float = e*value2
            start = int(mid_float - (seg_len*e/(parts2)))
            if e%2==1:
                out.append(start)
        return out
    
    size = os.path.getsize(filename)
    hasher = hashlib.sha256()
    
    if size<parts*seg_len:
        inds = [[0, size]]
    else:
        inds = find_location_of_small_segemnts(size, parts, seg_len)
    
    for s in inds:
        with open(filename, mode='rb') as fin:
            fin.seek(s)
            data_small = fin.read(seg_len)
            hasher.update(data_small)
    out = hasher.hexdigest()
    return out


def get_drive_info(filepath):
    ''' if a single ".name" file is in the highest directory it will grab the path to this
    the name often explain the devices info
    like: 'C:\\Dell-XPS_2019_2in1_PC.name'
    '''
    import os
    drive0 = os.path.splitdrive(filepath)[0]
    drive = drive0+'\\'
    p = os.listdir(drive)
    pp = [e for e in p if e.endswith('.name')]
    out = 'No Drive Info'
    if len(pp)==1:
        out = os.path.join(drive, pp[0])
    return out


def py_filepath_info(check=True):
    '''
    child will give you the location of the code
    parent will give you the location of the running file
    '''
    import sys, os, inspect
    
    out =  {'cwd':os.getcwd(),
            'parent_py_file':sys.argv,
             'child_py_file':inspect.getfile(lambda: None)}
    if check:
        assert 'ipykernel' not in out['child_py_file']
    return out




def save_pil_image_with_metadata(filepath, img_pil, mdata_str, user_comment_tag_ifd = 37510):
    print(filepath, mdata_str, user_comment_tag_ifd,'***<<<***')
    if mdata_str is None:
        img_pil.save(filepath)
    else:
        exif = img_pil.getexif() 
        exif[user_comment_tag_ifd] = mdata_str
        img_pil.save(filepath, exif=exif)  

def read_pil_image_with_metadata(filepath, user_comment_tag_ifd = 37510, return_no_metadata=False):
    img_pil = Image.open(filepath, mode='r')
    if return_no_metadata:
        return img_pil
    exif = img_pil.getexif() 
    mdata_str = exif[user_comment_tag_ifd]
    return img_pil, mdata_str
 



def filepaths_date(path):
    stats = os.stat(path)
    modified = datetime.date.fromtimestamp(stats.st_mtime)
    created  = datetime.date.fromtimestamp(stats.st_ctime)
    return f'M{modified}, C{created}'
    

























