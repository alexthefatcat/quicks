# -*- coding: utf-8 -*-
"""Created on Wed Aug 19 02:44:41 2026@author: Alexm"""

import os
from VideoSheet import VideoSheet 
from quick_pandas import update_database


#%%----------------------------------------------------------------------------

def get_files_in_folder(folder_path, exts=['.avi','.mp4']):
    if isinstance(folder_path, list):
        filepaths = []
        for folder_path_ in folder_path:
            filepaths_ = get_files_in_folder(folder_path_, exts=exts)
            filepaths.extend(filepaths_)
        return filepaths
        
    filepaths = []
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            for ext in exts:
                if filename.lower().endswith(ext):
                    filepath = os.path.join(root, filename)
                    filepaths.append(filepath)
    return filepaths


def get_files_just_in_folder(folder_path, exts=['.jpg']):
    filepaths = []
    
    # Loop through everything in the top-level folder only
    for filename in os.listdir(folder_path):
        for ext in exts:
            if filename.lower().endswith(ext):
                filepath = os.path.join(folder_path, filename)
                if os.path.isfile(filepath):
                    filepaths.append(filepath)
    return filepaths  
  
    
def modify_columns(df, first_columns, new_columns=None):#, last_columns=None):
    # df_database = modify_columns(df_database, ['File Name', 'File Size', 'Resolution','Duration','Ratings', 'Actress'])
    org_columns = list(df.columns)
    if new_columns is None:
        new_columns = []    
    for col in new_columns:
        if col not in org_columns:
            df[col] = ''
    org_columns = list(df.columns)            
    
    last_columns = [col for col in org_columns if col not in first_columns]
    return df[first_columns+last_columns]

  
#%%----------------------------------------------------------------------------
def create_videosheets_from_video_filepaths(filepaths, folder_out, verbose=False):
    new_videosheets = []
    folder_out = VIDEOSHEET_FOLDER
    for i,filepath in enumerate(filepaths):
        videosheet = VideoSheet()
        videosheet.create( filepath, folder_out)
        videosheet_fp = videosheet.filename_videosheet_out
        new_videosheets.append(videosheet_fp)
        if verbose:
            print(f' {i}/{len(filepaths)}', videosheet_fp)
    return new_videosheets



def create_videosheets_from_video_filepaths2(filepaths, folder_out): 
    folder_out = VIDEOSHEET_FOLDER
    nfiles = len(filepaths)
    for i,filepath in enumerate(filepaths):
        videosheet = VideoSheet()
        videosheet_fp = ''
        success = None
        try:
            videosheet.create( filepath, folder_out)
            videosheet_fp = videosheet.filename_videosheet_out
            success = True            
        except:
            success = False              
        
        yield (success, filepath, videosheet_fp, f'{i}/{nfiles}')


def videosheets_not_in_database(df_database):
    videosheet_filepaths = get_files_just_in_folder(VIDEOSHEET_FOLDER)
    videosheet_filepaths_entries = [videosheet_filepath for videosheet_filepath in videosheet_filepaths if videosheet_filepath not in list(df_database['Videosheet_fp'])]
    return videosheet_filepaths_entries




def get_some_videosheetdata(videosheet_fps):
    import pandas as pd
    from VideoSheet import VideoSheet
    
    if len(videosheet_fps)==0:
        return pd.DataFrame(), {}

    videosheet = VideoSheet()
    videosheets_dict = {}
    for i,videosheet_fp in enumerate(videosheet_fps):
        img, mdata = videosheet.read_pil_image_with_metadata(videosheet_fp)
        videosheets_dict[videosheet_fp] = mdata

    for i,(k,v) in enumerate(videosheets_dict.items()):
        text = v.splitlines()
        cols, vals = [], []
        for line in text:
            col, val = line.split(':',1)
            col, val = col.strip(), val.strip()
            cols.append(col)
            vals.append(val)
        if i == 0:
            df = pd.DataFrame(columns=cols)
        for col, val in zip(cols, vals):
            df.loc[i,col] = val  
        df.loc[i, 'Videosheet_fp'] = k
        
    df['Middle Image Pixel Loc'] = df['Middle Image Pixel Loc'].apply(lambda x:x.split(':')[-1].strip())    
    first_columns = ['File Name', 'File Size', 'Resolution','Duration','Ratings', 'Actress']
    new_columns = [ 'Tags','Ratings','Actress']
    df = modify_columns(df, first_columns, new_columns)
    return df, videosheets_dict





