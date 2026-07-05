
 
'''

have a contextmanger where block of code has a title indented colored red and line number



'''


 

from contextlib import contextmanager

@contextmanager
def red_indented_output(indent=4, color='red'):
    import sys
    from io import StringIO
    
    class RedIndentedStream:
        def __init__(self, stream, indent):
            self.stream = stream
            self.indent = ' ' * indent
            self.captured_output = StringIO()

        def write(self, text):
            if text.strip():  # Only color non-empty lines
                red_text = f"\033[31m{text}\033[0m"
                self.stream.write(self.indent + red_text+'\n')
            self.captured_output.write(text)
            
        def flush(self):
            self.stream.flush()

    old_stdout = sys.stdout
    red_stream = RedIndentedStream(sys.stdout, indent)
    sys.stdout = red_stream
    messages = []
    try:
        yield messages
    finally:
        messages.extend(red_stream.captured_output.getvalue().splitlines())
        sys.stdout = old_stdout

print('a')

with red_indented_output() as messages:
    print(6)
    print(7)

# Print the captured messages
print(messages)
print('d')


'''
####################################################################
#                   The Title of the Block(Line_no=)               #
####################################################################
'''


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[96m'

print(f">>{bcolors.OKGREEN}Yes we can set any Hex color in terminal?{bcolors.ENDC}<<")
print(f"{bcolors.OKBLUE}Yes we can set any Hex color in terminal?{bcolors.ENDC}")


import os

@contextmanager
def temporary_directory(new_dir):
    old_dir = os.getcwd()
    os.chdir(new_dir)
    try:
        yield
    finally:
        os.chdir(old_dir)


import time

@contextmanager
def timer():
    start = time.time()
    yield
    end = time.time()
    print(f'Time taken: {end - start} seconds')

with timer():
    # Code to be timed