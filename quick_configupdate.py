# -*- coding: utf-8 -*-
"""Created on Mon Jul 28 01:57:33 2025@author: Alexm"""


from quick_find_filepaths import find_filepaths
import os, json
from datetime import datetime

def read_json(filepaths):
    if isinstance(filepaths, str):
        with open(filepaths, 'r') as file_obj:
            data = json.load(file_obj)
    if isinstance(filepaths, (list,tuple)):
        data = {}
        for filepath in filepaths:
            with open(filepath, 'r') as file_obj:
                data[filepath] = json.load(file_obj) 
    return data


def get_ordered_keys(dic, key_value_func=None, return_search=False):
    if key_value_func is None:
        key_value_func = lambda x: x
    values_keys_ordered = sorted(list(dic.items()), key=lambda x:key_value_func(x[1]))
    values_ordered = [key_value_func(v) for k,v in values_keys_ordered]       
    keys_ordered = [k for k,v in values_keys_ordered]   
    if return_search:
        return keys_ordered, values_ordered
    return keys_ordered

def filepath_split(filepath, filename_sep = None):
    f0,filename = os.path.split(filepath)
    filepath_parts = [f0+'\\']
    if not filename_sep is None:
        f1, filename = filename.split('{}')
        filepath_parts.append(f1)
    f2,f3 = filename.split('.')
    filepath_parts.extend([f2, '.'+f3])
    return filepath_parts
    
def find_similar_filespaths_ordered_by_date(filepath_template, sep='{}',):
    if   isinstance(filepath_template, str) and sep in filepath_template:
        filepath_parts0 = filepath_split(filepath_template, '{}')
        filepaths0 = find_filepaths(filepath_parts0[0],  subfolders=False, extension=filepath_parts0[-1]) 
        
        filepaths = []
        for filepath in filepaths0:
            filepath_parts = filepath_split(filepath)
            if filepath_parts[1].startswith(filepath_parts0[1]) and filepath_parts[-1] == filepath_parts0[-1]:
                filepaths.append(filepath)
    elif isinstance(filepath_template, ((list, tuple))):
        filepaths = list(filepath_template)
    else:
        assert False
    
    def get_datetime_string_of_filepath(filepath):
        return datetime.fromtimestamp(os.path.getmtime(filepath)).isoformat()
                
    # find most recent files
    file_paths_info = {filepath:get_datetime_string_of_filepath(filepath) for filepath in filepaths}
    file_paths_date_sorted = get_ordered_keys(file_paths_info)    
    return file_paths_date_sorted
        




# create an exmple
if False:
    filepath_template = r'C:\Users\Alexm\Pictures\fatman.json'
    data = dict(version=3.1, tabs=[1,2,3,4,5,6])
    with open(filepath_template, 'w') as file_obj:
        json.dump(data, file_obj, indent=4)
    with open(filepath_template, 'r') as file_obj:
        data2 = json.load(file_obj)
    






#find relevent files and order by date
filepath_template = r'C:\Users\Alexm\Pictures\fatman{}.json'
filepaths_datetime_sorted = find_similar_filespaths_ordered_by_date(filepath_template)

# find most recent version by version key
file_datas = read_json(filepaths_datetime_sorted)
file_paths_version_sorted, verions = get_ordered_keys(file_datas, lambda x:x['version'], return_search=True)

#sorted smaller first, dates and version that are smaller are older
most_oldest, *_ , most_recent = filepaths_datetime_sorted
most_oldest, *_ , most_recent = file_paths_version_sorted

print(file_datas)

data = file_datas[most_recent]


data['version'] = max(verions)+1



with open(most_oldest, 'w') as file_obj:
    json.dump(data, file_obj, indent=4)





class ConfigJSONManager:
    def __init__(self, filepaths, version_key=None, verbose=True):
        if version_key is None:
            print('Versainlity will use the date of the files, it is receomend to use a key in the dict like "version"')
        # if version_key is None use date
        pass
    


file_paths = ['C:\\Users\\Alexm\\Pictures\\fatman - Copy.json', 'C:\\Users\\Alexm\\Pictures\\fatman.json']

config_handler = ConfigJSONManager(file_paths)

'config_session1_A'
'config_session1_B'
'config_session2_A'
'config_session2_B'



























