# -*- coding: utf-8 -*-
"""

videofilemanager 
   1) summary total no files total length, total size; 
   2) fix black lines and scroll bar after addicationl filter 









Things To Do
   Create Shirt-cut exe default opener, so progam to open python files
   fix wierd thign where do another search and search bar is still small
   speed up the start   
   fix black lines
   grey out missing videos
   *write up some notes on what to do
   button that clicks opens other program so can add new files




import sys

    from spyder.config.manager import CONF
    spyder_paths = CONF.get('main', 'spyder_pythonpath', default=[])
    
    # Add Spyder's paths to this terminal session
    for path in spyder_paths:
        if path not in sys.path:
            sys.path.append(path)
except Exception as e:
    print(f"Could not load Spyder paths: {e}")

# Now import your custom modules
from quick_pandas import update_database










Created on Tue Aug 11 21:40:07 2026 @author: Alexm

make sure video sheets doesnt override an existing one


Where is Video
   Natalie Portman interview while sexNP 11t16821__Natalie_Portman__DeepFake_Porn_Video∆
   I thing delta throws it off rewrite detector
   
   
   looses virginity sd card
   catch schools in shower sd card






AL DeepFake - Adriana Lima DeepFake 11_11

gray out missing videos
when click image or file same one is highlighted
when you search for soemhtting and go back lines are distaorted
some black lines are now missing
have option ofright image display on the right that shows videosheets



Hides Duplicates by default

1) Drives should be easily selected like actress
2) When Searching serach box goes light red then white when finineshed
4) Autofill when filling actress
5) fix grid of images



create a dummy one
select on file image gets highltied visvera
larger image on the right
fix the problem of after search affects what happens as rows are merged?



5) Fix black lines and 6 images for 6 lines of info



black lines drawn are seperated by 138(138/6=23)



better way for print outs
warning when closing
a program to detect missing files effiently













1) fix scrolling after I do filter I guess both need to be refreshed?
2) image on the right that can be hid
3) quicker opening
4) change default program to open python files and have automatic opening





    Refesh View, Total Rows = 283<<
# [ RefreshView ] completed in 0.71s (SyncedTableGalleryWidget2.py:806)
TaskManager python 31MB


   Refesh View, Total Rows = 495<<
# [ RefreshView ] completed in 1.65s (SyncedTableGalleryWidget2.py:806)


"""



# This code is added to top of python script so taskbar sees the open file same as link
import ctypes
APP_ID = 'videofilemanager.mygui.app.1.0'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(APP_ID)





import subprocess, hashlib, os, sys
from functools import lru_cache


from print_debug import print_debug

import pandas as pd
from quick_pandas import update_database


from PyQt5.QtWidgets import QMessageBox#, QTextEditQApplication, 

from PyQt5.QtWidgets import QApplication
from  SyncedTableGalleryWidget__VideoFileManager import VideoFileManager
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMenu, QInputDialog#, QMainWindow, QTableWidget, QTableWidgetItem

from Config import VIDEOSHEET_DATABASE#, VIDEOSHEET_FOLDER, FOLDERS_TO_SEARCH

    






class UtilityFuntions:
    def __init__(self):
        pass
    def open_file_in_window_explorer(filepath):
        path = os.path.normpath(filepath)
        if os.path.exists(path):
            subprocess.run(f'explorer /select,"{path}"')
        else:
            print(f"File not found: {path}") 
            



@lru_cache(maxsize=128)
def simple_hashed_string(string):
    return hashlib.shake_128(string.encode('utf-8')).hexdigest(4)

def get_hashed_directory(filepath):
    folder,_ = os.path.split(filepath)
    return simple_hashed_string(folder)



# Default global debug flag
PRINT_DEBUG = True

