# -*- coding: utf-8 -*-
"""Created on Wed Aug  5 03:30:01 2026@author: Alexm"""


from SyncedTableGalleryWidget2 import SyncedTableGallery
from QPushCycleButton import QPushCycleButton
from ImageWidget_v0 import ImageWidget

from PyQt5.QtWidgets import QMainWindow, QPushButton
from PyQt5.QtWidgets import QLineEdit, QVBoxLayout, QWidget, QHBoxLayout, QComboBox, QCompleter

from PyQt5.QtGui import QIcon, QFont, QPixmap, QColor, QPalette
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication


from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QMessageBox

import os
from types import SimpleNamespace
import pandas as pd


import time
from contextlib import contextmanager

from PrintAverageTimes import PrintAverageTimes

USER_ROLE = Qt.UserRole



@contextmanager
def timer(name):
    start = time.perf_counter()
    yield
    elapsed = time.perf_counter() - start
    print(f'[{name}] completed in {elapsed:.2f}s')






def find_small_filepath(filepath1, folder_small='small_90x90'):
    import os
    folder_1, filename1 = os.path.split(filepath1)    
    folder_2 = os.path.join(folder_1, folder_small)
    filename2 = filename1.replace('.vs.jpg','.vs_small.jpg')
    filepath2 = os.path.join(folder_2, filename2)
    return filepath2

def find_small_filepath2(filepath1, folder_small='small2_90x90'):
    import os
    folder_1, filename1 = os.path.split(filepath1)    
    folder_2 = os.path.join(folder_1, folder_small)
    filename2 = filename1.replace('.vs.jpg','.mid_small.jpg')
    filepath2 = os.path.join(folder_2, filename2)
    return filepath2

        
def color_textbox(self, text_box, color='red'):
    color_dict = {'green':"#d1e7dd", 'orange':"#fee9cc",
                  'red':"#ffe5d9",   'grey':"#f6f8f9",
                  'white':"#ffffff"}            
    
    palette = text_box.palette()  

    color = color_dict.get(color, "#ffffff")
    palette.setColor(QPalette.Base, QColor(color)) 
    text_box.setPalette(palette)            
        


class SearchableComboBoxApp(QComboBox):
    def __init__(self, items=[], placeholder="Actress..."):
        super().__init__()
        self.setEditable(True)
        self.addItems(items)
        self.lineEdit().setPlaceholderText("Type to search...")
        self.lineEdit().setPlaceholderText(placeholder)        
        self.setCurrentIndex(-1)       
        completer = self.completer()
        completer.setFilterMode(Qt.MatchContains)
        completer.setCompletionMode(QCompleter.PopupCompletion)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)








class InfoButton(QPushButton):
    def __init__(self, info='', button_text='', icon_size=None):
        super().__init__(button_text)
        self.info = info
        self.button_text = button_text
        
        style = self.style()
        self.icon = style.standardIcon(style.SP_MessageBoxInformation)
        self.setIcon(self.icon)

        if icon_size is not None:
            self.setIconSize(icon_size)
        else:
            self.setIconSize(QSize(20, 20))
            
        #self.setStyleSheet("QPushButton { padding: 8px; font-size: 14px; }")
        self.clicked.connect(self.show_info)
        
    def show_info(self):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Information")
        
        info = self.info
        if callable(info):
            info = info()
        if isinstance(info, (list, tuple)):
            info = "\n".join(str(item) for item in info)            
            
        msg_box.setText(info)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setTextInteractionFlags( Qt.TextSelectableByMouse | Qt.TextSelectableByKeyboard  )
        pixmap = self.icon.pixmap(32, 32)
        msg_box.setIconPixmap(pixmap)
        msg_box.exec_()

if False:
    class InfoButtonDemo(QWidget):
        def __init__(self):
            super().__init__()
            self.initUI()
    
        def initUI(self):
            self.setWindowTitle("PyQt5 Info Button Example")
            self.resize(300, 200)
            layout = QVBoxLayout()
            
            self.info_button = InfoButton( info="Here is the detailed information you requested!\n\nThis box is now\n completely silent, and you can select/copy this text."  )
            layout.addWidget(self.info_button)
            self.setLayout(layout)
    
    
    if __name__ == "__main__":
        app = QApplication(sys.argv)
        demo = InfoButtonDemo()
        demo.show()
        sys.exit(app.exec_())
    















