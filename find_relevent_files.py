# -*- coding: utf-8 -*-
"""Created on Thu Jul 17 01:38:53 2025 @author: Alexm



So link to config file


it has folders to search:-
and previously found files
and you can click search certain files again as well as search everything


useful with uis

saved_relevent_filepaths
   #config = create_config()
   config = read_config(config_fp)
   config = check_files_exist(config) # quick
   config = scan(config, long_scan = False)
   save_config(config)

"""


from quick_find_filepaths import find_filepaths
import os

def get_filepaths(verbose=True):
    file_paths = find_filepaths(r"C:\Users\Alexm",  subfolders=True, extension='.jsonlz4')
    fps = {}
    for file_path in file_paths:
        folder = os.path.split(file_path)[0]
        fps[folder] = fps.get(folder, []) +[file_path]  
    for e in list(fps.keys()):
        print(e)
    return fps


folders0 = r'''C:\Users\Alexm\AppData\Roaming\Mozilla\Firefox\Profiles\a5nt5bus.default-release\bookmarkbackups
C:\Users\Alexm\AppData\Roaming\Mozilla\Firefox\Profiles\a5nt5bus.default-release\datareporting\archived\2025-06
C:\Users\Alexm\AppData\Roaming\Mozilla\Firefox\Profiles\a5nt5bus.default-release\datareporting\archived\2025-07
C:\Users\Alexm\AppData\Roaming\Mozilla\Firefox\Profiles\a5nt5bus.default-release\sessionstore-backups
C:\Users\Alexm\Desktop\Check_These_Two
C:\Users\Alexm\Desktop\CODE\CuratedCode-GIT\Program_Hacks_and_Site_Scrapes\firefox_in\ignore
C:\Users\Alexm\Desktop\DataToBeRecovered\Firefox\2023-05-18 high priortiy, crash session deleted few days lost
C:\Users\Alexm\Desktop\DataToBeRecovered\Firefox\2023-05-18 high priortiy, crash session deleted few days lost\oooo
C:\Users\Alexm\Desktop\DataToBeRecovered\Firefox\2023-05-18 high priortiy, crash session deleted few days lost\Recovery\Recovery_20230519_000407\Misc\jsonlz4
C:\Users\Alexm\Desktop\DataToBeRecovered\Firefox\2023-06-27  low priority recover lost tab title names
C:\Users\Alexm\Desktop\DataToBeRecovered\Firefox\ff_wholeprevious_gone_5days_26-03-2021
C:\Users\Alexm\Desktop\DataToBeRecovered\Firefox\ff_wholeprevious_gone_5days_26-03-2021\a5nt5bus.default-release\bookmarkbackups
C:\Users\Alexm\Desktop\DataToBeRecovered\Firefox\ff_wholeprevious_gone_5days_26-03-2021\a5nt5bus.default-release\datareporting\archived\2021-02
C:\Users\Alexm\Desktop\DataToBeRecovered\Firefox\ff_wholeprevious_gone_5days_26-03-2021\a5nt5bus.default-release\datareporting\archived\2021-03
C:\Users\Alexm\Desktop\DataToBeRecovered\Firefox\ff_wholeprevious_gone_5days_26-03-2021\a5nt5bus.default-release\sessionstore-backups
C:\Users\Alexm\Desktop\DataToBeRecovered\Firefox\Temp_Restore__09_2021
C:\Users\Alexm\Desktop\DataToBeRecovered\Firefox\Temp_Restore__09_2021\extra after broken
C:\Users\Alexm\Desktop\DataToBeRecovered\Firefox\Temp_Restore__09_2021\temp2
C:\Users\Alexm\Desktop\Delete-In The Future\FIREFOXPROFILEBACKUPa5nt5bus.default-release
C:\Users\Alexm\Desktop\Delete-In The Future\FIREFOXPROFILEBACKUPa5nt5bus.default-release\bookmarkbackups
C:\Users\Alexm\Desktop\Delete-In The Future\FIREFOXPROFILEBACKUPa5nt5bus.default-release\datareporting\archived\2020-11
C:\Users\Alexm\Desktop\Delete-In The Future\FIREFOXPROFILEBACKUPa5nt5bus.default-release\datareporting\archived\2020-12
C:\Users\Alexm\Desktop\Delete-In The Future\FIREFOXPROFILEBACKUPa5nt5bus.default-release\sessionstore-backups
C:\Users\Alexm\Desktop\findi\a
C:\Users\Alexm\Desktop\findi\a\also_search if tab gentically modified skin that is resistant to uv
C:\Users\Alexm\Desktop\Important Data\WebRelated\Check these for missing tabs
C:\Users\Alexm\Desktop\Important Data\WebRelated\firefox_backup_deletable 06Jul20
C:\Users\Alexm\Desktop\Important Data\Z_Firefox_Backup_Restore
C:\Users\Alexm\Desktop\neew\Firefox_Recovery_Tools_and_Scripts\Example_Profile\sessionstore-backups
C:\Users\Alexm\Desktop\PastWebBrowsers\FirefoxPortable_Lapotop2012\Data\profile
C:\Users\Alexm\Desktop\PastWebBrowsers\FirefoxPortable_Lapotop2012\Data\profile\datareporting\archived\2020-03
C:\Users\Alexm\Desktop\PastWebBrowsers\FirefoxPortable_Lapotop2012\Data\profile\datareporting\archived\2020-04
C:\Users\Alexm\Desktop\PastWebBrowsers\FirefoxPortable_Lapotop2012\Data\profile\sessionstore-backups
C:\Users\Alexm\Desktop\PastWebBrowsers\Past_Sessions_Raw_Data\Firefox_Laptop2012
C:\Users\Alexm\Desktop\PastWebBrowsers\Portable__Installers\FirefoxPortable\Data\profile
C:\Users\Alexm\Desktop\PastWebBrowsers\Portable__Installers\FirefoxPortable\Data\profile\datareporting\archived\2020-01
C:\Users\Alexm\Desktop\PastWebBrowsers\_XPS_Firefox_Sessions\Lost Data I think\ff__temp firefox backups
C:\Users\Alexm\Desktop\PastWebBrowsers\_XPS_Firefox_Sessions\Lost Data I think\ff__temp firefox backups\9_9_drive
C:\Users\Alexm\Desktop\PastWebBrowsers\_XPS_Firefox_Sessions\Lost Data I think\ff__temp firefox backups\datareporting\archived\2020-08
C:\Users\Alexm\Desktop\PastWebBrowsers\_XPS_Firefox_Sessions\Lost Data I think\ff__temp firefox backups\datareporting\archived\2020-09
C:\Users\Alexm\Desktop\PastWebBrowsers\_XPS_Firefox_Sessions\Lost Data I think\ff__tempfirefoxbackuodd31jan2020_1423
C:\Users\Alexm\Desktop\PastWebBrowsers\_XPS_Firefox_Sessions\Lost Data I think\ff__zzz
C:\Users\Alexm\Desktop\PastWebBrowsers\_XPS_Firefox_Sessions\Sessions Saved\2021-09-19_to_2021-11-16
C:\Users\Alexm\Desktop\PastWebBrowsers\_XPS_Firefox_Sessions\Sessions Saved\2021-11-16_to_2022-01-13
C:\Users\Alexm\Desktop\PastWebBrowsers\_XPS_Firefox_Sessions\Sessions Saved\2022-01-13_to_2022-03-16
C:\Users\Alexm\Desktop\PastWebBrowsers\_XPS_Firefox_Sessions\Sessions Saved\2022-03-16_to_2022-05-15
C:\Users\Alexm\Desktop\PastWebBrowsers\_XPS_Firefox_Sessions\Sessions Saved\2022-05-15_to_2022-07-08
C:\Users\Alexm\Desktop\PastWebBrowsers\_XPS_Firefox_Sessions\Sessions Saved\2022-07-08_to_2022-09-03
C:\Users\Alexm\Desktop\PastWebBrowsers\_XPS_Firefox_Sessions\Sessions Saved\2022-09-03_to_2022-11-05
C:\Users\Alexm\Desktop\PastWebBrowsers\_XPS_Firefox_Sessions\Sessions Saved\2022-11-05_to_2023-04-14
C:\Users\Alexm\Desktop\PastWebBrowsers\_XPS_Firefox_Sessions\Sessions Saved\2023-04-14_to_2023-07-13\Part2 17thMay-2023 Post
C:\Users\Alexm\Desktop\PastWebBrowsers\_XPS_Firefox_Sessions\Sessions Saved\2023-07-06_to_2023-09-08
C:\Users\Alexm\Desktop\PastWebBrowsers\_XPS_Firefox_Sessions\Sessions Saved\2023-09-08_to_2023-10-29
C:\Users\Alexm\Desktop\PastWebBrowsers\_XPS_Firefox_Sessions\Sessions Saved\2023-10-29_to_2023-12-14
C:\Users\Alexm\Desktop\PastWebBrowsers\_XPS_Firefox_Sessions\Sessions Saved\2023-12-14_to_2024-02-01
C:\Users\Alexm\Desktop\PastWebBrowsers\_XPS_Firefox_Sessions\Sessions Saved\2025-01-08_to_2025_04_19
C:\Users\Alexm\Desktop\PastWebBrowsers\_XPS_Firefox_Sessions\Sessions Saved\2025-04-19_to_2025-07-15
C:\Users\Alexm\Desktop\PastWebBrowsers\_XPS_Firefox_Sessions\Sessions Saved\ff_session_2024_25
C:\Users\Alexm\Desktop\PYQT\PYQT5_Projects\__explorer
C:\Users\Alexm\Desktop\quick_solve'''.splitlines()