def printd(*args, **kwargs):
    # 1. Check if PRINT_DEBUG is set to False in the global scope
    if not globals().get('PRINT_DEBUG', True):
        return

    # 2. ANSI escape sequence for orange and style reset
    ORANGE = "\033[38;5;208m"
    RESET = "\033[0m"

    # 3. Handle 'sep' argument (defaulting to a space)
    sep = kwargs.pop('sep', ' ')
    formatted_message = sep.join(str(arg) for arg in args)

    # 4. Print wrapped in orange formatting
    print(f"{ORANGE}{formatted_message}{RESET}"+'#printd', **kwargs)










def custom_row_function(row):
    #Example
    #| vj 11t12251 victoria justice deepfake porn video | 469mb 460mb | | 11min 12min 13min 1080 | 0:12:21 0:12:20 | vj*
    
    def duration_func(out):
        foo = out.split(':')
        foo2 = (int(foo[0])*60)+(int(foo[1]))
        return str(foo2-1)+'min '+str(foo2)+'min '+str(foo2+1)+'min'    
    part1 = ['|', row['File Name'].rsplit('.',1)[0]]
    part2 = row['File Size'].split('.')[0]
    part2 = ['|',part2+'MB', part2[:-1]+'0MB ', (part2[:-3]+'.'+ part2[-3].replace('.0','')+'GB' if len(part2)>3 else '' )]
    
    bbt = ''
    if ('Butt' in row['Tags']) or ('Tits' in row['Tags']) or ('Body' in row['Tags']):
        bbt = '<Body/Butt/Tits>'

    tags = ','.join(['<'+e+'>' for e in row['Tags'].split(',')])

    
    part3 = ['|', '<anytag>' if len(row['Tags'])>3 else '', tags, bbt, row['Actress'] ]
    part3 = [ '' if pd.isna(e) else e.replace(',',' ') for e in part3 ]    
    part4 = ['|',duration_func(row['Duration']),  str(min([int(e) for e in row['Resolution'].split('x')]))]
    
    duration_string = row['Duration']#.split(':',1)[-1]
    duration_string2 = duration_string.rsplit(':')
    duration_string2[-1] = str(int(duration_string2[-1])-1)
    duration_string2 = ':'.join(duration_string2)
    part5 = ['|', duration_string, duration_string2]
    
    filepath = row['File Path'].lower()
    part6 = ['|']
    names = ['reona','sophie','nathaly','mikae','leona','elsa']
    for name in names:
        if name in filepath:
            part6.append(name)
            
    if row['Ratings']>3:
        part6.append('**')
    
    prefix,*_ = row['File Name'].split(' ')

    if len(prefix) in [1,2,3]:
        part6.append(prefix+'*')
    prefix = prefix.replace('1','').replace('2','').replace('3','').replace('4','')   
    if len(prefix) in [1,2,3]:
        part6.append(prefix+'*')     
        
    initials_from_actress_name = (''.join([(e+' ')[0] for e in str(row['Actress']).split(' ')]))+'*'.replace(' ','')
    part6.append(initials_from_actress_name)
    
    part7 = ['|',get_hashed_directory(row['File Path'])]
    part8 =['|',str(row['File Path'])]
    
    out = [e for ee in [part1,part2,part3,part4,part5,part6,part7,part8] for e in ee]
    out = ' '.join([e for e in out if e is not None])
    out = out.replace('+>','>star123>')
    out = ''.join([e if e not in '.+-_' else ' ' for e in out ])
    out = out.replace('>star123>','+>')    
    out = ' '.join([e for e in out.split(' ') if e!=''])
    out = out.lower().strip()
    return out






