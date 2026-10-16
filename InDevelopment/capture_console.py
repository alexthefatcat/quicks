# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 00:25:14 2026

@author: alexm
"""

import builtins
from contextlib import contextmanager
import sys


@contextmanager
def capture_console():
    captured = []

    # Store original references
    original_stdout = sys.stdout
    original_input = builtins.input

    # 1. Tee stdout wrapper: prints normally and logs non-empty lines
    class TeeStdout:

        def write(self, text):
            original_stdout.write(text)
            clean_text = text.strip()
            if clean_text:
                captured.append({"type": "print", "content": clean_text})

        def flush(self):
            original_stdout.flush()

    # 2. Intercept input(): prompts user normally and logs prompt + response
    def custom_input(prompt=""):
        prompt_str = str(prompt)

        # Prompt the user via standard terminal input
        user_response = original_input(prompt_str)

        if prompt_str.strip():
            captured.append({"type": "prompt", "content": prompt_str.strip()})
        captured.append({"type": "input", "content": user_response})

        return user_response

    # Hijack streams
    sys.stdout = TeeStdout()
    builtins.input = custom_input

    try:
        yield captured
    finally:
        # Guarantee restoration even if an exception occurs inside the with-block
        sys.stdout = original_stdout
        builtins.input = original_input


# --- Usage Example ---

with capture_console() as logs:
    print("Welcome to the CLI App!")
    name = input("Enter your username: ")
    print(f"Hello, {name}!")
    age = input("Enter your age: ")
    print("Setup complete.")

# --- Inspect Captured Results Outside Context Manager ---
print("\n=== Captured Session Log ===")
for entry in logs:
    print(f"[{entry['type'].upper():7}] {entry['content']}")
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    