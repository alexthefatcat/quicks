# -*- coding: utf-8 -*-
"""Created on Sat Apr 26 11:09:46 2025@author: Alexm"""








import sys, io

class CapturePrint:
    def __init__(self, show_in_ide=True):
        self.captured_output = io.StringIO()
        self.show_in_ide = show_in_ide

    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = self
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        sys.stdout = self._original_stdout

    def write(self, message):
        """ Capture output and optionally print to IDE. """
        self.captured_output.write(message)
        if self.show_in_ide:
            self._original_stdout.write(message)

    def flush(self):
        """ Required method for sys.stdout compatibility. """
        pass

    def get_output(self):
        return self.captured_output.getvalue()

    def __str__(self):
        return self.get_output()



if __name__ == "__main__":
    # Usage examples:
    with CapturePrint(show_in_ide=True) as captured_print:
        print("This will appear in the IDE and be captured.")
    
    with CapturePrint(show_in_ide=False) as captured_print:
        print("This will only be captured, not printed in the IDE.")
    
    # Retrieve captured output
    print("\nCaptured output from second block:")
    print(captured_print.get_output())
    
