# -*- coding: utf-8 -*-
"""Created on Sat Aug 12 04:17:16 2023@author: Alexm"""

def quick_todays_date(verbose=False):
    if verbose:
        print(  'from datetime import date\ntoday = date.today().isoformat() ')
    from datetime import date    
    return date.today().isoformat()






