# -*- coding: utf-8 -*-
"""Created on Tue Aug 11 21:40:07 2026 @author: Alexm

make sure video sheets doesnt override an existing one


"""
import pandas as pd
from quick_pandas import update_database

 
def custom_row_function(row):
    def duration_func(out):
        foo = out.split(':')
        foo2 = (int(foo[0])*60)+(int(foo[1]))
        return str(foo2-1)+'min '+str(foo2)+'min '+str(foo2+1)+'min'    
    part1 = ['|', row['File Name'].rsplit('.',1)[0]]
    part2 = row['File Size'].split('.')[0]
    part2 = ['|',part2+'MB', part2[:-1]+'0MB ', (part2[:-3]+'.'+ part2[-3].replace('.0','')+'GB' if len(part2)>3 else '' )]
    part3 = ['|', row['Tags'], row['Actress'] ]
    part3 = [ '' if pd.isna(e) else e.replace(',',' ') for e in part3 ]    
    part4 = ['|',duration_func(row['Duration']),  str(min([int(e) for e in row['Resolution'].split('x')]))]
    out = [e for ee in [part1, part2, part3, part4] for e in ee]
    out = ' '.join([e for e in out if e is not None])
    out = ''.join([e if e not in '.+-_' else ' ' for e in out ])    
    out = ' '.join([e for e in out.split(' ') if e!=''])
    out = out.lower().strip()
    return out





import sys
from PyQt5.QtWidgets import QApplication
from  SyncedTableGalleryWidget__VideoFileManager import VideoFileManager
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QMainWindow, QTableWidget, QTableWidgetItem, QMenu, QInputDialog)

VIDEOSHEET_DATABASE = r"C:\Users\Alexm\Desktop\__Videosheet_Databse__.csv"

def update_database_vidoesheets():
    pass




class VideoFileManager(VideoFileManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.df['Search'] = self.df.apply(custom_row_function, axis=1)
        self.columns_mutuable = ['Actress', 'Ratings']

        self.changes = []        
        self.update_btn.clicked.connect(update_database_vidoesheets)
        self.save_btn.clicked.connect(self.save_table) 
    
        self.synced_table_gallery.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.synced_table_gallery.table.customContextMenuRequested.connect(self.show_context_menu)

    def show_context_menu(self, position):
        selected_rows = set(index.row() for index in self.synced_table_gallery.table.selectedIndexes())
        if not selected_rows:
            return  
        menu = QMenu()
        rename_action = menu.addAction(f"Rename column 'Actress' ({len(selected_rows)} rows)")
        action = menu.exec_(self.synced_table_gallery.table.viewport().mapToGlobal(position))
        if action == rename_action:
            self.update_actress_names(selected_rows)

    def update_actress_names(self, selected_rows):
        actress_col_index = list(self.df.columns).index('Actress')
        for col in range(self.synced_table_gallery.table.columnCount()):
            if self.synced_table_gallery.table.horizontalHeaderItem(col).text() == "Actress":
                actress_col_index = col
                break

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
            print('Change this to allow ratings saveing')
            print(change)
            
        df_database =  update_database(VIDEOSHEET_DATABASE, df_database, overwrite=True)
        



df_database =  update_database(VIDEOSHEET_DATABASE)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    df_database['Actress'] = df_database['Actress'] .fillna(' - ')
    window = VideoFileManager(df_database)
    window.resize(1850, 1200)
    window.show()
    sys.exit(app.exec_())



dff =window.df

