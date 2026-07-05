# -*- coding: utf-8 -*-
"""Created on Wed Jan 24 17:19:39 2024@author: Alex"""

import os

def get_subfiles(folder, except_files = None, except_folders = None, just='files'):
    #just='files' does nothing at the moment
    if isinstance(folder, (tuple, list)):
        out0 = []
        for folder0 in folder:
            out0.extend(get_subfiles(folder0, except_files = except_files, except_folders = except_folders, just=just))
        return out0
    
    file_dic = {dirpath:filenames for (dirpath, dirnames, filenames) in os.walk(folder)} 
    
    if except_folders is not None:  
        file_dic = {k:v for k,v in file_dic.items() if not any([ k.startswith(f) for f in except_folders])}
    
    if except_files is not None: 
        out = [os.path.join(k, v0) for k,v in file_dic.items() for v0 in v if v0 not in except_files]
    else:
        out = [os.path.join(k, v0) for k,v in file_dic.items() for v0 in v]
    return out


def find_similar_files(filesa, filesb):
    W  = '\033[0m'  # white (normal)
    R  = '\033[31m' # red
    # finds the one in the first list which are/arnt in the second one
    filesa_path, filesa_fn = zip(*[os.path.split(f) for f in filesa ])
    filesb_path, filesb_fn = zip(*[os.path.split(f) for f in filesb ])
    for i, filepath in enumerate(filesa):
        filea_fn = filesa_fn[i]
        if filea_fn in filesb_fn:
            index = filesb_fn.index(filea_fn)
            fileb_path = filesb[index]
            #print(i,'Match',filea_fn , filepath, fileb_path)
        else:
            print(i, 'Missing', R+filea_fn+W, filepath)


def get_pc_name(drive=None):
    import os
    if drive is None:
        drive = 'C://'
    files = os.listdir(drive)
    files = [f for f in files if f.endswith('.name')]
    if len(files)==1:
        return files[0]
    return None
        




locations = ('D:\\', r'C:\Users\Alex')

ignore = (r"C:\Users\Alex\anaconda3",
          r"C:\Users\Alex\AppData\Local\Microsoft\Edge",
          r"C:\Users\Alex\AppData\Local\Microsoft\OneDrive",
          r"C:\Users\Alex\AppData\Local\Google\DriveFS",
          r"C:\Users\Alex\AppData\Local\Mozilla\Firefox\Profiles",
          r"C:\Users\Alex\AppData\Local\Packages\Microsoft.WindowsStore_8wekyb3d8bbwe",
          r"C:\Users\Alex\AppData\Local\Packages\MicrosoftTeams_8wekyb3d8bbwe",
          r"C:\Users\Alex\AppData",
          r"C:\Users\Alex\Jedi",
          r"C:\Users\Alex\Desktop\QUICKS\.git")









from quick_file import get_fileinfo
import pandas as pd
from quick_file import read_textfile, quick_find_similar_unused_filepath
from quick_split import split_intersections



files = get_subfiles(locations, except_folders=ignore)
df = get_fileinfo(files)

filess = read_textfile(r"C:\Users\Alex\Desktop\BackupLinks\All_Files__2024-01-04.txt", keep_newlines=False)
filess = [f for f in filess if f!='' and ('Jedi' not in f)]

a,b,c = split_intersections(files,filess)
    
    
print('New files I think')
find_similar_files(files, filess)
print('\n\n\n')
print('Old Missing files shouldnt really be any')
find_similar_files(filess, files)


from quick_file import quick_find_similar_unused_filepath
from quick_todays_date import quick_todays_date


if __name__=='__main__':

    pc_name = get_pc_name()
    
    if pc_name == 'Small_PC_2023_Mini_PC.name':
        print('Save csv of all files')
        today = quick_todays_date()
        for folder in (r"C:\Users\Alex\Desktop\BackupLinks", "D:\__Backup__"):
            csv_filename = os.path.join(folder, f'All_Files__{today}.csv')
            csv_filename = quick_find_similar_unused_filepath(csv_filename)
            df.to_csv(csv_filename)
        print('saved_csv')
    
    
    if pc_name == 'Small_PC_2023_Mini_PC.name':
        print('Copy recent version of certain backup files')
    
        from shutil import copy2 as overwrite_copy
        from quick_file import quick_shortcut_lnk_find
        
        links_dir = r"C:\Users\Alex\Desktop\BackupLinks\4534_BackupFiles"    
        folders_to_copy_to = [r"D:\__Backup__\4534_BackedUp", r"C:\Users\Alex\Desktop\BackupLinks\4534_BackedUp"]   
        
        links = [os.path.join(links_dir,f) for f in os.listdir(links_dir)]
        links2 = [quick_shortcut_lnk_find(f) for f in links]
        # this will overwrite any files
        for link2 in links2:
            for folder_to_copy_to in folders_to_copy_to:
                overwrite_copy(link2, folder_to_copy_to) 
    
        
        
    
if False:

    class color_text:
        def __init__(self):
            pass
        def blue(self, text):
            pass
        def red(self, text):
            W  = '\033[0m'  # white (normal)
            R  = '\033[31m' # red
            return R+str(text)+W
        
        
    from quick_string.color_text import red
    
    red = color_text().red
    print(f'The dog was {red("red")}')









