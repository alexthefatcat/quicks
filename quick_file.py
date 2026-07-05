# -*- coding: utf-8 -*-
"""Created on Tue Nov  7 14:18:58 2023@author: alexm

is_files_identical(fp1,fp2)
find_identical_files(fps)
remove_empty_folders(folderpaths)
get_file_table


"""
import os

# from quick_file import read_textfile, save_textfile, modify_textfile, get_files, get_subfiles, create_files_move_dic

def __get_file_extension(filepath):
    folder, filename = os.path.split(filepath)
    filename_parts = filename.rsplit('.',1)
    if len(filename_parts)==1:
        return ''
    return '.'+filename_parts[1]    

__function_type = type(lambda : None)


def read_textfile(fp, keep_newlines=True):
    if isinstance(fp, (list, tuple)):
        return {f:read_textfile(f, keep_newlines) for f in fp}
    elif isinstance(fp, str):
        with open(fp) as fo:
             if keep_newlines:
                 return fo.readlines()
             return fo.read().splitlines()           
             
       
        

def save_textfile(fp, text):
    if isinstance(text, (list, tuple)):
        if not all([('-'+l)[-1]=='\n' for l in text ]):
            text = [l+'\n' for l in text]
        text = ''.join(text)
    
    with open(fp, 'w') as fo:
        fo.write(text)


def modify_textfile(fp, func_line=None, func_text=None):
    text = read_textfile(fp)
    if func_line is not None:
        try:
            text = [func_line(i,l) for i,l in enumerate(text)]
        except:
            text = [func_line(l) for l in text]            
    if func_text is not None:
        text = func_text(text)
    save_textfile(fp, text)
    





if True:# combine these four
        # file order & what to do about empty files

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
        
        def get_files(folder, include_folders=True):
            files = [os.path.join(folder, f) for f in os.listdir(folder)]
            if not include_folders:
                files = [f for f in files if os.path.isfile(f)]
            return files
        
        
        
        
        
        def get_subfiles__pretty_text(folder, indent_str = '   ', folder_pattern = '<{}>'):
            '''
            Returns a string of all the subfiles in a folder in a nice pretty format
            '''
        
            def find_loc_of_first_disagreanent_two_lists(lisa,lisb):
                for i, (a,b) in enumerate(zip(lisa,lisb)):
                    if a!=b:
                        return i
                return min(len(lisa),len(lisb))
        
            # creating nice file list
            def get_identical_prefix(*msgs):
                out = ''
                for p in zip(*msgs):
                    if len(set(p))>1:
                        break
                    out = out+p[0]
                return out    
        
            if isinstance(folder, str):
                filess = get_subfiles(folder)
            elif isinstance(folder, (list, tuple)):
                print('Assuming the list youve given is a list of filenames to prettify')
                filess = folder
            else:
                assert False, 'folder should be a string(filepath)'
            
            f1,f2 = filess[0], filess[-1]
            base,_ = get_identical_prefix(f1,f2).rsplit('\\',1)
            base = base+'\\'
            out = [base]    
            
            folderlocs2 = []
            for f in filess:
                f0 = f.removeprefix(base)
                *folderlocs,f1 = f0.split('\\')
                depth = 1+len(folderlocs)
                
                # find a newly seen folder
                iloc = find_loc_of_first_disagreanent_two_lists(folderlocs, folderlocs2)
        
                # add newly seen folders to list
                for i, folderloc in enumerate(folderlocs):
                    if i>=iloc:
                        indent = (i+1) * indent_str
                        out.append(indent+ (folder_pattern.replace('{}', folderloc)))
                            
                # add file to list
                indent = depth * indent_str
                out.append(indent+f1)
                
                folderlocs2 = folderlocs
            files_text = '\n'.join(out)
            return files_text
        

        # works
        def convert_pretty_to_filepaths(files_pretty, indent_str = '   '):
            #quicks_functional
            def find_first(lis):
                for i,e in enumerate(lis):
                    if e:
                        return i        
            out = []
            for i, line in enumerate(files_pretty.split('\n')):  
                if i ==0:
                    current_dir = line.rstrip('\\').split('\\')
                    base_length = len(current_dir)
                else:
                    loc = find_first([len(e)>0 for e in line.split(indent_str)])
                    filename = line[(loc*len(indent_str)):]
                    
                    if '<' in line:   #   folder_pattern = '<{}>'         
                        loc2 = base_length+loc-1
                        filename0 = filename[1:-1]
                        current_dir = current_dir[:loc2]+[filename0]  
                    else:
                        filepath = '\\'.join(current_dir+[filename,])
                        out.append(filepath)
            return out
            
        
        



















def quick_find_file(*contains, extension=None, folder = r"C:\Users\Alexm\Desktop"):
    if not os.path.exist(folder) and folder==r"C:\Users\Alexm\Desktop":
        assert False, 'put other paths here'
        
    contains0 = [e.lower() for e in contains]
    files0 = get_subfiles(folder)
    files1 = [(os.path.split(f)[-1], f) for f in files0]
    files2 = [ff for ff in files1 if all([c in ff[0] for c in contains0])]
    if extension is not None:
        if isinstance(extension,str):
            extension = [extension]
        files3 = [ff for ff in files2 if all([ff[0].endswith(ext) for ext in extension])]
    else:
        files3 = files2
    return files3
    
    
