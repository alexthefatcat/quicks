# -*- coding: utf-8 -*-
"""Created on Fri Dec 29 16:35:29 2023@author: Alexm"""

def string_swap(msg, dic, inverse=True):
    dic2 = dic.copy()
    if inverse:
        dic2 = {v:k for k,v in dic2.items()}|dic2
    return ''.join([dic2.get(e,e) for e in msg])

if False:
    pass
    # string_splits(msg, splitters, remove_blank=False,prefix_split=False)
    # prefix_split the splitters are not removed but prefixed to followeing sting
    