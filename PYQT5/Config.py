# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 01:07:27 2026
@author: alexm

from Config import VIDEOSHEET_FOLDER, FOLDERS_TO_SEARCH, VIDEOSHEET_DATABASE 
"""

import os

if os.path.exists(r"C:\Users\Alexm\Desktop\TEMP_VIDEOSHEET"):
    VIDEOSHEET_FOLDER = r"C:\Users\Alexm\Desktop\TEMP_VIDEOSHEET"
    FOLDERS_TO_SEARCH = [r'C:\Users\Alexm\Desktop\AV\_Downloaded',
                         r"C:\Users\Alexm\Desktop\AV\_Streamed"]
    VIDEOSHEET_DATABASE = r"C:\Users\Alexm\Desktop\__Videosheet_Databse__.csv"
else:
    
    VIDEOSHEET_FOLDER = r"C:\Users\alexm\OneDrive\Desktop\VideosheetsAV"
    FOLDERS_TO_SEARCH = [r"C:\Users\alexm\OneDrive\Desktop\QuickDrop\Jessica Albanka (Alisa, Alisa I)",
                         r"C:\Users\alexm\OneDrive\Desktop\QuickDrop\AV\KatanaKombat"]
    VIDEOSHEET_DATABASE = r"C:\Users\alexm\OneDrive\Desktop\VideosheetsAV.csv"
    
    
        
    FOLDERS_TO_SEARCH = r'''
    C:\Users\alexm\OneDrive\Desktop\MoveFiles\Po\Alissa
    C:\Users\alexm\OneDrive\Desktop\MoveFiles\Po\DF+Po Best Shortcuts
    C:\Users\alexm\OneDrive\Desktop\MoveFiles\Po\DF-Planetsuzy
    C:\Users\alexm\OneDrive\Desktop\MoveFiles\Po\DF-ReelDeepfakes
    C:\Users\alexm\OneDrive\Desktop\MoveFiles\Po\JezabelVessir
    C:\Users\alexm\OneDrive\Desktop\MoveFiles\Po\KatiadeLys(Ass)
    C:\Users\alexm\OneDrive\Desktop\MoveFiles\Po\LittleCaprice
    
    C:\Users\alexm\OneDrive\Desktop\MoveFiles\Po\Po_Dump
    C:\Users\alexm\OneDrive\Desktop\MoveFiles\Po\Streamed
    
    C:\Users\alexm\OneDrive\Desktop\QuickDrop\AV\AndreinaDeLux
    C:\Users\alexm\OneDrive\Desktop\QuickDrop\AV\GloriaGucci
    C:\Users\alexm\OneDrive\Desktop\QuickDrop\AV\KatanaKombat
    C:\Users\alexm\OneDrive\Desktop\QuickDrop\FelicityFey
    C:\Users\alexm\OneDrive\Desktop\QuickDrop\Jessica Albanka (Alisa, Alisa I)
    
    C:\Users\alexm\OneDrive\Desktop\QuickDrop\DeepFakes_ForumsDownload\Copied_to_NAS_DF
    
    C:\Users\alexm\OneDrive\Desktop\MoveFiles\Po\ZC
    
    C:\Users\alexm\OneDrive\Desktop\MoveFiles\DF-MrDeepfakes(Abroad)
    
    C:\Users\alexm\Downloads\NataliaAndreeva
    C:\Users\alexm\Downloads\- Karen Ishida - Reona Kirishima
    C:\Users\alexm\Downloads\女優合集394葵司作品4高清無水印33集\SSIS-434
    C:\Users\alexm\Downloads\葵つかさ,Tsukasa Aoi\videos\036 DV-1541
    C:\Users\alexm\Downloads\葵つかさ,Tsukasa Aoi\videos\055 DVAJ-033
    C:\Users\alexm\Downloads\葵つかさ,Tsukasa Aoi\videos\058 SNIS-449
    C:\Users\alexm\Downloads\葵つかさ,Tsukasa Aoi\videos\097 SSNI-303
    
    C:\Users\alexm\OneDrive\Desktop\MoveFiles\Po
    
    C:\Users\alexm\OneDrive\Desktop\QuickDrop
    C:\Users\alexm\OneDrive\Desktop\QuickDrop\AV
    
    C:\Users\alexm\OneDrive\Desktop\QuickDrop\_AV_NAS__Best_Copies
    
    
    Z:\
        
    D:\Streamed
    D:\TiffanyDiamond
    D:\GDP
    D:\AlinaB
    D:\LiyaSilver
    D:\NataliaAndreeva
    D:\DeepFakes
    D:\AV
    D:\LeonaKirishima
            
    '''.splitlines()
    
    
    
    
    
    
    FOLDERS_TO_SEARCH = [e.strip() for e in FOLDERS_TO_SEARCH if len(e.replace(' ',''))>0]









