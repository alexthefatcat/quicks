# -*- coding: utf-8 -*-
"""Created on Thu Jul  2 02:28:47 2026@  author: Alexm"""



from pysheet3v4 import VideoSheet, py_filepath_info
import os
import pandas as pd

filepath_info = py_filepath_info()



# GET CSV LOCATION AND CREATE IF DOES NOT EXIST

fp_script = py_filepath_info()['child_py_file']
fps = fp_script.rsplit('.',1)
fps[-1]='csv'
fp_csv = '.'.join(fps)

del fps
if not os.path.exists(fp_csv):
    print('Could not find CSV')
    columns = ['File Name','File Size','Resolution','Duration','File Path','File Size Raw','Hash Code','Hash Code30','DriveInfo','script']
    df = pd.DataFrame(columns = columns)
    df.to_csv(fp_csv, index=False)
    
class Advanced_VideoSheet:
    def __init__(self, *kwargs, **args):
        super().__init__()
        
    def batch(self,filepath_ins, folder_out):
        for i,filepath_in in enumerate(filepath_ins):
            print(f'{i}/{len(filepath_ins)}', filepath_in)
            self.videosheet_i =  VideoSheet()
            self.create(filepath_in, folder_out)

    @staticmethod
    def get_filepaths_from_folder(folder, only_video_formats=False):
        files = [os.path.join(folder, file) for file in os.listdir(folder)]
        files = [file for file in files if not os.path.isdir(file)]
        files = [file for file in files if not file.endswith('.lnk')]
        if only_video_formats:
            video_formats = ['avi', 'mkv', 'mp4', 'mpeg', 'mpg', 'wmv']
            files = [file for file in files if file.split('.')[-1].lower() in video_formats ]
        return files

    def _save(self, filepath_in, folder_out, vsheet, mdata=None):
        super()._save(filepath_in, folder_out, vsheet, mdata)               
        text_lines = [ e.split(': ', 1) for e in mdata.splitlines() ]
        columns, data = list(zip(*text_lines))
        out_df = pd.DataFrame(index=[0], columns=columns, data = [data])
        out_df.to_csv(fp_csv, mode='a', header=False, index=False)
        print('Append to csv')

        backup_dir = r"C:\Users\Alexm\Desktop\pyVideoSheets3\complete2023"
        SAVE_SECOND_COPY = True
        

        if SAVE_SECOND_COPY:
            folder = os.path.join(backup_dir, filepath_in_folder)
            if not os.path.exists(folder):
                os.mkdir(folder)
            fp2_pre = os.path.join(folder, fn)
            fp2 = find_unused_filepath(fp2_pre.replace('.vs.jpg', '<>.vs.jpg'))
            
        global vsheet2, mdata2, exif
        mdata2= mdata
        vsheet2 = vsheet
        
        

        if SAVE_SECOND_COPY and fp2 is not None:
            save_pil_image_with_metadata(fp2, vsheet, mdata)  

            
