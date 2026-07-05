# -*- coding: utf-8 -*-
"""
Created on Sun Aug 17 03:41:15 2025

@author: Alexm
"""


import quick_systemproperties



import argparse
parser = argparse.ArgumentParser( description="Your script description", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
parser.add_argument('-f', '--filepath', type=str, help='Path to input file')
parser.add_argument('-c', '--color', default='red', choices=['red', 'green', 'blue'], help='Choose a color')  #  help='Choose a color(default: %(default)s)'

args_parsed = parser.parse_args()
verbose = args_parsed.verbose




from  quick_systemproperties import parser








if False:
    import subprocess
    result = subprocess.run(['python', 'quick_systemproperties.py', '--help'], capture_output=True, text=True)
    print(result.stdout)
    
    
    








import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QCheckBox, QComboBox, QFileDialog
)


if False:
    
    class ArgparseGUI(QWidget):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Argparse GUI")
            self.init_ui()
    
        def init_ui(self):
            layout = QVBoxLayout()
    
            # Verbose checkbox
            self.verbose_checkbox = QCheckBox("Enable verbose output")
            layout.addWidget(self.verbose_checkbox)
    
            # Filepath input
            file_layout = QHBoxLayout()
            self.file_input = QLineEdit()
            file_button = QPushButton("Browse")
            file_button.clicked.connect(self.browse_file)
            file_layout.addWidget(QLabel("Filepath:"))
            file_layout.addWidget(self.file_input)
            file_layout.addWidget(file_button)
            layout.addLayout(file_layout)
    
            # Color dropdown
            self.color_dropdown = QComboBox()
            self.color_dropdown.addItems(["red", "green", "blue"])
            color_layout = QHBoxLayout()
            color_layout.addWidget(QLabel("Color:"))
            color_layout.addWidget(self.color_dropdown)
            layout.addLayout(color_layout)
    
            # Run button
            run_button = QPushButton("Run")
            run_button.clicked.connect(self.run_script)
            layout.addWidget(run_button)
    
            self.setLayout(layout)
    
        def browse_file(self):
            filepath, _ = QFileDialog.getOpenFileName(self, "Select File")
            if filepath:
                self.file_input.setText(filepath)
    
        def run_script(self):
            verbose = self.verbose_checkbox.isChecked()
            filepath = self.file_input.text()
            color = self.color_dropdown.currentText()
    
            print(f"Verbose: {verbose}")
            print(f"Filepath: {filepath}")
            print(f"Color: {color}")
    
    if __name__ == "__main__":
        app = QApplication(sys.argv)
        gui = ArgparseGUI()
        gui.show()
        sys.exit(app.exec_())
        
        
else:
        
        
        
    
    
    class ArgparseGUI(QWidget):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Argparse GUI")
            self.init_ui()
    
        def init_ui(self):
            layout = QVBoxLayout()
            

            for action in parser._actions:
                if action.dest not in ['help']:
                    print(action.dest)
                    print("  Argument:", action.option_strings)
                    print("  Help:", action.help)
                    print("  Default:", action.default)
                    print("  Choices:", action.choices)
                    # maybe use this so that you know what the user set as its default incases where he did None
                    explicit_default = parser.get_default(action.dest)        
                    print('\n')



    
            # Verbose checkbox
            self.verbose_checkbox = QCheckBox("Enable verbose output")
            layout.addWidget(self.verbose_checkbox)
    
            # Filepath input
            file_layout = QHBoxLayout()
            self.file_input = QLineEdit()
            file_button = QPushButton("Browse")
            file_button.clicked.connect(self.browse_file)
            file_layout.addWidget(QLabel("Filepath:"))
            file_layout.addWidget(self.file_input)
            file_layout.addWidget(file_button)
            layout.addLayout(file_layout)
    
            # Color dropdown
            self.color_dropdown = QComboBox()
            self.color_dropdown.addItems(["red", "green", "blue"])
            color_layout = QHBoxLayout()
            color_layout.addWidget(QLabel("Color:"))
            color_layout.addWidget(self.color_dropdown)
            layout.addLayout(color_layout)
    
            # Run button
            run_button = QPushButton("Run")
            run_button.clicked.connect(self.run_script)
            layout.addWidget(run_button)
    
            self.setLayout(layout)
    
        def browse_file(self):
            filepath, _ = QFileDialog.getOpenFileName(self, "Select File")
            if filepath:
                self.file_input.setText(filepath)
    
        def run_script(self):
            verbose = self.verbose_checkbox.isChecked()
            filepath = self.file_input.text()
            color = self.color_dropdown.currentText()
    
            print(f"Verbose: {verbose}")
            print(f"Filepath: {filepath}")
            print(f"Color: {color}")
    
    if __name__ == "__main__":
        app = QApplication(sys.argv)
        gui = ArgparseGUI()
        gui.show()
        sys.exit(app.exec_())
    
        
        
for key, value in args_parsed.__dict__.items():
    print(f"{key}: {value}")        
        
    
# Loop through all actions
for action in parser._actions:
    if '--verbose' in action.option_strings or '-v' in action.option_strings:
        print("Argument:", action.option_strings)
        print("Help:", action.help)
        print("Default:", action.default)
        print("Choices:", action.choices)
        print("Required:", action.required)
        print("Type:", action.type)


    
action.__dict__    
    









if False: # Nice UI works as wanted 
    
    info = {}
    
    for action in parser._actions:
        if action.dest not in ['help']:
            info0 = {}
            print(action.dest)
            print("  Argument:", action.option_strings)
            print("  Help:", action.help)
            print("  Default:", action.default)
            print("  Choices:", action.choices)
            # maybe use this so that you know what the user set as its default incases where he did None
            explicit_default = parser.get_default(action.dest)        
            print('\n')
            
            info0['Name'] = action.dest        
            info0['Argument'] = action.option_strings
            info0['Help'] = action.help    
            info0["Default"] = action.default
            info0["Choices"] = action.choices
            info[action.dest] = info0
    
    
    from pyqt_utils import QVBoxWidgets, MainWindow
    
    class GroupedWidgets(QVBoxWidgets):
        def __init__(self):
            super().__init__()
            
            buttons_dict = {}
            for i, (k,v) in enumerate(info.items()):
                button = QPushButton(f"Button {i}")
                line_edit = QLineEdit()
                line_edit.setPlaceholderText(f"Enter text for Group {i}")
                buttons_dict[k] = QVBoxWidgets([button, line_edit], vertical=False, margins=0)
                
            buttons_widget = QVBoxWidgets(buttons_dict)
            self.addWidget(buttons_widget)
            run_button = QPushButton("Run")  
            self.addWidget(run_button)
            
            
    
    if __name__ == "__main__":
        central_widget = GroupedWidgets()
        app = QApplication(sys.argv)
        window = MainWindow(central_widget, size=(550, 0), title='Select Argument Value')
        window.show()
        sys.exit(app.exec_())
    
    
    
    






    