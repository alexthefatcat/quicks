# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 02:00:30 2026

@author: alexm
"""


    
  
import inspect
from typing import NamedTuple, List, Optional

class GroupedParameters(NamedTuple):
    positional_only: List[str]
    positional_or_keyword: List[str]
    var_positional: Optional[str]        # *args stored here only
    keyword_only: List[str]
    var_keyword: Optional[str]           # **kwargs stored here only
    parameter_names: List[str]          # Standard arguments only


def get_function_parameter_names(func) -> GroupedParameters:
    sig = inspect.signature(func)
    
    pos_only = []
    pos_or_kw = []
    var_pos = None
    kw_only = []
    var_kw = None
    parameter_names = []
    
    for name, param in sig.parameters.items():
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            var_pos = name
        elif param.kind == inspect.Parameter.VAR_KEYWORD:
            var_kw = name
        else:
            # Only add standard named arguments to parameter_names
            parameter_names.append(name)
            
            if param.kind == inspect.Parameter.POSITIONAL_ONLY:
                pos_only.append(name)
            elif param.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD:
                pos_or_kw.append(name)
            elif param.kind == inspect.Parameter.KEYWORD_ONLY:
                kw_only.append(name)

    return GroupedParameters(
        positional_only=pos_only,
        positional_or_keyword=pos_or_kw,
        var_positional=var_pos,
        keyword_only=kw_only,
        var_keyword=var_kw,
        parameter_names=parameter_names
    )
    
    
    
    