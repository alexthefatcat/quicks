# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 04:57:40 2026

@author: alexm
"""

import time
import inspect
import os
from contextlib import contextmanager

@contextmanager
def print_debug(*args, **kwargs):
    '''
    with print_debug('Excute for loop'):
    '''

    start = time.perf_counter()
    yield
    elapsed = time.perf_counter() - start
    
    # Get the frame where the 'with' block ended
    caller_frame = inspect.currentframe().f_back.f_back
    
    # Extract line number and short filename (e.g., 'search.py:42')
    line_num = caller_frame.f_lineno
    file_name = os.path.basename(caller_frame.f_code.co_filename)
    
    print('\033[33m# [', *args, f'] completed in {elapsed:.2f}s ({file_name}:{line_num})\033[0m',**kwargs)
    # [Building Searcher] completed in 1.45s (data_pipeline.py:108)
    
    
    
    
    
    
    
    
    
    
if __name__ == '__main__':
    with print_debug('Excute for loop'):
        for n in range(100):
            m = n+1
    
    