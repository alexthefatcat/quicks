# -*- coding: utf-8 -*-
"""
Created on Sat Sep 27 05:44:02 2025

@author: Alexm
"""


import os, time

def print_recent_python_files_in_the_last_50_days(ndays=50, folder=os.path.join(os.path.expanduser("~"), "Desktop"),ext='.py'):
    desktop_path = folder
    time_threshold = time.time() - (ndays * 86400)  # 86400 seconds in a day
    for root, dirs, files in os.walk(desktop_path):
        for file in files:
            if file.endswith(ext):
                full_path = os.path.join(root, file)
                if os.path.getmtime(full_path) >= time_threshold:
                    print(full_path)
