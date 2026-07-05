# -*- coding: utf-8 -*-
"""Created on Fri Jun 12 19:08:23 2026@author: Alexm"""



import os
class getFilepathsFromDirectory:
    
    folder_dict = {'Downloads':r"C:\Users\<username>\Downloads",
                   'Pictures' :r"C:\Users\<username>\Pictures",
                   'Documents':r"C:\Users\<username>\Documents"}
    
    extensions_dict = {'Images':['.jpg','.jpeg','.png','.webp'],
                       'Video':['.mp4','.mov','.avi','.mkv','.wmv','.webm'],
                       'Text':['.text','.txt','.py'],
                       'Firefox':['.jsonlz4','.baklz4']}
    
    skip_folders_default = [r'C:\Users\<username>\AppData']
    
    def __new__(cls, root_dir, extensions='Text', subfolders=True, verbose=True, skip_folders=None):#, generator=True
        assert subfolders in (True, False, None)
        
        if skip_folders is None:
            skip_folders = []
        if isinstance(skip_folders, str):
            skip_folders = [skip_folders]
        skip_folders = list(skip_folders)+cls.skip_folders_default
        skip_folders = [cls._fillUsernameInFilepath(e) for e in skip_folders]  
        
        if isinstance(extensions, str):
            extensions = cls.extensions_dict.get(extensions.title(), extensions)  
        
        if verbose:
            args = (root_dir, extensions)
            print(f'getFilepathsFromDirectory({args[0]}, {args[1]}): \n\t{root_dir=}, \n\t{extensions=}\n')    
                 
        if isinstance(root_dir,(tuple, list, dict)):
            for root_dir_i in root_dir:
                yield from getFilepathsFromDirectory(root_dir_i, extensions=extensions, subfolders=subfolders, verbose=False, skip_folders=skip_folders)
        else:
            root_dir = cls.folder_dict.get(root_dir, root_dir)
            root_dir = cls._fillUsernameInFilepath(root_dir)
            filepaths_generator = cls.walk2 if subfolders else cls.listdir2  
            for filepath in filepaths_generator(root_dir):
                 if not cls._is_correct_extension(filepath, extensions):
                     continue
                 if any([filepath.startswith(skip_folder) for skip_folder in skip_folders]):
                     continue  
                 yield filepath

    def _fillUsernameInFilepath(filepath_template):
        username = os.environ.get("USERNAME")
        return filepath_template.replace('<username>', username)

    def _is_correct_extension(filepath_or_name, extensions):
        if extensions is None or extensions == "*.*":
            return True
        filepath_or_name = filepath_or_name.lower()
        for extension in extensions:
            if filepath_or_name.endswith(extension.lower()):
                return True        
        return False

    def walk2(root_dir):
        for dirpath, _, filenames in os.walk(root_dir):
            for filename in filenames:
                yield os.path.join(dirpath, filename)
                
    def listdir2(root_dir):
        for filename in os.listdir(root_dir):
            yield  os.path.join(root_dir, filename)  
            
            
            
            
            
            