class VideoSyncedTableGallery(SyncedTableGallery):
    def __init__(self,*args,image_thumbnail_version,**kwargs):
        self.image_thumbnail_version = image_thumbnail_version        
        super().__init__(*args,**kwargs)
        self.gridlist.itemDoubleClicked.connect(self.on_item_double_clicked)


    def get_image_from_row(self, row_data):
        item = self.default_icon
        for val in row_data:
            if 'vs.jpg' in str(val):
                image_fp = str(val)
                if self.image_thumbnail_version() ==0:
                    image_fp_small = find_small_filepath(image_fp)
                if self.image_thumbnail_version() ==1:                    
                    image_fp_small = find_small_filepath2(image_fp)
                    
                if os.path.exists(image_fp_small):
                    image_fp = image_fp_small

                pixmap = QPixmap(image_fp)
                item = QIcon(pixmap)
                #item = QIcon(image_fp)
        return item
    
    def find_video_filepath_given_series(self, row_data):
        video_extensions = ['.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.m4v']           
        for val in row_data:          
            if any(str(val).lower().endswith(ext) for ext in video_extensions):
                if ':' in val:
                    return val
                
    def modify_grid_item0(self, item):
        data_dic = item.data(USER_ROLE)
        if data_dic is not None:
            value = data_dic['id']
            row = self.df_view.iloc[value]
            video_filepath = self.find_video_filepath_given_series(row)
            data_dic['video_filepath'] = video_filepath
            item.setData(Qt.UserRole, data_dic)
            for val in row:
                if 'vs.jpg' in str(val):
                    image_fp = str(val)
                    tooltip_html = f'<img src="{image_fp}" style="max-width: 400px; max-height: 400px;">'
                    break
            
            item.setToolTip(tooltip_html)
            
        return item
        
    def modify_grid_item(self, item, row=None):
      if not hasattr(self, 'pat'):
         self.pat = PrintAverageTimes(snooze=True)
      user_data = item.data(USER_ROLE)
      if user_data is None:
        return item
      self.pat(1,'Start above slow 11 total')    
      # 1. Handle both integer counter and dict seamlessly
      if isinstance(user_data, dict):
        value = user_data.get('id')
        data_dic = user_data
      else:
        value = user_data
        data_dic = {'id': value}
      self.pat(2,'Middle1')        
      # 2. Extract row data and resolve video filepath
      if value is not None and value < self.length_df_view:
        self.pat(3,'Middle1 start of loop pretty slow 8s')            
        if row is None: 
           row = self.df_view.iloc[value] 
        video_filepath = self.find_video_filepath_given_series(row)
    
        # Store updated dictionary back into item data
        data_dic['video_filepath'] = video_filepath
        item.setData(Qt.UserRole, data_dic)
        self.pat(4,'Middle3')  
        # 3. Find image for tooltip
        tooltip_html = None
        for val in row:
          val_str = str(val)
          if 'vs.jpg' in val_str:
            tooltip_html = (
                f'<img src="{val_str}" style="max-width: 400px; max-height:'
                ' 400px;">'
            )
            break
        if tooltip_html:
          item.setToolTip(tooltip_html)

        self.pat(6,'end')
        self.pat(7,'Tidy')
        if self.pat.count%200==199:
            self.pat.print_summary()

    
      return item
        
    
    
    
    def on_item_double_clicked(self, item):
        data_dic = item.data(Qt.UserRole)
        video_filepath = data_dic['video_filepath'] 
        os.startfile(video_filepath)


    def changed_item(self, row_idx):
        if row_idx is False:
            print('Unselected')
            return
            
        if len(self.df_view)>row_idx:
            info = self.df_view.iloc[row_idx]
            vs_fp = info['Videosheet_fp']
            print('changed_item',vs_fp, row_idx)
            self.img_widget.set_image(vs_fp)


    def refresh_view(self):
        super().refresh_view()
        print(len(self.df_view))
        n_videos = len(self.df_view)

        total_seconds = int(sum(self.df_view['Duration'].apply(lambda x: sum([int(e)*v for e,v in zip(x.split(':'),[3600,60,1])]))))
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        timecode = f'{hours}:{minutes:02d}:{seconds:02d}'
        bytes_size = int(self.df_view['File Size Raw'].sum())

        #bytes_size = total_bits / 8
        gb = bytes_size / (1024 ** 3)  # Gigabytes (GiB)
        gb_code = f"{gb:.2f} GB"
        
        table_info_label = f'       {n_videos} Videos Found Matching Search;  TotalTime: {timecode},  TotalSize: {gb_code}'
        table_info_label = table_info_label + ''.join(self.extra_notes)

        if hasattr(self, 'table_info_label'):
            self.table_info_label.setText(table_info_label)
        
                



    
