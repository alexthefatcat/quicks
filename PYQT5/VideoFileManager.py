# -*- coding: utf-8 -*-
"""Created on Tue Aug 11 02:21:16 @author: Alexm
    

and in theory there could be duplicated for videoshetfiles if two viode have the same filename




TasksToDo:-

    1) Find code to make the csv ; so search all python files for this
    2) Create Code to get videosheet data and save it into a csv
    3) Videosheets why didnt it work on all files on this machine fix so works on all videos
    4) run on travel labptop ange get videosheets working debug and gui problems as well
    5) Git 

    7) build on database
    9) create databsae so it can work


    Finish
        Save Ratings
        Upload and Save Buttons do something
        Tidy Widget Code
        Editable Actress and Save them
        when you search for something and then un search, rows in that chunk have all the rows filled up
        after you search and the fitlered result should be sorted accrodingly
    
    

    Extras:-
        09) Speed up a bit slow at the momoent
        10) Future properly sought out all debug proglems
        11) adjustable so when size changes number of images shown changes so when right widget expanded 8 images are shown
        12) can have gaps with titles and click and hide expand on groupings[but gaps anyway]
        15) Playlists
        16) make ratings column wider
        17) after you have just searched/filtered keep sorting



Added index__sorting_mask which dymically creates the df_view from df - so sorting and masking easier
Added modifing actress and saving to database











"""
import pandas as pd
from quick_pandas import update_database


def create_search_column__function(row):
    def duration_func(out):
        foo = out.split(':')
        foo2 = (int(foo[0])*60)+(int(foo[1]))
        return str(foo2-1)+'min '+str(foo2)+'min '+str(foo2+1)+'min'    
    part1 = ['|', row['File Name'].rsplit('.',1)[0]]
    part2 = row['File Size'].split('.')[0]
    part2 = ['|',part2+'MB', part2[:-1]+'0MB ', (part2[:-3]+'.'+ part2[-3].replace('.0','')+'GB' if len(row)>3 else '' )]
    part3 = ['|', row['Tags'], row['Actress'] ]
    part3 = [ '' if pd.isna(e) else e.replace(',',' ') for e in part3 ]    
    part4 = ['|',duration_func(row['Duration']),  str(min([int(e) for e in row['Resolution'].split('x')]))]
    out = [e for ee in [part1, part2, part3, part4] for e in ee]
    out = ' '.join([e for e in out if e is not None])
    out = ''.join([e if e not in '.+-_' else ' ' for e in out ])    
    out = ' '.join([e for e in out.split(' ') if e!=''])
    out = out.lower().strip()
    return out
    
def order_columns(df, first_columns):
    org_columns = list(df.columns)
    last_columns = [col for col in org_columns if col not in first_columns]
    new_columns = first_columns+last_columns
    return df[new_columns]




df_database =  update_database('pyvideo_film_info.csv')

actress = ['Roxy Bell', 'Reona Kirishamia','Nina James',None,'Mini Diva', 'Little Caprice', 'Bella Brookz', 'Bella Brookz','Roxy Bell','Roxy Bell','Roxy Bell','Alice','Alice','Alice','Alice','Alice',]
df_database['Actress'] = actress
del actress
df_database['Search'] = df_database.apply(create_search_column__function, axis=1)




if False:
    df_database = pd.concat({'A':df_database, 'B':df_database,'C':df_database,'D':df_database,'E':df_database})
    df_database = df_database.reset_index()
    for n in range(0,len(df_database),6):
        df_database.loc[ n,'File Name'] = str(n)+ df_database['File Name'][n]
    del n



df_database = order_columns(df_database, ['File Name', 'File Size', 'Resolution','Duration','Ratings', 'Actress'])
df = df_database


import sys
from PyQt5.QtWidgets import QApplication
from  SyncedTableGalleryWidget__VideoFileManager import VideoFileManager

if True:
    if __name__ == "__main__":
        app = QApplication(sys.argv)
        window = VideoFileManager(df)
        window.resize(1450, 1000)
        window.show()
        sys.exit(app.exec_())
    
    