#desktop_files2 = [f for f in desktop_files if 'firefox' in os.path.split(f)[-1].lower()]







def check_all_files_exist(out):
    from os.path import isfile        
    for i,e in enumerate(out):
        if not isfile(e):
            print(i,e)
        assert isfile(e) 
    print('All files exist')














#------------------------------------------------------------------------------
# def remove_empty_folders():
#     pass


# def remove_all_files_from_folder(path, except_files = None, except_folders = None):
#     # 
#     except_files = except_files if except_files is not None else []
#     except_folders = except_folders if except_folders is not None else []    
        
#     for (dirpath, dirnames, filenames) in os.walk(path):
#         dirpath2 = (dirpath.removeprefix(path)).strip('\\')
#         parents = dirpath2.split('\\')
#         _, parent = os.path.split(dirpath)
        
#         protected_parents = set(except_folders).intersection(parents)
#         if len(protected_parents)>0:
#             continue
        
#         for filename in filenames:
#             filepath = os.path.join(dirpath, filename)
#             if filename not in except_files:
#                 os.remove(filepath)


def create_files_move_dic(filepaths, dst_folder, prefix=''):
    out = {}
    for filepath in filepaths:
        filename = os.path.split(filepath)[-1]
        out[filepath] = os.path.join(dst_folder, prefix+filename)
    return out


def quick_find_similar_unused_filepath(fp, maker=None, limit=100 ):
    import os

    if maker is None:
        # add maker in before . in filename if it has one or stick it on the end
        marker= '<>' 
        folder, filename = os.path.split(fp)
        fpa = filename.rsplit('.', 1)
        if len(fpa)<2:
            fpa.append('')
        else:
            fpa[1]='.'+fpa[1]
        fp = os.path.join(folder, marker.join(fpa))

    assert fp.count(marker)==1
    import itertools
    for i in itertools.count():
        replacement = '' if i == 0 else f'({i})'
        new_fp = fp.replace(marker, replacement)
        if not os.path.isfile(new_fp):
            return new_fp
        if i ==limit:
            return


def quick_shortcut_lnk_find(shortcut_fp):
    import win32com.client
    shell = win32com.client.Dispatch('WScript.Shell')
    shortcut = shell.CreateShortcut(shortcut_fp)
    return shortcut.Targetpath
 



def hash_file(filepath=None, data=None, quick=True, no_parts = 60, segment_size = 2_000_000, verbose=False):
    def vprint(*args, **kwargs):
        if verbose:
            print(*args, **kwargs)
    
    import os, hashlib
    
    def read_file_section(filepath, start=None, segment_size=-1):    
        with open(filepath, mode='rb') as fo:
            if start is not None:            
                fo.seek(start)
            return fo.read(segment_size)
    
    def get_data_generator(filepath, inds=None, segment_size=None):
        if inds is None:
            yield read_file_section(filepath)
        else:
            for s in inds:
                yield read_file_section(filepath, s, segment_size)
                
    def calcuate_start_of_each_part(no_parts, segment_size, file_size):
        def get_part_start(part_i, no_parts, segment_size, file_size):
            return int((file_size*(((1+2*part_i)/no_parts)) -segment_size)/2)
        return tuple([get_part_start(i, no_parts, segment_size, file_size) for i in range(no_parts)])
    
    assert calcuate_start_of_each_part(2, 0, 100) == (25, 75)
    assert calcuate_start_of_each_part(2, 10, 100) == (20, 70)   
    assert calcuate_start_of_each_part(4, 25, 100) == (0, 25, 50, 75)          
    assert (filepath, data).count(None)==1
    
    if filepath is not None:
        min_size = no_parts*segment_size
        file_size = os.path.getsize(filepath)
        if file_size<min_size or not quick:
            vprint('not quick if large, small')  
            datas = get_data_generator(filepath)
        else:
            vprint('large mode, quick if large, lots of blocks')          
            part_starts = calcuate_start_of_each_part(no_parts, segment_size, file_size)
            global inds_b
            inds_b = part_starts
            datas = get_data_generator(filepath, part_starts, segment_size)
            
    if data is not None:
        datas = [data]
        
    hasher = hashlib.sha256()             
    for data_segement in datas:
        hasher.update(data_segement)
    out = hasher.hexdigest()
    return out        
            
def quick_identical_files_check(fp1, fp2):
    return hash_file(fp1)==hash_file(fp2)

def group_identical_files(filepaths, with_hash=False, quick=True):
    def group_items(items, function):
        out = {}
        for item in items:
            key = function(item)
            out[key] = out.get(key, [])+[item]
        return out 
    
    if not quick:
        tt = group_items(filepaths, hash_file)
        if with_hash:
            return tt
        return [tuple(e) for e in tt.values()]
    
    p = group_items(filepaths, lambda fp:os.path.getsize(fp))
    p2 = {}
    for k,v in p.items():
        if len(v)==1:
            p2[(None,len(p2))] = v
        else:
            for kk,vv in group_items(v, hash_file).items():
                p2[(k,kk)] = vv
    if with_hash:                
        return p2
    return [tuple(e) for e in p2.values()]
              



