class VideoFileManager(QMainWindow):
    def __init__(self, df, *args,**kwargs):
        super().__init__(*args,**kwargs)
        
        screen_size_obj = self.screen().size()
        self.screen_size = (screen_size_obj.width(), screen_size_obj.height())
        self.screen_mode = {(3440, 1440):'UltraWide'}.get(self.screen_size, 'Unknown')
                
        
        
        self.masks = SimpleNamespace()
        self.setWindowTitle("VideoFileManager")
        self.__init_ui__(df)
        self.synced_table_gallery.sort_func_dict = {'File Size':lambda x: float(x.strip().split(' ')[0])}   
        self.search_extra = {}
    
 
    @property
    def df(self):
        return self.synced_table_gallery.df
    @df.setter
    def df(self, value):
        self.synced_table_gallery.df = value 
    @property
    def index__sorting_mask(self):
        return self.synced_table_gallery.index__sorting_mask
    @index__sorting_mask.setter
    def index__sorting_mask(self, value):
        self.synced_table_gallery.index__sorting_mask = value         
    @property
    def df_view(self):
        return self.synced_table_gallery.df_view    
    
    @property
    def extra_notes(self):
        return self.synced_table_gallery.extra_notes
    @extra_notes.setter
    def extra_notes(self, value):
        self.synced_table_gallery.extra_notes = value
        
    def get_column_index_by_name(self, col_name):
        pass
        
        
    
    
    
    
    def __init_ui__(self, df):
        print('z')        
        
        self.image_thumbnail_version = 0        
        self.synced_table_gallery = VideoSyncedTableGallery(df=df, image_thumbnail_version=lambda : self.image_thumbnail_version)
        
        print('y')  
        
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search by name...")
        self.search_bar.returnPressed.connect(self.apply_filter)
        self.search_btn = QPushButton('Search')     
        self.search_btn.clicked.connect(self.apply_filter)
        
        self.actress = ['Natalie Portman']+sorted([ str(e) for e in self.df['Actress'].unique()])
        self.search_actress = SearchableComboBoxApp(self.actress)  
        self.search_actress.currentTextChanged.connect(self.actress_selected)    
        
        self.search_tags = SearchableComboBoxApp(self.tag_list(short=False), placeholder='Tags...')  
        self.search_tags.currentTextChanged.connect(self.actress_selected)           
        
        
        app_font = QFont("Arial", 12)        
        self.search_bar.setFont(app_font)
        self.search_btn.setFont(app_font)
        self.search_actress.setFont(app_font)        
        self.search_tags.setFont(app_font)           
        
        search_widgets_layout = QHBoxLayout()       
        search_widgets_layout.addWidget(self.search_bar)
        search_widgets_layout.addWidget(self.search_btn)
        search_widgets_layout.addWidget( self.search_actress) 
        search_widgets_layout.addWidget( self.search_tags)              
        
        self.switch_images_btn = QPushButton('Switch Image')   
        self.switch_images_btn.clicked.connect(self.change_image_thumbnail)
        self.switch_images_btn.setFont(app_font)     
        search_widgets_layout.addWidget(self.switch_images_btn)
        
          
        
        self.pin_button = QPushButton("Pin Window")
        self.pin_button.setCheckable(True)
        is_on_top = bool(self.windowFlags() & Qt.WindowStaysOnTopHint)
        self.pin_button.setChecked(is_on_top)
        self.pin_button.toggled.connect(self.toggle_always_on_top)
        self.pin_button.setFont(app_font) 
        
        info = 'Some Info'
        if hasattr(self, 'info'):
            info = self.info
        self.info_button = InfoButton(info)
        
        
        self.upload_btn = QPushButton('Upload New Vids')     
        self.upload_btn.clicked.connect(self.upload_new_vids)
        self.upload_btn.setFont(app_font)            
 
        debug_future = lambda x: print('Feature does not work yet')
        self.update_btn = QPushButton('Update')     
        self.update_btn.clicked.connect(debug_future)
        self.update_btn.setFont(app_font)        
        self.save_btn = QPushButton('Save')
        self.save_btn.clicked.connect(debug_future) 
        self.save_btn.setFont(app_font) 
        
        self.btn_image_visable = QPushCycleButton([("Show Image", False),("Hide Image", True)])
        self.btn_image_visable.setFont(app_font)
        self.btn_image_visable.valueChanged.connect(lambda state: self.img_widget.setVisible(state))
        search_widgets_layout.addWidget(self.btn_image_visable)        
        
        
        search_widgets_layout.addWidget(self.pin_button)
        search_widgets_layout.addWidget(self.info_button)       
        search_widgets_layout.addWidget(self.upload_btn)
        search_widgets_layout.addWidget(self.update_btn)
        search_widgets_layout.addWidget(self.save_btn)   
        
        search_widgets = QWidget()
        search_widgets.setLayout(search_widgets_layout)   

        main_layout = QVBoxLayout()
        main_layout.addWidget(search_widgets, stretch=0)
        
        
        table_and_image = QHBoxLayout()        
        self.img_widget = ImageWidget()
        table_and_image.addWidget(self.synced_table_gallery)
        table_and_image.addWidget(self.img_widget)
        self.synced_table_gallery.img_widget = self.img_widget
        
        main_layout.addLayout(table_and_image, stretch=1)
        
        #main_layout.addWidget(self.synced_table_gallery, stretch=1)        
 
        
 
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        self.btn_image_visable.refresh()  

  
    def upload_new_vids(self):
        import sys, subprocess
        print(' Add files to video manager')
        script_path = r"detect_and_upload_new_videos\MultiStageTaskRunner__VideoFileMager.py"
        subprocess.Popen([sys.executable, script_path])
        #important conflict with dtabase
        # have to save before open
        # and then reload
    



    def toggle_always_on_top(self, checked):
        flags = self.windowFlags()
        if checked:
            flags |= Qt.WindowStaysOnTopHint
        else:
            flags &= ~Qt.WindowStaysOnTopHint
        self.setWindowFlags(flags)
        self.show()  # Re-render window to apply flag changes immediately


    def tag_list(self, short=True, extra=['Orgy','Black','Sexy Voice', 'Hypno+','FewVideos',"Butt", "Tits", "Body",'Sexy Clothing','Incest','Compliation','MultipleActress','preCompliation'] ):
        values = list(self.df['Tags'].unique())+extra
        values = sorted(list(set(','.join(values).split(','))))
        values0 = [e for e in values if e !=' - ']
        values = ['Body/Butt/Tits', 'AnyTag']+ values
        if short:        
            return values0
        return values

      
    
    def change_image_thumbnail(self):
        self.image_thumbnail_version = {0:1,1:0}[self.image_thumbnail_version]
        
        
    def actress_selected(self, text):
        self.apply_filter()

 
    def apply_filter(self, refresh_view=True):
        """Bespoke function to filter the dataset."""
        print('Search *Start ','self.apply_filter',f'{refresh_view=}')
        color_textbox(self, self.search_bar, color='red')
        self.search_btn.setDisabled(True)
        if refresh_view:
            QApplication.processEvents()  
      
        self.apply_filter__collect_search_data_modify_indes__sorting_mask()
      
        if refresh_view:
            self.refresh_ui()
            
        color_textbox(self, self.search_bar, color='white')        
        self.search_btn.setDisabled(False)
        print('   Search *Finished ')

    
    def apply_filter__collect_search_data_modify_indes__sorting_mask(self):
        text1 = self.search_bar.text().lower()
        text2 = self.search_actress.currentText().lower()
        text2 = text2.replace('-','')
        text3 = ''
        text4 = self.search_tags.currentText().lower()
        text4 = text4.replace('-','').strip(' ')
        if len(text4)>3:
            text4 = ('<'+text4+'>'+' anytag ')#.replace('+','')
        
        search_extra = getattr(self, 'search_extra', {})
        for k,(flag,search_string, refresh) in search_extra.items():
            if flag:
                text3 = search_string
                if refresh:
                    search_extra[k][0] = False
        search_text = ' '.join([text1, text2, text3, text4])
        if not search_text:
            self.filtered_df = self.df.copy()
        else:    
            search_text = search_text.split(' ')
            search_text = [e for e in search_text if e!='' ]
            
            with timer(f'Searching... ({search_text=})'):            
                mask_search = self.df['Search'].apply(lambda x: all([text in x for text in search_text]))
            
            #Use the masks from duplicates and drives that are not accesiable to hide other files
            mask = pd.Series(True, index=mask_search.index)
            for attr, value in vars(self.masks).items():
                state, optional_mask = value
                if state:
                    mask = mask & optional_mask
            files_skipped_search = int(sum(~mask))
            self.extra_notes[0] = f'           {files_skipped_search} Files that skipped search'            
            
            mask = mask & mask_search
            self.index__sorting_mask = mask[self.index__sorting_mask.index]        




    def refresh_ui(self):
        scrollbar1 = self.synced_table_gallery.gridlist.verticalScrollBar()
        scrollbar2 = self.synced_table_gallery.table.verticalScrollBar()    
        scrollbar1.blockSignals(True)
        scrollbar2.blockSignals(True)
        self.synced_table_gallery.refresh_view()
        scrollbar1.blockSignals(False)
        scrollbar2.blockSignals(False)


    
    