folders_ignore = r'''C:\Users\Alexm\Desktop\quick_solve
C:\Users\Alexm\Desktop\PYQT\PYQT5_Projects\__explorer
C:\Users\Alexm\Desktop\neew\Firefox_Recovery_Tools_and_Scripts\Example_Profile
C:\Users\Alexm\Desktop\findi
C:\Users\Alexm\Desktop\Delete-In The Future
C:\Users\Alexm\AppData\Roaming\Mozilla\Firefox\Profiles\a5nt5bus.default-release\datareporting
C:\Users\Alexm\Desktop\Check_These_Two
C:\Users\Alexm\Desktop\CODE\CuratedCode-GIT\Program_Hacks_and_Site_Scrapes\firefox_in\ignore
C:\Users\Alexm\AppData\Roaming\Mozilla\Firefox\Profiles\a5nt5bus.default-release
'''.splitlines()

folders = r'''C:\Users\Alexm\Desktop\PastWebBrowsers
C:\Users\Alexm\Desktop\DataToBeRecovered
C:\Users\Alexm\Desktop\Important Data
'''.splitlines()

#fps = get_filepaths()



for e in folders0:
    z = False
    for ee in folders_ignore:
        if ee in e:
            z = True
    for ee in folders:
        if ee in e:
            z = True
            
    if z:
        continue
    print(e)
del e,z,ee


files_found = {}
for fp in folders0:
    for k in folders:
        if k in fp:
            files_found[k] = files_found.get(k, []) +[fp]  



config = {'Scan date':None,
          'Folders_To_Scan':folders,
          'Folder_To_Ignore':folders_ignore,
          'Files_Last_Found':files_found,
          'Previously_Found_But_Missine':None,
          'Folder_Long_Scan':r"C:\Users\Alexm"}



    






