if False:
    fp = r"C:\Users\alexm\Desktop\sdfsadf sdf.txt"
    text = read_textfile(fp)
    text2 = ['>>'+l for l in text]
    fp2 = fp.replace('.', '(1).')
    save_textfile(fp2, text2)
if False:
    modify_textfile(r"C:\Users\alexm\Desktop\sdfsadf sdf.txt", lambda i,x: ('<< ' if i==0 else '>> ')+x)
    modify_textfile(r"C:\Users\alexm\Desktop\sdfsadf sdf.txt", lambda x: '-- '+x)
    modify_textfile(r"C:\Users\alexm\Desktop\sdfsadf sdf.txt", None, lambda x:[l for l in x if 'a' not in l])    

if False:
    files = get_files(r"C:\Users\alexm\Desktop\DATASETS")
    files2 = get_files(r"C:\Users\alexm\Desktop\DATASETS", False)
    files3 = get_subfiles(r"C:\Users\alexm\Desktop\DATASETS")
    files4 = files3[-10_000:]





def find_textfiles(filepaths, func=None, extension='.txt'):
    assert 'IN DEVELOPMENT'
    if isinstance(filepaths, str):
        filepaths = get_subfiles(filepaths)    
    elif not isinstance(filepaths, (list,tuple)):
        assert 'Unexpected filetype'
    if extension is not None:
        if isinstance(extension, str):
            extension = [extension]
        if not isinstance(extension, (tuple, list)):
            assert 'Unexpected filetype'
        filepaths = [filepath for filepath in filepaths if __get_file_extension(filepath) in extension]
    if isinstance(filepaths, __function_type):
        pass
           








def filename_split(fp):
    "('C:\\Users\\Alexm\\Desktop\\GD\\', '_Fcw_IT2aUAApLNI-10-13-18 ', '.jpg')"
    fp = os.path.normpath(fp)
    a0,b0 = os.path.split(fp)
    a = a0+os.path.sep
    if '.' in b0:
        b,c0 = b0.rsplit('.', 1)
        c= '.'+c0
    else:
        b,c = b0, ''
    return a,b,c


def get_fileinfo(filepath):
    '''
    in the future
    hash, isfolder,  hash, 
    also when given folder given option of find all files in folder/subfolder??
    '''
    if isinstance(filepath, (list,tuple)):
        import pandas as pd
        order = ['root', 'basename', 'ext', 'parent', 'size_MB', 'size_bits', 'is_folder',
                 'created_date', 'created_time', 'modified_date', 'modified_time',
                 'accessed_date', 'accessed_time']
        out = []
        for i, filepath0 in enumerate(filepath):
            info = get_fileinfo(filepath0)
            out.append([filepath0,]+[info[k] for k in order])
        return pd.DataFrame(columns=['filepath',]+order, data=out) 
    import os, datetime, time
    root, basename, ext = filename_split(filepath)
    parent = os.path.split(root[:-1])[1]
    statinfo = os.stat(filepath)
    created_date, created_time = datetime.datetime.strptime(time.ctime(statinfo.st_ctime), "%a %b %d %H:%M:%S %Y").isoformat().split('T')
    modified_date, modified_time = datetime.datetime.strptime(time.ctime(statinfo.st_mtime), "%a %b %d %H:%M:%S %Y").isoformat().split('T')
    accessed_date, accessed_time = datetime.datetime.strptime(time.ctime(statinfo.st_atime), "%a %b %d %H:%M:%S %Y").isoformat().split('T')
    size_raw = statinfo.st_size
    is_folder = os.path.isdir(filepath)
    size_MB = round(float(statinfo.st_size)/1048576 ,4)# MB
    return dict(created_date=created_date,created_time=created_time,modified_date=modified_date,modified_time=modified_time,size_bits=size_raw,size_MB = size_MB,
                root=root, basename=basename, ext=ext, parent=parent, is_folder=is_folder,
                accessed_date=accessed_date, accessed_time=accessed_time)







if False:
    
    
    
    
    
    # Find all text files in desktop file, and read them in a dict
    print('Find all text files')

    folder = r"C:\Users\alexm\Desktop"
    files = get_subfiles(folder)
    files = [f for f in files if __get_file_extension(f) in ['.txt']]
    
    files2 = files
    files2 = [f for f in files2 if not f.startswith(r'C:\Users\alexm\Desktop\DATASETS\GRAZPEDWRI-DX-Wrist_Fractures\folder_structure\yolov5\labels') ]
    files2 = [f for f in files2 if not f.startswith(r'C:\Users\alexm\Desktop\delete after 2023-01-01\quick_wrist_run - Copy\labels\train') ]
    files2 = [f for f in files2 if not f.startswith(r'C:\Users\alexm\Desktop\delete after 2023-01-01\quick_wrist_run - Copy\labels\val') ]
    assert len(files2)<200, 'Too many files'
    
    text_files = read_textfile(files2)
    
    
    
















 
    
    