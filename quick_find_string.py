# -*- coding: utf-8 -*-
"""Created on Sat Aug  5 23:32:09 2023@author: Alexm"""
import os

def quick_find_string(msgs, all_in=None, one_in=None, not_in=None, just_one_in=None, starts_with=None, ends_with=None, case_sensative=False, return_failed=True):

    def split_list(lis, func):
        lis_a, lis_b = [],[]
        for e in lis:
            if func(e):
                lis_a.append(e)
            else:
                lis_b.append(e)
        return lis_a, lis_b
    
    
    #contains_one, contains_all, contains_one, contains_none
    def find_string(all_in=None, one_in=None, not_in=None, just_one_in=None, starts_with=None, ends_with=None, case_sensative=False):
        'one_in # atleast one in, '
        
        def correct_case(msg):
            return msg if case_sensative else msg.lower()
        
        def correct_arg(arg):
            if arg is None:
                return []
            if isinstance(arg,str):
                return [arg]
            return [correct_case(e) for e in arg]
        
        all_in = correct_arg(all_in)
        one_in = correct_arg(one_in)
        not_in = correct_arg(not_in)
        just_one_in = correct_arg(just_one_in) 
        starts_with = correct_arg(starts_with)
        ends_with = correct_arg(ends_with)    
        
        def function(msg):
            msg0 = correct_case(msg)
            if not all([e in msg0 for e in all_in]):
                return False
            if len(one_in)>0:
                if not any([e in msg0 for e in one_in]):
                    return False             
            if any([e in msg0 for e in not_in]):
                return False        
            if (len(just_one_in)>0) and (sum([e in msg0 for e in just_one_in])!=1):
                return False   
            if len(starts_with)>0:
                if not any([msg.startswith(e) for e in starts_with]):
                    return False    
            if len(ends_with)>0:
                if not any([msg.endswith(e) for e in ends_with]):
                    return False               
            return True           
        return function    
      
    msgs0, msgs1 = split_list(msgs, find_string(all_in, one_in, not_in, just_one_in, starts_with, ends_with, case_sensative))
    if return_failed:
        return msgs0, msgs1
    return msgs0


