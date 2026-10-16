# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 00:32:56 2026

@author: alexm


1) simplfy 
  remove code that isnt used
  join similar functions
  combine some into UtilityFunctions
  ?use smartdic?
  ?tracker function seems useful -> debug_tools? 
  
2) Add the Smaller Image part into the stages

3) remove old


before stage 4 it only printed at the end




#So ran all stages as well as first 2 twice results of function tracker

{'get_files_in_folder': 117, 
 'get_files_just_in_folder': 4, 
 'videosheets_not_in_database': 4, 
 'get_some_videosheetdata': 3, 
 'section_1': 2, 'section_2': 2, 
 'modify_columns': 1, 
 'create_videosheets_from_video_filepaths2': 1, 
 'section_3': 1, 'section_4': 1, 
 'section_5': 1, 'section_6': 1, 
 'create_videosheets_from_video_filepaths': 0, 
 'update_database_vidoesheets': 0, 
 'print_filepaths_with_strange_characters': 0}


{'get_filespaths_from_directory': 80, 
 'videosheets_not_in_database': 2, 
 'get_some_videosheetdata': 2, 
 'modify_columns': 1, 
 'create_videosheets_from_video_filepaths': 1, 
 'section_1n': 1, 
 'section_2n': 1, 
 'section_3n': 1,
 'section_4n': 1,
 'section_5n': 1,
 'section_6n': 1, 
 
 'print_filepaths_with_strange_characters': 0,
 'section_1': 0, 
 'section_2': 0, 
 'section_3': 0, 
 'section_4': 0, 
 'section_5': 0, 
 'section_6': 0}




"""


from MultiStageTaskRunner import MultiStageTaskRunner
import sys
from PyQt5.QtWidgets import QApplication

#from VideoFileManager_DetectFiles2 import section_1, section_2, section_3, section_4, section_5, section_6
from VideoFileManager_DetectFiles2 import tracker

from VideoFileManager_DetectFiles2 import section_1n as section_1, section_2n as section_2, section_3n as section_3, section_4n as section_4, section_5n as section_5, section_6n as section_6


#from VideoFileManager_DetectFiles import sectons as section_names


import time

    
section_names = {'Stage 1: Info':None,
                   'Stage 2: Detect Any Videosheets that havent been uploaded to Database':None,
                   "Stage 3: Find All Files on Folders":None,
                   "Stage 4: Check if Videos Found have already been found in databse":None,
                   "Stage 5: Process Videosheets of Missing VideoFiles":None,
                   'Stage 6: Upload these extra videosheets to the databse':None}
            
        
     




def section_1a(msg, shared_scope): 
    shared_scope.color_textbox = lambda *args:None
    yield from section_1(msg, shared_scope)


def section_2a(msg, shared_scope): 
    shared_scope.color_textbox = lambda *args:None
    yield from section_2(msg, shared_scope)

def section_3a(msg, shared_scope):
    print("Starting pause...")
    time.sleep(10)  # Pauses execution for 10 seconds
    print("10 seconds passed!")    
    shared_scope.color_textbox = lambda *args:None
    yield from section_3(msg, shared_scope)

def section_4a(msg, shared_scope):
    shared_scope.color_textbox = lambda *args:None
    yield from section_4(msg, shared_scope)

def section_5a(msg, shared_scope):
    shared_scope.color_textbox = lambda *args:None
    yield from section_5(msg, shared_scope)

def section_6a(msg, shared_scope):
    shared_scope.color_textbox = lambda *args:None
    yield from section_6(msg, shared_scope)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MultiStageTaskRunner([section_1, section_2, section_3a, section_4a, section_5a, section_6a], section_names)
    window.show()
    exit_code = app.exec_()
    print(tracker.get_most_used())
    session = window.shared_scope
    session0 = dict(session)
    sys.exit(exit_code)
    
    
    
    
    
    
    
    
    
    
    
    
"""



@log_purple_name
def section_1(msg):
    print('--section_1')
    df_database = update_database(VIDEOSHEET_DATABASE)
    videosheets_missing_from_database = videosheets_not_in_database(df_database)

    filepaths = get_files_in_folder(FOLDERS_TO_SEARCH)
    filepaths = list(set(filepaths))
    global filepaths_not_in_database
    filepaths_not_in_database = [filepath for filepath in filepaths if filepath not in list(df_database['File Path'])]

    msg = f'''Info:-
                {len(df_database):5}  Files found in database of Videosheets,
                {len(videosheets_missing_from_database):5}    Files(Videosheets) Found in Folder Not in Videosheet Database
                {len(filepaths_not_in_database):5}    Videos Found in Folder not in Video Database ( {len(filepaths)} Video Files Found Total)
    '''
    yield msg



get_function_parameter_names

"""











  

