# -*- coding: utf-8 -*-
"""Created on Tue Aug 11 02:26:33 2026@author: Alexm"""


import sys
from PyQt5.QtWidgets import QApplication
from SyncedTableGalleryWidget__VideoFileManager import SyncedTableGallery
from quick_example import fileinfo_df 
import pandas as pd


def create_dummy_table(nrows=1001):
    fileinfos = []
    for i in range(nrows):
        extra = ('Sarah','Bob','Kate','Tom','Brian')[i%5]
        file_name = f"Image_File_{i:04}_{extra}.jpg"
        size = 100 + ((123*(i%5)) +(5*(i%11)))
        day = 1+ (i%23)
        month =  4+ ((i//100)%5)
        row = [file_name, f"{day:02}/{month:02}/2026 02:44", "JPG File", f"{size} KB"]  
        fileinfos.append(row)
    return fileinfos
dummy_table = create_dummy_table()
dummy_df = pd.DataFrame(columns=["Name", "Date Modified", "Type", "Size"], data = dummy_table)
dummy_df['Ducks'] = 'Quack'

if False:
    dummy_df = fileinfo_df




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SyncedTableGallery(df=dummy_df)
    #window.resize(1150, 400)
    window.show()
    sys.exit(app.exec_())