class VideoFileManager(VideoFileManager):

    def info(self):
        screen_size_info = f'Moniter: {self.screen_mode};ScreenSize(W,H):-({self.screen_size[0] } X {self.screen_size[1]})'

        info = f''' 
        **   -  To Filter for 4/5 star films
        NEW* -  For Recently Added Films to the Database
        NP*  -  Initals of the Actress so for Natalie Portman 
        
        {screen_size_info}
        
        '''    
        return info
    
    
    def __init__(self, *args, **kwargs): 
        

        

                    
        
        super().__init__(*args, **kwargs)
        self.extra_notes = ['','']    

        with print_debug('Add Search Column to DataFrame'):
            self.df['Search'] = self.df.apply(custom_row_function, axis=1)
            col, nrows, val = 'Search', 40, ' new* '
            self.df.loc[self.df.index[-nrows:], col] = self.df[col].tail(nrows) + val
            
            

            
        self.check_drives_exist_of_files()        

        self.masks.duplicates = [True, ~(df_database['Hash Code30']+df_database['Duration']).duplicated()]

        self.search_extra = {'Files_Same_Folder': [False, '', False]}
        self.columns_mutuable = ['Actress', 'Ratings']

        self.changes = []        
        self.update_btn.clicked.connect(lambda : print('Done Created Yet'))
        self.save_btn.clicked.connect(self.save_table) 
        self.synced_table_gallery.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.synced_table_gallery.table.customContextMenuRequested.connect(self.show_context_menu) 
        self.search_bar.setText('**')
        self.apply_filter(refresh_view=False)
        self.synced_table_gallery.table_column_sort(0)
        self.btn_image_visable.click()
        self.synced_table_gallery.table.selectRow(1)
        self.showMaximized()

        self.synced_table_gallery.table.resizeColumnToContents(1)
        self.synced_table_gallery.table.resizeColumnToContents(2)
        self.synced_table_gallery.table.resizeColumnToContents(3)  
        

    def show_context_menu(self, position):
        selected_rows = set(index.row() for index in self.synced_table_gallery.table.selectedIndexes())
        if not selected_rows:
            return  
        menu = QMenu()
        
        rename_action = menu.addAction(f"Rename column 'Actress' ({len(selected_rows)} rows)")
        
        hide_duplicates_action = menu.addAction("Hide Duplicates")        
        hide_duplicates_action.setCheckable(True)
        
        hide_duplicates_action.setChecked(self.masks.duplicates[0])
        
        show_files_in_same_folder_action = menu.addAction("Show all files in same folder")          
        show_files_in_same_folder_action.setCheckable(True)
        show_files_in_same_folder_action.setChecked(self.search_extra['Files_Same_Folder'][0])  
        
        show_in_windows_explorer = menu.addAction("Show in Windows Explorer")    
        
        tag_action = menu.addAction("Add Tag")

        hide_driveexist_action = menu.addAction("Hide Files that are in a drive that cannot be accesed")        
        hide_driveexist_action.setCheckable(True)
        if self.masks.driveexist[0] is None:
            hide_driveexist_action.setEnabled(False)
        else:
            hide_driveexist_action.setChecked(self.masks.driveexist[0])
            
            
        always_on_top_action = menu.addAction("Always on Top") 
        always_on_top_action.setCheckable(True)  
          
            
        
        action = menu.exec_(self.synced_table_gallery.table.viewport().mapToGlobal(position))
        if action == rename_action:
            self.update_actress_names(selected_rows)
            
        if action == hide_duplicates_action:
            self.masks.duplicates[0] = not self.masks.duplicates[0]
            self.apply_filter()
            
        if action == show_files_in_same_folder_action: 
            self.search_extra['Files_Same_Folder'][0] = not self.search_extra['Files_Same_Folder'][0]
            self.click_same_folder(selected_rows)
            
        if action == tag_action: 
            self.update_tags(selected_rows)      
            
        if action == hide_driveexist_action:
            if self.masks.driveexist[0] is None:
                hide_driveexist_action.setEnabled(False)
            else:
                self.masks.driveexist[0] = not self.masks.driveexist[0]
                self.apply_filter()
                
        if action == show_in_windows_explorer:
            self.show_in_windows_explorer(selected_rows)
            
 
    def show_in_windows_explorer(self, selected_rows):
        for row in selected_rows:
            irow = self.index__sorting_mask[self.index__sorting_mask].index[row]
            filepath = self.df.loc[irow, 'File Path']
            UtilityFuntions.open_file_in_window_explorer(filepath)
            break

    def click_same_folder(self, selected_rows):
        for row in selected_rows:
            irow = self.index__sorting_mask[self.index__sorting_mask].index[row]
            filepath = self.df.loc[irow, 'File Path']
            hashdir = get_hashed_directory(filepath)
            self.search_extra['Files_Same_Folder'][1] = hashdir
            break
        self.apply_filter()

    def update_tags(self, selected_rows):
        tags_col_index = list(self.df.columns).index('Tags')
        for col in range(self.synced_table_gallery.table.columnCount()):
            if self.synced_table_gallery.table.horizontalHeaderItem(col).text() == 'Tags':
                tags_col_index = col
                break       
        
        # editable=True lets the user select from the list OR type a completely new name
        new_name, ok = QInputDialog.getItem(
            self, 
            "Add Tag", 
            "Select or enter new tag:", 
            self.tag_list()+['*Delete'], 
            current=0,       # Default selected index
            editable=True    # Allows typing custom input
        ) 
                
        if ok and new_name is not None:
            for row in selected_rows:
                irow = self.index__sorting_mask[self.index__sorting_mask].index[row]
                current_value = self.df.loc[irow, 'Tags']
                if new_name in current_value:
                    continue 
                if new_name == '*Delete':
                    new_name = ''
                else:
                    if current_value.strip(' ') != '-':
                        new_name = ','.join([current_value, new_name])
                filename = self.df.loc[irow, 'File Name']
                self.changes.append([row, tags_col_index, new_name, irow, filename])
                self.df.loc[irow, 'Tags'] = new_name        




    def check_drives_exist_of_files(self):
        vc = self.df['File Path'].apply(lambda x: os.path.splitdrive(x)[0]).value_counts().to_dict()
        vc = {k:int(v) for k,v in vc.items()}
        missing_drives_vc = {k:v for k,v in vc.items() if not os.path.exists(k)}
        missing_drives = tuple(missing_drives_vc.keys())

        mask = ~self.df['File Path'].str.upper().str.startswith(missing_drives)   
        
        if len(missing_drives)>0:
            self.extra_notes[1]=f',  Warning Following Drives are Missing:- {", ".join(missing_drives)}'
            self.masks.driveexist = [True, mask]            
        else:
            self.masks.driveexist = [None, mask]             
     

        




    def update_actress_names(self, selected_rows):
        actress_col_index = list(self.df.columns).index('Actress')
        for col in range(self.synced_table_gallery.table.columnCount()):
            if self.synced_table_gallery.table.horizontalHeaderItem(col).text() == "Actress":
                actress_col_index = col
                break

        for row in selected_rows:
            irow = self.index__sorting_mask[self.index__sorting_mask].index[row]
            filename = self.df.loc[irow, 'File Name']
            prefix = filename.split(' ')[0]
            if len(prefix)<4:
                prefix = prefix.replace('1','').replace('2','').replace('3','').replace('4','').replace('5','')
                
        actress_with_initials = []
        for actress in self.actress:
            initials = ''.join([(e+' ')[0] for e in actress.split(' ')]).replace(' ','')
            if initials==prefix:
                actress_with_initials.append(actress)

        if True:
            new_name, ok = QInputDialog.getItem(
                self, 
                "Rename Actress", 
                "Enter or select actress name:", 
                actress_with_initials, 
                0,      # Default selected index
                True    # Editable = True
            )
            if ok and new_name:
                print("User entered/selected:", new_name)
    
        else:
            new_name, ok = QInputDialog.getText( self,  "Rename Actress", "Enter new actress name:")

        if ok and new_name is not None:
            for row in selected_rows:
                #self.synced_table_gallery.table.setItem(row, actress_col_index, QTableWidgetItem(new_name))
                irow = self.index__sorting_mask[self.index__sorting_mask].index[row]
                filename = self.df.loc[irow, 'File Name']
                self.changes.append([row, actress_col_index, new_name, irow, filename])
                self.df.loc[irow, 'Actress'] = new_name
                
    def save_table(self):
        df_database =  update_database(VIDEOSHEET_DATABASE)
        changes = self.changes
        for change in changes:
            row, actress_col_index, new_name, irow, filename = change
            #print(change)
            col = df_database.columns[actress_col_index]
            df_database.loc[irow, col] = new_name
        for change in window.synced_table_gallery.star_changes:
            irow, col_name, new_rating = change
            df_database.loc[irow, col_name] = new_rating          

        self.no_changes_saved = len(changes)+len(window.synced_table_gallery.star_changes)
        print(f'Saving Changes: total changes = {self.no_changes_saved}')        
        df_database =  update_database(VIDEOSHEET_DATABASE, df_database, overwrite=True)
    
    
    def is_unsaved(self):
        no_changes = len(self.changes)+len(window.synced_table_gallery.star_changes)
        no_changes_saved = getattr(self,'no_changes_saved',0)
        unsaved = no_changes != no_changes_saved
        printd(f'self.is_unsaved():: {unsaved=}   #{no_changes=},{no_changes_saved=}')
        return unsaved
        
    def closeEvent(self, event):
            printd('closeEvent # which should check if unsaved')
            if not self.is_unsaved():
                event.accept()
                return
            reply = QMessageBox.question(self, "Unsaved Changes","You have unsaved changes.", QMessageBox.Discard | QMessageBox.Cancel, QMessageBox.Cancel) 
            if reply == QMessageBox.Discard:
                event.accept()    
            else:
                event.ignore()   
    
    
    
    
    
    