#%%----------------------------------------------------------------------------
def update_database_vidoesheets():
    #desktop = os.path.join(os.path.expanduser("~"), "Desktop")

    print('Stage 1: Find Filepaths of videos in folder')
    filepaths = get_files_in_folder(FOLDERS_TO_SEARCH)
    filepaths = [filepath for filepath in filepaths if filepath.isascii()]
    filepaths_bad_names = [filepath for filepath in filepaths if not filepath.isascii()]
    print(' * Bad Filepaths', filepaths_bad_names)
        
    print('Stage 2: Load Databse if exist and remove filepaths to create videosheet if already exist')
    if os.path.exists(VIDEOSHEET_DATABASE):
        print(' *Database Exists')
        df_database =  update_database(VIDEOSHEET_DATABASE)
        filepaths_not_in_database = [filepath for filepath in filepaths if filepath not in list(df_database['File Path'])]
        filepaths = filepaths_not_in_database
        videosheet_filepaths_entries = videosheets_not_in_database(df_database)
        df_new,*_ = get_some_videosheetdata(videosheet_filepaths_entries)
        df_database =  update_database(VIDEOSHEET_DATABASE, df_new)

    try:
        new_videosheets = create_videosheets_from_video_filepaths(filepaths, folder_out=VIDEOSHEET_FOLDER, verbose=True)
        df_new,*_ = get_some_videosheetdata(new_videosheets)
        df_database =  update_database(VIDEOSHEET_DATABASE, df_new)
    except:
        pass
    

        
# Someway to do this
def process():
    yield 'Start'
    try:
        for n in range(10):
            yield f'Starting {n}'
            yield f'Finished {n}'        
        yield 'Finished'
    except:
        yield 'Failed'
if False:       
    for n in process():
        print(n)
            
            
            
        
    
#%%----------------------------------------------------------------------------    
    
    


from PyQt5.QtGui import QColor, QPalette

FOLDERS_TO_SEARCH = [r'C:\Users\Alexm\Desktop\AV\_Downloaded',
                     r"C:\Users\Alexm\Desktop\AV\_Streamed"]

VIDEOSHEET_FOLDER = r"C:\Users\Alexm\Desktop\TEMP_VIDEOSHEET"
VIDEOSHEET_DATABASE = r"C:\Users\Alexm\Desktop\__Videosheet_Databse__.csv"
 
    
 
    
 
    
 
    
 
    
 
    
sectons = {'Stage Z: Info':None,
           'Stage 0: Detect Any Videosheets that havent been uploaded to Database':None,
           "Stage 1: Find All Files on Folders":None,
           "Stage 2: Check if Videos Found have already been found in databse":None,
           "Stage 3: Process Videosheets of Missing VideoFiles":None,
           'Stage 4: Upload these extra videosheets to the databse':None}
    



def section_z(msg):
    df_database = update_database(VIDEOSHEET_DATABASE)
    videosheets_missing_from_database = videosheets_not_in_database(df_database)

    filepaths = get_files_in_folder(FOLDERS_TO_SEARCH)
    filepaths_not_in_database = [filepath for filepath in filepaths if filepath not in list(df_database['File Path'])]

    msg = f'''Info:-
                {len(df_database):5}  Files found in database of Videosheets,
                {len(videosheets_missing_from_database):5}    Files(Videosheets) Found in Folder Not in Videosheet Database
                {len(filepaths_not_in_database):5}    Videos Found in Folder not in Video Database ( {len(filepaths)} Video Files Found Total)
    '''
    yield msg




def section_0(msg):
    df_database_orig = update_database(VIDEOSHEET_DATABASE)
    videosheets_missing_from_database = videosheets_not_in_database(df_database_orig)    
    msg += f'{len(df_database_orig)} Files found in database, Adding {len(videosheets_missing_from_database)} to it\n'
    yield msg           
    df_new,*_ = get_some_videosheetdata(videosheets_missing_from_database)
    df_database =  update_database(VIDEOSHEET_DATABASE, df_new)
    msg += f'{len(df_database)} Files found in database, Now'     
    yield msg     

def section_1(msg, self):
    filepaths = get_files_in_folder(FOLDERS_TO_SEARCH)
    filepaths = [filepath for filepath in filepaths if filepath.isascii()]
    filepaths_bad_names = [filepath for filepath in filepaths if not filepath.isascii()]
    msg = f'{len(filepaths)} Good Video Files found in the folders,'
    if len(filepaths_bad_names)==0:
        msg = msg+' No Bad Files where found(None Ascii)'
    else:
        msg = msg+f'{len(filepaths_bad_names)} Bad filepaths found\n\tBadFiles:-\n'+('\n\t\t'.join(filepaths_bad_names))    
    self.filepaths = filepaths
    yield msg


def section_2(msg, self):
    filepaths = self.filepaths
    
    if not os.path.exists(VIDEOSHEET_DATABASE):
        msg = 'Video Database:-\n\tNOT DETECTED ERROR'
        yield msg
        return
    msg += 'Video Database:-\n\tDETECTED\n\n'
    yield msg
    
    df_database =  update_database(VIDEOSHEET_DATABASE)
    filepaths_not_in_database = [filepath for filepath in filepaths if filepath not in list(df_database['File Path'])]
    filepaths = filepaths_not_in_database
    msg += f'{len(filepaths_not_in_database)} Files that are not present in the database\nFilesMissing:-\n\t' 
    msg += '\n\t'.join(filepaths)
    yield msg
    self.filepaths2 = filepaths  



