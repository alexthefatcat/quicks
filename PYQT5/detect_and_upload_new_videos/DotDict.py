# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 02:09:47 2026

@author: alexm
"""

class DotDict(dict):
    """A dictionary that allows dot notation access to its keys."""
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(f"'DotDict' object has no attribute '{key}'")

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError:
            raise AttributeError(f"'DotDict' object has no attribute '{key}'")



