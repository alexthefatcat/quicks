# -*- coding: utf-8 -*-
"""Created on Wed Apr 24 15:35:47 2024@author: AlexmThere must be a previous version of this

I think I have done something similar to this so find that

add size, date_created, length?
"""
import os
import pandas as pd

if True:
    folderpath = r'C:\Users\Alexm\Downloads'
    extra_true = True
# def quick_filelist_dataframe(folderpath, extra_info=True):
    def get_subfiles(folder, except_files = None, except_folders = None, just='files'):
        out = []
        for (dirpath, dirnames, filenames) in os.walk(folder):
            out.extend([os.path.join(dirpath,f) for f in filenames])
    
        if except_files is not None:
            out = [l for l in out if not os.path.split(l)[-1] in except_files]
    
        if except_folders is not None:
            out0 = []
            for filepath in out:
                _, *parents, fn = filepath.removeprefix(folder).split('\\')
                if not len(set(except_folders).intersection(parents))>0:
                    out0.append(filepath)
            out = out0
        return out
    
    files = get_subfiles(folderpath)
    files_df = pd.DataFrame(columns = ['filepath'], data= [[f] for f in files])
    files_df['filename'] = files_df['filepath'].apply(lambda x:x.split('\\')[-1])
    files_df['filetype'] = files_df['filename'].apply(lambda x: '' if '.' not in x else '.'+(x.split('.')[-1]))
    files_df['folder_name'] = files_df['filepath'].apply(lambda x:x.split('\\')[-2])
    files_df['folder_path'] = files_df['filepath'].apply(lambda x:x.rsplit('\\',1)[0])
    if extra_info:# add size, date_created, date_modified, hash
        pass
        
    
    
    
    
    #folders = files_df['folder_path'].value_counts()