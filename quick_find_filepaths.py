# -*- coding: utf-8 -*-
r"""Created on Tue Jan 21 12:45:00 2025
@author: Alexm



This is in development should be quick to use 






find_files

file_paths = find_filepaths(r"C:\Users\Alexm\Desktop",last_days=50, strings_in_content=('oragne',),strings_in_filepath,strings_not_in_filepath, subfolders=True, extensions='.txt')





folder_path
subfolders
last_days
extension
strings_in_content
start_date
last_date
strings_not_in_filepath

strings_in_filepath
strings_not_in_content

do ideally

from quick_find_filepaths import find_filepaths
python_files_60_days = find_filepaths(r"C:\Users\Alexm\Desktop", last_days=60, extension='.py')


better variable names:-
    mathced_file_paths
    file_paths of filepaths?
    date_start or start_date


have this in the extension options
*text = ['.txt', '.py']
*image = ['.jpg', '.jpeg', '.png']


need to check everythin works but looks good so far


In future have split as an option so the ones that failed go into a second list that is outputed



"""







def find_filepaths(folder_path, subfolders=True, last_days=None, extension=None, content_contains=None, date_start=None, date_finish=None, filepath_contains_skip = None):
    import os, time
    from datetime import datetime, timedelta
    
    def any_in(ee, eee):
        for e in ee:
            if e in eee:
                return True
        return False     
    
    if isinstance(folder_path, str): 
        filepaths = []
        if subfolders:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    filepaths.append(file_path)         
        else:
            for file in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file)
                if os.path.isfile(file_path):
                    filepaths.append(file_path) 
                
        if last_days is not None:
            now = time.time()
            time_threshold = now - int(last_days * 86400)           
            out2 = []
            for file in filepaths:
                try:
                    if os.path.getmtime(file)>= time_threshold:
                        out2.append(file)
                except FileNotFoundError:
                    out2.append(file)
            filepaths = out2
    elif isinstance(folder_path, (list, tuple)):
        filepaths = list(folder_path)
        
    if extension is not None: 
        if isinstance(extension, str):
            extension = (extension,)
        out2 = []
        for file in filepaths:
            for extension0 in extension:
                if file.endswith(extension0):
                    out2.append(file)
                    break
        filepaths = out2  
        
    if content_contains is not None:  
        if isinstance(content_contains, str):
            content_contains = (content_contains,)
        content_contains = [str(e).lower().strip() for e in content_contains]
        out2 = []
        for file in filepaths: 
            with open(file, 'r', encoding='utf-8') as text_file:
                content = text_file.read().lower()
            if any_in(content_contains, content):
                out2.append(file)   
        filepaths = out2
        
    if date_start is not None:
        date_start0 = datetime.fromisoformat(date_start).date()
        matched_file_paths = []
        for file_path in filepaths:
            date_file = datetime.fromtimestamp(os.path.getmtime(file_path)).date()
            if date_start0<=date_file:#str(date_file)
                matched_file_paths.append(file_path)
        filepaths = matched_file_paths        

    if date_finish is not None:
        date_finish0 = datetime.fromisoformat(date_finish).date()
        matched_file_paths = []
        for file_path in filepaths:
            date_file = datetime.fromtimestamp(os.path.getmtime(file_path)).date()
            if date_file<=date_finish0:#str(date_file)
                matched_file_paths.append(file_path)
        filepaths = matched_file_paths
        
    if filepath_contains_skip is not None:
        if isinstance(filepath_contains_skip, str):
            filepath_contains_skip = (filepath_contains_skip,)   
        filepath_contains_skip = [str(e).lower().strip() for e in filepath_contains_skip]

        out2 = []
        for file in filepaths:
            if not any_in(filepath_contains_skip, file.lower()):
                out2.append(file)
        filepaths = out2            
    return filepaths



if __name__ == '__main__':

    def read_files(file_paths):
        import os
        def read_file(file_path):
            with open(file_path, 'r', encoding='utf-8') as text_file:
                content = text_file.read()
            return content
        out = {}
        for file_path in file_paths:
            key = ', '.join( os.path.split(file_path)[::-1])
            value = read_file(file_path)
            out[key] = value
        return out


    if False:
        python_files_60_days = find_filepaths(r"C:\Users\Alexm\Desktop", last_days=100, extension=['.py','.txt'], content_contains='for')
    python_files_60_days = find_filepaths(r"C:\Users\Alexm\Desktop", extension=['.py','.txt'], date_start='2024-11-10')
    
    files = read_files(python_files_60_days)
    files2 = {k:v.lower().split('for') for k,v in files.items()}
    files4 = find_filepaths(r"C:\Users\Alexm", last_days=120, extension='.png', filepath_contains_skip=['AppData', r'Alexm\Downloads', 'Body_Breasts'])
    
    files5 = find_filepaths(files4, filepath_contains_skip=['OneDrive'])
    
    
    
    
