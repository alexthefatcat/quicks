# -*- coding: utf-8 -*-
"""
Created on Sat Jul 11 15:45:43 2026

@author: Alexm
"""
    
    
import sys
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont



func = lambda a,b,z:[f"Source {z} - Item {i+1}" for i in range(a,b)]
data = {"SOURCE 1 DATA BELOW":func(0,70,1),"SOURCE 2 DATA BELOW":func(70,140,2),"SOURCE 3 DATA BELOW":func(140,150,3)}




class SegmentedTableWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Multi-Source Table with Section Dividers')
        self.setGeometry(100, 100, 650, 500)
        
        layout = QVBoxLayout()
        self.segment_divider = True
        
        nrow_index = sum(len(v) for k,v in data.items()) + (len(data) if self.segment_divider else 0)     
        
        # 150 original data rows + 2 divider rows = 152 total rows
        self.table = QTableWidget(nrow_index, 3)
        self.table.setHorizontalHeaderLabels(['Data Field A', 'Data Field B', 'Data Field C'])
        
        dis_inx = 0
        row_inx = 0
        for i,(k,v) in enumerate(data.items()):
            if self.segment_divider:
                self.create_section_divider(row_inx, k)
                row_inx +=1
            for row in v:
                self.create_data_row(row_inx, row, dis_inx)
                row_inx +=1
                dis_inx +=1                    

        layout.addWidget(self.table)
        self.setLayout(layout)

    def create_data_row(self, row_idx, text_prefix, visual_index = None):
        """Helper to populate standard data cells"""
        if visual_index is not None:
            self.table.setVerticalHeaderItem(row_idx, QTableWidgetItem(str(visual_index)))
        
        for col in range(3):
            item = QTableWidgetItem(f"{text_prefix}, Col {col + 1}")
            self.table.setItem(row_idx, col, item)

    def create_section_divider(self, row_idx, title):
        """Creates a stylized, unselectable gap spanning all columns"""
        # 1. Clear the row number for the divider so it looks like a clean break
        self.table.setVerticalHeaderItem(row_idx, QTableWidgetItem(""))
        self.table.setRowHeight(row_idx, 14)
        
        # 2. Merge all 3 columns into 1 single wide cell
        self.table.setSpan(row_idx, 0, 1, 3)
        
        # 3. Create and style the divider item
        divider = QTableWidgetItem(f" ─── {title} ───")
        divider.setFlags(Qt.NoItemFlags) # Unclickable/uneditable
        divider.setTextAlignment(Qt.AlignCenter)
        
        # Optional: Give it a light gray/blue background highlight
        divider.setBackground(QColor("#f0f4f8"))
        divider.setForeground(QColor("#555555"))
        
        font = QFont()
        font.setBold(True)
        font.setPointSize(9)
        divider.setFont(font)
        
        self.table.setItem(row_idx, 0, divider)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SegmentedTableWidget()
    ex.show()
    sys.exit(app.exec_())    
    
    






