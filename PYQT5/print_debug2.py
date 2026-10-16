# -*- coding: utf-8 -*-
"""
Created on Wed Sep  2 13:41:19 2026

@author: alexm

colors
and line number


"""

import inspect

DEBUG = True

def print_debug(*args, limit=None, **kwargs):
    # Initialize a dictionary to track counts per line of code
    if not hasattr(print_debug, "counts"):
        print_debug.counts = {}

    if DEBUG:
        if limit is not None:
            # 1. Identify exactly which file and line of code called this function
            frame = inspect.currentframe().f_back
            call_site = (frame.f_code.co_filename, frame.f_lineno)
            
            # 2. Get the current count for this specific line (defaulting to 0)
            count = print_debug.counts.get(call_site, 0)
            
            # 3. Stop if this specific line has hit its limit
            if count >= limit:
                return
            
            # 4. Print and increment the count for this specific line
            print(*args, **kwargs)
            print_debug.counts[call_site] = count + 1
        else:
            # If no limit was asked for, just print normally and don't track it
            print(*args, **kwargs)





if __name__ == '__main__':
    # --- TEST ---
    
    for i in range(15):
        # This line has its own limit of 3
        print_debug(f'First Loop Iteration: {i}', limit=3)
    
    print_debug("\n--- This print is completely unaffected! ---\n")
    
    for i in range(15):
        # This line has its own separate limit of 2
        print_debug(f'Second Loop Iteration: {i}', limit=2)