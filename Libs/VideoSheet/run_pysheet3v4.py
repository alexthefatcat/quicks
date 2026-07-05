# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 03:07:23 2026

@author: Alexm
"""

from pysheet3v4 import VideoSheet






#2026
if True:
    filename = r"C:\Users\Alexm\Desktop\AV\MD new, tnshd - 9395 Mini Diva Homemade Sextape.mp4"
    folder_out = r"C:\Users\Alexm\Desktop\pyVideoSheets3\out"
    videosheet = VideoSheet()
    videosheet.create( filename, folder_out)
    videosheet_fp = videosheet.filename_videosheet_out
    img, mdata = videosheet.read_pil_image_with_metadata(videosheet_fp) 
    info = videosheet.infos[0]
    
    
    #images = imgs_nlis
    
assert False







if False:
    img, mdata = read_pil_image_with_metadata(r"C:\Users\Alexm\Desktop\pyVideoSheets3\out\Blade.Runner.2049.2017.1080p.10bit.BluRay.8CH.x265.HEVC-PSA.vs.jpg")                    
    assert False



 














print('Important fix this')
if False:
    videosheet_batch = VideoSheet()
    files2 = [ r"C:\Users\Alexm\Desktop\AV\_Downloaded\LT Fresh_Off_the_Bus_Scene_4__missing9mins.mp4"]
    # this file does not work
    folderpath_out='C:\\Users\\Alexm\\Desktop\\AV\\_Downloaded\\VideoSheet_2023-08-07'
    videosheet_batch.batch(files2, folderpath_out)
    
    hash_file(files2[0])
    # as below 120,b hashing is failing fix this
    #evenutally add videosheet to easyImport
    # videosheet_data
    
    
    
    
DEBUG = True
if DEBUG:
    # comment = json.dumps(dic)
    # comment = encode_pdata(comment)
    # exif = set_usercomment(exif, comment0+comment+comment_end)      
    filename = r"C:\Users\Alexm\Desktop\BBC.Adam.Curtis.HyperNormalisation.WebRip.x264-MCTV.mp4"
    #filename = r"C:\Users\Alexm\Desktop\The Gravedancers (2006) x264 720p UNRATED BRRiP {Dual Audio} [Hindi 2.0 - English 2.0] Exclusive By DREDD.mkv"    
    #filename = r"C:\Users\Alexm\Desktop\Blade.Runner.2049.2017.1080p.10bit.BluRay.8CH.x265.HEVC-PSA.mkv"
    folder_out = r"C:\Users\Alexm\Desktop\pyVideoSheets3\out"
    videosheet = VideoSheet()
    videosheet.create( filename, folder_out)
    assert False, 'Finished Single Debug'
    
filepath_in = filename
folder_name = os.path.split(folder_out)[0]

backup_dir = r"C:\Users\Alexm\Desktop\pyVideoSheets3\complete2023"




    







if __name__ == '__main__':
    
    def input_yes_or_no(msg, suffix=' (Y/N)?:  '):
        while True:
            out = input(msg+suffix).strip().lower()
            if out in ('y', 'yes', 'n', 'no'): 
                return out[0]
    def create_folder_safe(folderpath):
        if not os.path.exists(folderpath):
            os.makedirs(folderpath)
            print(f'Created Folder:"{folderpath}"')   
         
    def filepath_check(filepath):
        if filepath.count('"')==2:
            filepath = filepath.split('"')[1]
        return filepath

    
    ans = input_yes_or_no('Do you want to find videosheets of all videos in a folder')         
    if ans == 'y':
        folderpath = input(' 1): Enter filepath of folder: ').strip()
        folderpath = filepath_check(folderpath)
        
        parent_folder_name = os.path.basename(folderpath)  
        
        assert os.path.exists(folderpath), "Can't find filepath"
        assert not parent_folder_name in ('orig','old','__pycache__','old')
        assert not parent_folder_name.endswith('.py')
        
        folderpath_out_options = [os.path.join(folderpath,'VideoSheet_'+get_todays_date()),
                                  r"C:\Users\Alexm\Desktop\pyVideoSheets3\out",
                                  rf"C:\Users\Alexm\Desktop\pyVideoSheets3\_{parent_folder_name}"]
        
        for folderpath_out in folderpath_out_options:
            ans = input_yes_or_no('  2): ' +f'Save videosheet at path: "{folderpath_out}"') 
            if ans == 'y':  
                break
        else:
            folderpath_out = input('  2): ' +'Enter folderpath to create to save videosheets in: ').strip()
            folderpath_out = filepath_check(folderpath_out)  
            
        ans = 'n'    
        if os.path.exists(folderpath_out):
           ans = input_yes_or_no('  3): ' +'Skip files existing with same name') 

            
        print('\nProcessing VideoSheets')            
        print(f'\tFolderpath in : "{folderpath}"')            
        print(f'\tFolderpath out: "{folderpath_out}"')
        create_folder_safe(folderpath_out)
        
        if ans=='y':
            files_skip = [f.rsplit('.')[0] for f in os.listdir(folderpath_out) if f.endswith('.jpg')]     
        else:
            files_skip = []
        
        videosheet_batch = VideoSheet()
        files = VideoSheet.get_filepaths_from_folder(folderpath)
        
        #if debug(same_week_as = '2023-01-22'):
        if False:
            files = ["D:\AV\MK SSNI-556.mp4"]
            folderpath_out = r'C:\Users\Alexm\Desktop\pyVideoSheets3\out'
            
        files2 = [f for f in files if os.path.splitext(os.path.basename(f))[0] not in files_skip]
        videosheet_batch.batch(files2, folderpath_out)
        print('Finished')






# ' "MK SSNI-556.mp4" # this file failed'
# def date_within_week(date_str, week=7):
#     from datetime import datetime    
#     date2 = datetime.fromisoformat(date_str).date() 
#     date1 = datetime.now().date()
#     return abs((date1 - date2).days) < week 

# def debug(same_week_as):
#     v = date_within_week(same_week_as)
#     #get globals
#     DEBBUGED = True
#     if v:
#         print('Waning being debugged')
#     return v

# if debug__if_within_week_of('2023-01-22'):
#     #debug

 


