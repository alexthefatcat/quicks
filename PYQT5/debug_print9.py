# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 21:55:03 2026

@author: alexm
"""



import inspect
import time
from contextlib import ContextDecorator

class print_debug(ContextDecorator):
    """3-in-1 Debug Utility:
    
    1. Standalone Call: print_debug_context("Label")
       -> Prints a 1-line checkpoint with current variables immediately.
       
    2. Context Manager: with print_debug_context("Label"):
       -> Measures block timing; dumps locals if an exception occurs.
       
    3. Decorator: @print_debug_context("Label")
       -> Wraps function execution.
    """
    def __init__(self, label: str = "Debug Point", show_locals: bool = True):
        self.label = label
        self.show_locals = show_locals
        
        # Inspect caller frame & source line
        frame = inspect.currentframe().f_back
        info = inspect.getframeinfo(frame)
        self.filename = info.filename.split("/")[-1]
        self.lineno = info.lineno

        # Detect usage mode from caller's source code line
        line = info.code_context[0].strip() if info.code_context else ""
        self.is_block = line.startswith("with ") or line.startswith("@")

        # Standalone call: print point-in-time snapshot immediately
        if not self.is_block:
            self._print_inline(frame)

    def _print_inline(self, frame):
        locals_dict = frame.f_locals
        user_vars = {k: v for k, v in locals_dict.items() if not k.startswith("__")}
        
        if user_vars and self.show_locals:
            vars_str = ", ".join(f"{k}={repr(v)}" for k, v in user_vars.items())
            print(f"[DEBUG INLINE] {self.label} ({self.filename}:{self.lineno}) ── {vars_str}")
        else:
            print(f"[DEBUG INLINE] {self.label} ({self.filename}:{self.lineno})")

    def __enter__(self):
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        elapsed_ms = (time.perf_counter() - self.start_time) * 1000

        # Success inside context manager/decorator
        if exc_type is None:
            print(f"[DEBUG BLOCK]  {self.label} ({self.filename}:{self.lineno}) — SUCCESS ({elapsed_ms:.2f}ms)")
            return True

        # Exception inside context manager/decorator
        print(f"\n┌── [DEBUG FAILED] {self.label} ({self.filename}:{self.lineno}) — {elapsed_ms:.2f}ms")
        print(f"├── ❌ EXCEPTION: {exc_type.__name__}: {exc_val}")
        if self.show_locals and exc_tb:
            tb = exc_tb
            while tb.tb_next:
                tb = tb.tb_next
            locals_dict = tb.tb_frame.f_locals
            print("├── 🔍 Local variables at failure:")
            for k, v in locals_dict.items():
                if not k.startswith("__"):
                    print(f"│     • {k} = {repr(v)}")
        print("└── [DEBUG END]\n")
        return False
    
    
    
# 1. Standalone Inline Call
a = 3
print_debug("Process Batch")
b = 9

# 2. Context Manager Block
with print_debug("Data Transformation"):
    items = [1, 2, 3]

# 3. Decorator Usage
@print_debug("Run Pipeline")
def run():
    return True

run()    
    
    
    

    
    
    
    
    
import re

class print_debug_loops:
    def __init__(self, title, number=10):
        self.title = title
        self.number = number
        self.logs = []

    def __enter__(self):
        def log(msg):
            self.logs.append(msg)
        return log

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"#{self.title}:-")
        total = len(self.logs)
        if total > 0:
            step = total / self.number
            for i in range(self.number):
                idx = int((i + 0.5) * step)
                msg = re.sub(r'\b\d{4,}\b', lambda m: f"{int(m.group(0)):,}", self.logs[idx])
                print(f"\t#{idx:03d}/{total}: {msg}")

# Usage
def foo(n):
    return n**2

elements = list(range(1000))

with print_debug_loops("Square Numbers", 10) as print_debug_loop:
    out = []
    for n in elements:
        v = foo(n)
        out.append([n, v])
        print_debug_loop(f"Score {n} -> {v}")    
    
    
    


    
    
        
    
'''
print_debug_prefix = '#>> '
    
# 1. Standalone Inline Call
a = 3
print_debug("Process Batch")
b = 9

# 2. Context Manager Block
with print_debug("Data Transformation"):
    items = [1, 2, 3]

# 3. Decorator Usage
@print_debug("Run Pipeline")
def run():
    return True

run()    
    
    
    
    
    
with print_debug("Square Numbers", 10) as print_debug_loop:
    out = []
    for n in elements:
        v = foo(n)
        out.append([n, v])
        print_debug_loop(f"Score {n} -> {v}")    






'''    
    
    
    
    
    
    
    
    
    
    
    
    