# -*- coding: utf-8 -*-
r"""Created on Fri Aug 15 23:54:13 2025@author: Alexm
python "C:\Users\Alexm\Desktop\EasyImportPython\quicks_git\quicks\quick_systemproperties.py" --help

import subprocess

result = subprocess.run(
    ['python', 'target_script.py', '--help'],
    capture_output=True,
    text=True
)

print(result.stdout)



"""



# import wmi

# c = wmi.WMI()
# for system in c.Win32_ComputerSystem():
#     print(f"Manufacturer: {system.Manufacturer}")
#     print(f"Model: {system.Model}")





'''
argparse2
parser = argparse.ArgumentParser(description="Your script description", return_value=True, automatic_single_letter_flag=True )
verbose = parser.add_argument('--verbose', type=bool, default=True, help='Enable verbose output')
filepath = parser.add_argument('--filepath', type=str, help='Path to input file')
color = parser.add_argument('--color', default='red', choices=['red', 'green', 'blue'], help='Choose a color')
level = parser.add_argument('--level', type=int, min=10, max=20, help='Choose a level between 1 and 10')
players = parser.add_argument('--players', type=float, min=1, max=100, help='Choose a level between 1 and 100')

if True:
   args_parsed = parser.parse_args()
   verbose0, filepath0, color0 = args_parsed.verbose, args_parsed.filepath, args_parsed.color
   verbose = args_parsed.verbose


'''
    
    


import sys, os
import platform
import psutil
import math
from datetime import datetime
import socket
# from screeninfo import get_monitors


import argparse

def restricted_int(min_val, max_val):
    def validator(value):
        ivalue = int(value)
        if ivalue < min_val or ivalue > max_val:
            raise argparse.ArgumentTypeError(f"Value must be between {min_val} and {max_val}")
        return ivalue
    return validator

class LevelAction(argparse.Action):
    def __init__(self, option_strings, dest, min_val=None, max_val=None, **kwargs):
        self.min = min_val
        self.max = max_val
        super().__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        ivalue = int(values)
        if self.min is not None and ivalue < self.min:
            raise argparse.ArgumentTypeError(f"Value must be >= {self.min}")
        if self.max is not None and ivalue > self.max:
            raise argparse.ArgumentTypeError(f"Value must be <= {self.max}")
        setattr(namespace, self.dest, ivalue)


    
parser = argparse.ArgumentParser( description="Your script description", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
parser.add_argument('-f', '--filepath', type=str, help='Path to input file')
parser.add_argument('-c', '--color', default='red', choices=['red', 'green', 'blue'], help='Choose a color')  #  help='Choose a color(default: %(default)s)'
parser.add_argument('--level', type=restricted_int(1, 10), help='Choose a level between 1 and 10')
parser.add_argument('--players', action=LevelAction, min_val=1, max_val=100, help='Choose a level between 1 and 100')
args_parsed = parser.parse_args()
verbose, filepath, color = args_parsed.verbose, args_parsed.filepath, args_parsed.color


verbose = args_parsed.verbose



    
    
    








from PyQt5.QtWidgets import QApplication
_app = QApplication(sys.argv)
_screen = _app.screens()[0]
_geometry = _screen.geometry()
_app.quit()




class SystemProperties:
    spyder_enviroment = ('SPYDER_ARGV' in os.environ) or ('SPYDER_ARGS' in os.environ)
    python_version = sys.version
    python_exe = sys.executable
    platform_info = platform.system(), platform.release(), platform.version()      
    platform = sys.platform
    

    cpu_count = psutil.cpu_count(logical=True)
    ram_gb = round(psutil.virtual_memory().total / (1024 ** 3), 2)
    
    time = datetime.now().strftime("%H:%M:%S")
    date = datetime.now().date().isoformat()
    
    screen_pixels = _geometry.width(), _geometry.height()     
    screen_dpi = round(_screen.physicalDotsPerInch(),1)
    screen_inches = tuple([round(e/_screen.physicalDotsPerInch(),1) for e in screen_pixels])
    screen_diagonal_inches = round(math.sqrt(screen_inches[0]**2 + screen_inches[1]**2))
    screen_displayed = screen_displayed = 'XPS-13inchScreen' if screen_diagonal_inches < 15 else None if screen_diagonal_inches < 32 else 'Ultrawide' if screen_diagonal_inches < 36 else  None
    screen_cms =  tuple([round(e*2.54,1) for e in screen_inches])

    script_name = os.path.basename(sys.argv[0])
    script_path = os.path.abspath(sys.argv[0])
    working_directory = os.getcwd()
    
    args = sys.argv[1:]
    args_parsed = vars(args_parsed)
    is_exe = getattr(sys, 'frozen', False)
    
    is_main = __name__ == '__main__'
    ip_address = socket.gethostbyname(socket.gethostname())
    pc_name = [f for f in os.listdir("C:/") if f.endswith(".name")]

    def __init__(self):
        print('\n')
        print('SystemProperties')
        for name in self.__class__.__dict__:
            if not name.startswith('__'):
                if name in ('screen_pixels', 'script_name'):
                    print('')
                print(f"\t{name}: {getattr(self,name)}")
        print('\n\n')
       
       
if __name__ == '__main__':
    SystemProperties()


systemproperties = SystemProperties


print(args_parsed)




