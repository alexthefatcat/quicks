# -*- coding: utf-8 -*-
"""Created on Wed Aug  5 03:30:01 2026@author: Alexm"""


from SyncedTableGalleryWidget import SyncedTableGallery
from PyQt5.QtWidgets import QMainWindow, QPushButton
from PyQt5.QtWidgets import QLineEdit, QVBoxLayout, QWidget, QHBoxLayout, QComboBox, QCompleter
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
import os




class SearchableComboBoxApp(QComboBox):
    def __init__(self, items=[]):
        super().__init__()
        self.setEditable(True)
        self.addItems(items)
        self.lineEdit().setPlaceholderText("Type to search...")
        self.lineEdit().setPlaceholderText("Actress...")        
        self.setCurrentIndex(-1)       
        completer = self.completer()
        completer.setFilterMode(Qt.MatchContains)
        completer.setCompletionMode(QCompleter.PopupCompletion)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)



class VideoSyncedTableGallery(SyncedTableGallery):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.gridlist.itemDoubleClicked.connect(self.on_item_double_clicked)

    def get_image_from_row(self, row_data):
        item = self.default_icon
        for val in row_data:
            if 'vs.jpg' in str(val):
                image_fp = str(val)
                item = QIcon(image_fp)
        return item
    
    def find_video_filepath_given_series(self, row_data):
        video_extensions = ['.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.m4v']           
        for val in row_data:          
            if any(str(val).lower().endswith(ext) for ext in video_extensions):
                if ':' in val:
                    return val
                
    def modify_grid_item(self, item):
        data_dic = item.data(Qt.UserRole)
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
    
    def on_item_double_clicked(self, item):
        data_dic = item.data(Qt.UserRole)
        video_filepath = data_dic['video_filepath'] 
        os.startfile(video_filepath)






    
class VideoFileManager(QMainWindow):
    def __init__(self, df, *args,**kwargs):
        super().__init__(*args,**kwargs)
        self.setWindowTitle("VideoFileManager")
        self.__init_ui__(df)
        self.synced_table_gallery.sort_func_dict = {'File Size':lambda x: float(x.strip().split(' ')[0])}   
 
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
    
    
    
    
    
    
    
    
    
    
    def __init_ui__(self, df):
        self.synced_table_gallery = VideoSyncedTableGallery(df=df)
        
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search by name...")
        #self.search_bar.textChanged.connect(self.apply_filter)
        self.search_bar.returnPressed.connect(self.apply_filter)
        self.search_btn = QPushButton('Search')     
        self.search_btn.clicked.connect(self.apply_filter)
        
        self.actress = ['Natalie Portman']+sorted([ str(e) for e in self.df['Actress'].unique()])
        self.search_actress = SearchableComboBoxApp(self.actress)  
        self.search_actress.currentTextChanged.connect(self.actress_selected)        

        app_font = QFont("Arial", 12)        
        self.search_bar.setFont(app_font)
        self.search_btn.setFont(app_font)
        self.search_actress.setFont(app_font)        
        
        search_widgets_layout = QHBoxLayout()       
        search_widgets_layout.addWidget(self.search_bar)
        search_widgets_layout.addWidget(self.search_btn)
        search_widgets_layout.addWidget( self.search_actress)       
        
        debug_future = lambda x: print('Feature does not work yet')
        self.update_btn = QPushButton('Update')     
        self.update_btn.clicked.connect(debug_future)
        self.update_btn.setFont(app_font)        
        self.save_btn = QPushButton('Save')
        self.save_btn.clicked.connect(debug_future) 
        self.save_btn.setFont(app_font) 
        search_widgets_layout.addWidget(self.update_btn)
        search_widgets_layout.addWidget(self.save_btn)         
        
        search_widgets = QWidget()
        search_widgets.setLayout(search_widgets_layout)   

        main_layout = QVBoxLayout()
        main_layout.addWidget(search_widgets, stretch=0)
        main_layout.addWidget(self.synced_table_gallery, stretch=1)        
 
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
        
    def actress_selected(self, text):
        self.apply_filter()

 
    def apply_filter(self):
        """Bespoke function to filter the dataset."""
        text1 = self.search_bar.text().lower()
        text2 = self.search_actress.currentText().lower()
        search_text = ' '.join([text1, text2])
        
        if not search_text:
            self.filtered_df = self.df.copy()
        else:    
            search_text = search_text.split(' ')
            search_text = [e for e in search_text if e!='' ]

            mask = self.df['Search'].apply(lambda x: all([text in x for text in search_text]))
            self.index__sorting_mask = mask[self.index__sorting_mask.index]
            print('Searching ')






        #self.apply_sort()
        self.refresh_ui()


    def refresh_ui(self):
        scrollbar1 = self.synced_table_gallery.gridlist.verticalScrollBar()
        scrollbar2 = self.synced_table_gallery.table.verticalScrollBar()    
        scrollbar1.blockSignals(True)
        scrollbar2.blockSignals(True)
        self.synced_table_gallery.refresh_view()
        scrollbar1.blockSignals(False)
        scrollbar2.blockSignals(False)