def section_4(msg, self):
    new_videosheet_fps = self.filepaths3
    df_database_orig = update_database(VIDEOSHEET_DATABASE)
    msg += f'{len(df_database_orig)} Files found in database, Adding {len(new_videosheet_fps)} to it\n'
    yield msg            
    df_new,*_ = get_some_videosheetdata(new_videosheet_fps)
    df_database =  update_database(VIDEOSHEET_DATABASE, df_new)
    msg += f'{len(df_database)} Files found in database, Now'
    yield msg            

                












import sys
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy, QFrame,
                             QLabel, QTextEdit, QPushButton)

class MultiSectionWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        app_font = QFont("Arial", 12)        
        self.setFont(app_font)

    def init_ui(self):
        self.setWindowTitle("Three Section Layout")
        self.resize(550, 500)
        main_layout = QVBoxLayout()
        self.text_boxes = []
        self.buttons = []
        for idx, (title_text, v) in enumerate(sectons.items()):
            line = QFrame()
            line.setFrameShape(QFrame.HLine)
            line.setFrameShadow(QFrame.Sunken)

            button = QPushButton(f"Run {idx}")
            button.clicked.connect(lambda checked, i=idx: self.handle_button_click(i))  
            button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            self.buttons.append(button)                
            
            title_label = QLabel(title_text)
            title_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)                
            
            text_box = QTextEdit()
            text_box.setPlainText('')
            text_box.setLineWrapMode(QTextEdit.NoWrap)
            text_box.setReadOnly(True)
            line_height = text_box.fontMetrics().lineSpacing()
            text_box.setFixedHeight(line_height * 3 + 16)
            self.text_boxes.append(text_box)

            title2 = QWidget()
            row_layout2 = QHBoxLayout()
            row_layout2.addWidget(title_label)
            row_layout2.addWidget(button)                  
            title2.setLayout(row_layout2)
            title2.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        
            box_column = QVBoxLayout()
            box_column.addWidget(title2)
            box_column.addWidget(text_box)
            row_layout = QHBoxLayout()
            row_layout.addLayout(box_column)
            
            main_layout.addWidget(line)                
            main_layout.addLayout(row_layout)                
            main_layout.addSpacing(line_height)
            
        self.setLayout(main_layout)
        
        
    def color_textbox(self, text_box, color='red'):
        color_dict = {'green':"#d1e7dd", 'orange':"#fee9cc",
                      'red':"#ffe5d9",   'grey':"#f6f8f9",
                      'white':"#ffffff"}            
        
        palette = text_box.palette()  

        color = color_dict.get(color, "#ffffff")
        palette.setColor(QPalette.Base, QColor(color)) 
        text_box.setPalette(palette)            
        


    def handle_button_click(self, section_num):
        text_val = self.text_boxes[section_num - 1].toPlainText()
        print(f"Section {section_num} button clicked. Current text:\n{text_val}\n")
        text_box = self.text_boxes[section_num]
        msg = ''
        btn = self.buttons[section_num]
        btn.setDisabled(True)
        text_box.setPlainText('Running')
        self.color_textbox(text_box,'grey')
        section_num=section_num-1
        
        if section_num==-1:
            for msg in section_z(msg):
                print(msg)
                text_box.setPlainText(msg)
                QApplication.processEvents()  

        if section_num==0:
            for msg in section_0(msg):
                print(msg)
                text_box.setPlainText(msg)
                QApplication.processEvents()  

        if section_num==1:
            for msg in section_1(msg, self):
                print(msg)
                text_box.setPlainText(msg) 
                QApplication.processEvents()  
            self.color_textbox(text_box,'red')                


        if section_num==2:
            for msg in section_2(msg, self):
                print(msg)
                text_box.setPlainText(msg) 
                QApplication.processEvents()  
            self.color_textbox(text_box,'orange')                    
            
            
        if section_num==3:
            filepaths =self.filepaths2
            msg += f'Converting Videos to VideoSheets({len(filepaths)} Files)...\n' 
            msg2 = ''
            self.filepaths3 = []
            for success, filepath, videosheet_fp, msg_i in create_videosheets_from_video_filepaths2(filepaths, folder_out=VIDEOSHEET_FOLDER):
                filename = os.path.split(filepath)[1] 
                sucess2 = "✓" if success else "✗"
                line = f'\t{sucess2} {filename}; {videosheet_fp}; {filepath}\n' 
                msg_tmp = msg+'-'*30+'\n'+line+'-'*30+'\n'+msg2
                text_box.setPlainText(msg_tmp)
                QApplication.processEvents()
                msg2 = line + msg2
                if success:
                    self.filepaths3.append(filepath)                    
            msg +=msg2
            
        if section_num==4:
            for msg in section_4(msg, self):
                print(msg)
                text_box.setPlainText(msg) 
                QApplication.processEvents()  
            self.color_textbox(text_box,'orange')                  

        
        btn.setDisabled(False)
        content = text_box.toPlainText()
        content += '\n\t**FINISHED**'
        text_box.setPlainText(content)         




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MultiSectionWindow()
    window.show()
    sys.exit(app.exec_())
    