df_database =  update_database(VIDEOSHEET_DATABASE)















# This might be useful one say showing what folders are when and user can clickon them like windows explorer
if True:
    paths = df_database['File Path']
    parent_paths = paths.apply(lambda x:os.path.split(x)[0])
    parent_paths_vc = parent_paths.value_counts()
    
    
    df = pd.DataFrame(parent_paths_vc)
    df['File Path'] = df.index
    df['path'] =''    
    df['depth'] = df['File Path'].apply(lambda x:len(os.path.normpath(x).split(os.sep)))
    df = df.sort_values('depth',ascending=False)
    df['count1'] = 0
    df['count2'] = 0
    df['parent1'] = ''
    df['parent2'] = ''

    for ind,row in df.iterrows():
        if row['count']>11:
            df.loc[ind, 'path'] = ind
            continue
        
        parent1 = os.path.split(row['File Path'])[0]
        if parent1 in df['File Path']:
            df.loc[parent1, 'count1'] = df.loc[parent1, 'count1'] + row['count'] 
            df.loc[ind, 'parent1'] = parent1
            
    for ind,row in df.iterrows():
        if len(df.loc[ind, 'path'])>0:
            continue
        if row['count']+row['count1']>11:
            df.loc[ind, 'path'] = ind            
            continue
        
        parent1 = df.loc[ind, 'parent1']
        if len(parent1)>0:
            if len(df.loc[parent1, 'path'])>0:        
                df.loc[ind, 'path'] = parent1 
                continue
        
        parent1 = os.path.split(row['File Path'])[0]
        parent2 = os.path.split(parent1)[0]
        if parent2 in df['File Path']:
            df.loc[parent2, 'count2'] = df.loc[parent2, 'count2'] + row['count'] 
            df.loc[ind, 'parent2'] = parent2
    df = df.sort_index()    
        
#maybe use this for config
def get_first_file_that_exists(filepaths):
    for filepath in filepaths:
        if os.path.exists(filepath):
            return filepath





















if __name__ == "__main__":
    app = QApplication(sys.argv)
    df_database['Actress'] = df_database['Actress'] .fillna(' - ')
    df_database['Tags'] = df_database['Tags'] .fillna(' - ')   
    #df_database['File Path'] = df_database['File Path'].apply(lambda x:x.replace('D:','G:'))
    
    #df_database = df_database.loc[:80]
    window = VideoFileManager(df_database)
    #window.resize(2800,900)
    window.show()
    sys.exit(app.exec_())



dff = window.df






