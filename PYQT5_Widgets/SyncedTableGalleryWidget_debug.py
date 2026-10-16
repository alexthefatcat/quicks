# -*- coding: utf-8 -*-
"""Created on Wed Sep  9 22:32:49 2026@author: alexm

This program should use all of the PYQT5_widgets Ive created

"""


from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QIcon

import pandas as pd
import sys, os


from QPushCycleButton import QPushCycleButton
from SyncedTableGalleryWidget2 import SyncedTableGallery
from ImageWidget_v0 import ImageWidget



fp_csv =r"C:\Users\alexm\OneDrive\Desktop\VideosheetsAV.csv"
df = pd.read_csv(fp_csv)
df = df.iloc[:300]

mask = pd.Series(False, index = list(df.index))

df1, df2, df3, df4 = df.iloc[:8],  df.iloc[10:28], df.iloc[40:281], df.iloc[200:201]


class SyncedTableGallery2(SyncedTableGallery):
    def __init__(self,*args, **kwargs):
        super().__init__(*args,**kwargs)
        
    def get_image_from_row(self, row_data):
        thumbnail = self.default_icon
        for val in row_data:
            str_val = str(val)
            if 'vs.jpg' in str_val:
                image_fp_small = self.find_small_filepath(str_val)
                if os.path.exists(image_fp_small):
                    thumbnail = image_fp_small
                    break
        item = QIcon(thumbnail)
        return item

    def find_small_filepath(self, filepath1, folder_small='small_90x90'):
        folder_1, filename1 = os.path.split(filepath1) 
        filename2 = filename1.replace('.vs.jpg','.vs_small.jpg')
        folder_2 = os.path.join(folder_1, folder_small)
        return os.path.join(folder_2, filename2)
    
    def changed_item(self, row_idx):
        if row_idx is None or row_idx is False:
            print('Unseletected')
            return
        info = self.df_view.iloc[row_idx]
        vs_fp = info['Videosheet_fp']
        #print('changed_item',vs_fp, row_idx)
        self.img_widget.set_image(vs_fp)
 
    

class MainWindow(QMainWindow):
    def __init__(self, df, *args,**kwargs):
        self.df = df
        super().__init__(*args,**kwargs)
        self.resize(2800,900)
        self.setWindowTitle("SyncedTableGallery_Debug")
        self.__init_ui__(df)
        
    def __init_ui__(self,df):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        button_layout = QHBoxLayout()
        
        self.btn_info = {"df1(8)":(0,8), "df2(18)":(10,28), "df3(241)":(40,281), "df4(1)":(200,202), "df5(100)":(5,105)}
        for btn_name_k in self.btn_info.keys():
            btn = QPushButton(btn_name_k)
            btn.clicked.connect(lambda checked=False, n=btn_name_k: self.btn_clicked(n))         
            button_layout.addWidget(btn)
            
        self.btn_image_visable = QPushCycleButton([("Show Image", False),("Hide Image", True)])
        self.btn_image_visable.valueChanged.connect(lambda state: self.img_widget.setVisible(state))        
        button_layout.addWidget(self.btn_image_visable) 

        btn = QPushButton('print("----------------------")')
        btn.clicked.connect(lambda : print('----------------------'))  
        button_layout.addWidget(btn)         

        main_layout.addLayout(button_layout)
        
        table_and_image = QHBoxLayout()
        #synced_table_gallery created and used here
        self.synced_table_gallery = SyncedTableGallery2(df=df)
        self.img_widget = ImageWidget()
        table_and_image.addWidget(self.synced_table_gallery)
        table_and_image.addWidget(self.img_widget)
        self.synced_table_gallery.img_widget = self.img_widget
        
        main_layout.addLayout(table_and_image)
        self.btn_image_visable.refresh()
        print('Button Pressed Before')
        if False:
            self.btn_clicked("df2(18)", refresh_view=False)
            print('Button Pressed After')        

    
    def btn_clicked(self, btn_name_k, refresh_view=True):
        ind_start, ind_end = self.btn_info[btn_name_k]
        mask2 = mask.copy()
        mask2[ind_start:ind_end] = True
        self.synced_table_gallery.index__sorting_mask = mask2[self.synced_table_gallery.index__sorting_mask.index]
        if refresh_view:
            self.synced_table_gallery.refresh_view()#
            self.btn_image_visable.index = 0
        
    def resizeEvent(self, event):
            new_size = event.size()
            print( f"Window Size -> Width: {new_size.width()}px, Height: {new_size.height()}px")
            super().resizeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow(df)
    window.show()
    sys.exit(app.exec_())




            
      
     
            
            
            
            
            
            
            
            
            
        
            
            
            
            
    
    