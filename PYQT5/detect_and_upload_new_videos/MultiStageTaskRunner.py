# -*- coding: utf-8 -*-
"""Created on Fri Sep  4 01:03:00 2026@author: alexm





include table so table could be all results output
color could be a pass and fail on each if its not working

extract help from the function help


input('asdfsadfsa')







Ideas
    what to do about input('')
    I want tables to show nicly
    I want to update progress bar
    




maybe some hints in print

**progressbar(23/40)  ?
 we detect this and update progress bar

















"""

from get_function_parameter_names import get_function_parameter_names


from PyQt5.QtWidgets import  QTabWidget, QVBoxLayout, QLabel, QPushButton, QProgressBar, QTableWidget, QTableWidgetItem, QTextEdit
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication
from QBox_Widget import QBox_Widget
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import QTabBar, QStylePainter, QStyleOptionTab, QStyle


class ColorTabBar(QTabBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._bg_colors = {}

    def setTabBackgroundColor(self, index, color):
        """Custom method to store and trigger background colors."""
        # Convert string color names or hex strings automatically to QColor
        if isinstance(color, str):
            color = QColor(color)
        self._bg_colors[index] = color
        self.update()

    def paintEvent(self, event):
        painter = QStylePainter(self)
        option = QStyleOptionTab()

        for i in range(self.count()):
            self.initStyleOption(option, i)
            
            if i in self._bg_colors:
                # 1. Fill the tab rectangle with your custom color
                rect = self.tabRect(i)
                painter.fillRect(rect, self._bg_colors[i])
                
                # 2. Draw ONLY the label (text/icon) over your custom background
                painter.drawControl(QStyle.CE_TabBarTabLabel, option)
            else:
                # Standard native rendering for uncolored tabs
                painter.drawControl(QStyle.CE_TabBarTab, option)









class DotDict(dict):
    """A dictionary that allows dot.notation access to its keys."""
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(f"'TaskState' has no attribute '{key}'")
    def __setattr__(self, key, value):
        self[key] = value
    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError:
            raise AttributeError(f"'TaskState' has no attribute '{key}'")


colors = DotDict({'green':"#d1e7dd", 'orange':"#fee9cc",
                   'red':"#ffe5d9",   'grey':"#f6f8f9",
                    'white':"#ffffff", 'blue':'#edf4ff'})         # '#cfe2ff'
        

colors.not_ran= colors.grey
colors.running = colors.blue
colors.crash = colors.red
colors.ran_good = colors.green
colors.ran_bad = colors.orange



data = [ ("Alice", "28"),("Bob", "34"),("Charlie", "22")    ]

class QTableWidget2(QTableWidget):
    def __init__(self, data, columns):
        irow = len(data)
        icol = len(columns)
        super().__init__(irow ,icol)
        self.setHorizontalHeaderLabels(columns)
        
        for row_index, row in enumerate(data):
            for col_index, value in enumerate(row):
                self.setItem(row_index, col_index, QTableWidgetItem(str(value)))
                
    def append(self, new_row):
        row_position = self.rowCount()
        self.insertRow(row_position)
        for col_index,val in enumerate(new_row):
            self.setItem(row_position, col_index, QTableWidgetItem(str(val)))


class MultiStageTaskRunner(QMainWindow):
    def __init__(self, stages, stage_names=None):
        super().__init__()
        self.stages = stages
        self.stage_names = stage_names
        self.shared_scope = DotDict()
        self.setWindowTitle("MultiStageTaskRunner")
        self.resize(700, 450)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        self.tabs = QTabWidget()
        
        custom_tab_bar = ColorTabBar(self.tabs)
        self.tabs.setTabBar(custom_tab_bar)


        
        
        self.tabs_list = []
        self.tabs_widgets = []
        

        #First Tab Which Should be a Note
        tab = QWidget()
        tab_layout = QVBoxLayout()
        label_text = "Notes about the differnt stages:-"

        if not self.stage_names is None:
            for k,v in self.stage_names.items():
                    label_text = label_text + f'\n\t{k}'
        
        tab_label = QLabel(label_text)        
        tab_layout.addWidget(tab_label)
        self.run_all =  QPushButton('Run All')
        tab_layout.addWidget(self.run_all)        
        tab.setLayout(tab_layout)            
        self.tabs_list.append(tab)           
        self.tabs.addTab(tab, 'MainMenu')         
     
        
        self.data = DotDict()
        for i, stage in enumerate(stages,1):
            tab, tabs_widget = self.create_tab_widget(i, stage)
            self.tabs_list.append(tab)
            
            self.connect_tab_widgets(stage, tabs_widget) 
            
            self.tabs.addTab(tab, f'Stage {i}')
            if not self.stage_names is None:
                tab_name = list(self.stage_names.keys())[i-1]
                self.tabs.setTabToolTip(i, tab_name)

            self.tabs_widgets.append(tabs_widget)  
        
        if False:
            self.tabs.setTabEnabled(0, True)        
            for i, stage in enumerate(stages,1):
                self.tabs.setTabEnabled(i, False)
            self.tabs.setTabEnabled(1, True)
        
        main_layout.addWidget(self.tabs)
        self.status_label = QLabel("Status: Not Running")
        main_layout.addWidget(self.status_label)



    def create_tab_widget(self, i, stage):
        
        title = None
        if not self.stage_names is None:
            tab_name = list(self.stage_names.keys())[i-1]
            title =  QLabel(f"<b>{tab_name}</b>")

        tabs_widget = DotDict()
        
        tabs_widget.run_btn = QPushButton('Run')
        tabs_widget.progress_bar = QProgressBar()           
        tabs_widget.label = QLabel("Welcome to the first tab!")
        tabs_widget.tab_i = i        
        
        tabs_widget.table = None
        if False:
            tabs_widget.table = QTableWidget2(data, columns=["Name", "Age"])
        
        tabs_widget.text_box = QTextEdit()
        tabs_widget.text_box.setPlainText('')
        tabs_widget.text_box.setLineWrapMode(QTextEdit.NoWrap)
        
        tabs_widget.progress_and_run_btn = QBox_Widget.H(tabs_widget.progress_bar, tabs_widget.run_btn)
        tab = QBox_Widget.V(title, tabs_widget.progress_and_run_btn, tabs_widget.label, tabs_widget.table, tabs_widget.text_box)  
        
        return tab, tabs_widget        


    def connect_tab_widgets(self, stage, tabs_widget):
        tabs_widget.run_btn.clicked.connect(lambda :self.run_code(stage, tabs_widget ))
        
    def run_code(self, stage, tabs_widget ):
        msg = ''
        self.color_textbox(tabs_widget.text_box, colors.running) 
        paramaters = [msg]
        parameter_info_all = get_function_parameter_names(stage) 
        parameter_info = parameter_info_all[1]
        if len(parameter_info)>0:
            if parameter_info[-1] in ('shared_scope', 'session'):
                paramaters.append(self.shared_scope)
        
        self.status_label.setText('Status:Running...')
        self.color_textbox(tabs_widget.text_box, colors.running)  
        QApplication.processEvents()        
        for msg in stage(*paramaters):
            print(msg)
            tabs_widget.text_box.setPlainText(msg)
            QApplication.processEvents() 
        self.color_textbox(tabs_widget.text_box, colors.ran_good)        
        self.status_label.setText("Status: Not Running")
        self.tabs.tabBar().setTabBackgroundColor(tabs_widget.tab_i, colors.ran_good)

    def color_textbox(self, text_box, color='red'):
        palette = text_box.palette()
        if color in colors.keys():
            color = colors.get(color, "#ffffff")
        palette.setColor(QPalette.Base, QColor(color)) 
        text_box.setPalette(palette)            
        
































    
    