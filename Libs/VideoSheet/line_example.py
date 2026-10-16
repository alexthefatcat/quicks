# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 23:57:45 2026

@author: alexm



"""

import sys
from PyQt5.QtCore import Qt, QPoint, QTimer, QEvent
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QListWidget, QTableWidget, 
    QTableWidgetItem, QHeaderView, QVBoxLayout,QLabel
)


if False:   

    class ExampleWidget(QWidget):
        def __init__(self):
            super().__init__()   
            self.setWindowTitle("Synced List & Table with Overlay Lines")    
            self.resize(750, 500)        
    
            self.layout = QHBoxLayout(self)
            self.layout.setSpacing(0)  # Seamless edge joining
            
            # 1. List Widget (Names) - Renamed to gridlist
            self.gridlist = QListWidget(self)
    
            # 2. Table Widget (Names & Ages) - Renamed to table
            self.table = QTableWidget(100, 2, self)
            self.table.setHorizontalHeaderLabels(["Name", "Age"])
            self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            
            sb_list = self.gridlist.verticalScrollBar()
            sb_table = self.table.verticalScrollBar()
            sb_list.valueChanged.connect(sb_table.setValue)
            sb_table.valueChanged.connect(sb_list.setValue)        
    
            # Populate 100 items into both widgets
            for i in range(100):
                name = f"User {i + 1}"
                age = str(20 + (i % 45))
                
                self.gridlist.addItem(name)
                self.table.setItem(i, 0, QTableWidgetItem(name))
                self.table.setItem(i, 1, QTableWidgetItem(age))
    
            # Table is on the LEFT, List is on the RIGHT
            self.layout.addWidget(self.table)
            self.layout.addWidget(self.gridlist)
    
    
    class SyncedListTableWidget(ExampleWidget):
        def __init__(self):
            super().__init__()
            self.setup_overlay()
            self.setup_scroll_sync()
        
        def setup_overlay(self):
            self.overlay = QWidget(self)
            self.overlay.setAttribute(Qt.WA_TransparentForMouseEvents, True)
            self.overlay.setAttribute(Qt.WA_TranslucentBackground, True)
            self.overlay.installEventFilter(self)
            self.overlay.show()        
            
        def eventFilter(self, obj, event):
            # When the overlay is told to paint, intercept it and draw your lines
            if obj is self.overlay and event.type() == QEvent.Paint:
                self.draw_overlay_lines(self.overlay)
                return False 
                
            return super().eventFilter(obj, event)
    
        def setup_scroll_sync(self):
            sb_list = self.gridlist.verticalScrollBar()
            sb_table = self.table.verticalScrollBar()
    
            # Defer overlay repaints by 1 tick so item rect coordinates update before painting
            sb_list.valueChanged.connect(lambda: QTimer.singleShot(0, self.overlay.update))
            sb_table.valueChanged.connect(lambda: QTimer.singleShot(0, self.overlay.update))
    
    
        def update_overlay_geometry(self):
            """Stretches overlay geometry across the full combined width of list & table."""
            if not hasattr(self, 'overlay') or not hasattr(self, 'gridlist'):
                return
    
            # Use the table for X-coordinate since it is on the LEFT
            table_global = self.table.mapToGlobal(QPoint(0, 0))
            table_local = self.mapFromGlobal(table_global)
    
            total_width = self.gridlist.width() + self.table.width()
    
            self.overlay.setGeometry(
                table_local.x(),
                table_local.y(),
                total_width,
                max(self.gridlist.height(), self.table.height())
            )
            self.overlay.raise_()
    
        def showEvent(self, event):
            super().showEvent(event)
            self.update_overlay_geometry()
    
        def resizeEvent(self, event):
            super().resizeEvent(event)
            self.update_overlay_geometry()
    
        def draw_overlay_lines(self, overlay_widget):
            count = self.gridlist.count()
            if count == 0:
                return
    
            viewport = self.gridlist.viewport()
            vh = viewport.height()
    
            viewport_global = viewport.mapToGlobal(QPoint(0, 0))
            viewport_y = overlay_widget.mapFromGlobal(viewport_global).y()
    
            painter = QPainter(overlay_widget)
            painter.setPen(QPen(QColor(255, 50, 50), 2))  # Red accent divider line
    
            start_x = 0
            end_x = overlay_widget.width()
    
            step = 2
            for idx in range(step - 1, count, step):
                item = self.gridlist.item(idx)
                if not item:
                    continue
    
                rect = self.gridlist.visualItemRect(item)
    
                if rect.isValid() and 0 <= rect.bottom() <= vh:
                    y = viewport_y + rect.bottom()
                    painter.drawLine(start_x, y, end_x, y)
    
            painter.end()
    
    
    if __name__ == "__main__":
        app = QApplication(sys.argv)
        window = SyncedListTableWidget()
        window.show()
        sys.exit(app.exec_())



class ExampleWidget(QWidget):
    def __init__(self):
        super().__init__()   
        self.setWindowTitle("Synced List & Table with Overlay Lines")    
        self.resize(750, 500)        

        self.layout = QHBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0) # Remove layout margins for a seamless look
        
        # --- CONSTANTS FOR PIXEL-PERFECT ALIGNMENT ---
        ROW_HEIGHT = 30
        HEADER_HEIGHT = 35

        # ==========================================
        # 1. TABLE SETUP
        # ==========================================
        self.table = QTableWidget(100, 2, self)
        self.table.setHorizontalHeaderLabels(["Name", "Age"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # Force exact heights
        self.table.horizontalHeader().setFixedHeight(HEADER_HEIGHT)
        self.table.verticalHeader().setDefaultSectionSize(ROW_HEIGHT)
        
        # Hide the vertical row numbers to prevent a left-side offset gap
        self.table.verticalHeader().setVisible(False) 
        
        # Remove borders
        self.table.setFrameShape(QTableWidget.NoFrame) 


        # ==========================================
        # 2. GRIDLIST SETUP (with Fake Header)
        # ==========================================
        # Create a container with a fake header so it gets pushed down equal to the table
        self.list_container = QWidget(self)
        list_layout = QVBoxLayout(self.list_container)
        list_layout.setSpacing(0)
        list_layout.setContentsMargins(0, 0, 0, 0)

        # The fake header matches the Table's header height
        self.fake_header = QLabel(" Gridlist (Names)")
        self.fake_header.setFixedHeight(HEADER_HEIGHT)
        self.fake_header.setStyleSheet("background-color: #f4f4f4; border-bottom: 1px solid #d0d0d0;")

        self.gridlist = QListWidget(self)
        
        # Force List Item Height using a stylesheet
        self.gridlist.setStyleSheet(f"QListWidget::item {{ height: {ROW_HEIGHT}px; }}")
        self.gridlist.setFrameShape(QListWidget.NoFrame)
        
        # Hide the list's scrollbar (we will rely entirely on the table's scrollbar)
        self.gridlist.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Add both to the vertical container
        list_layout.addWidget(self.fake_header)
        list_layout.addWidget(self.gridlist)


        # ==========================================
        # 3. SYNC & POPULATE
        # ==========================================
        sb_list = self.gridlist.verticalScrollBar()
        sb_table = self.table.verticalScrollBar()
        sb_list.valueChanged.connect(sb_table.setValue)
        sb_table.valueChanged.connect(sb_list.setValue)        

        for i in range(100):
            name = f"User {i + 1}"
            age = str(20 + (i % 45))
            
            self.gridlist.addItem(name)
            self.table.setItem(i, 0, QTableWidgetItem(name))
            self.table.setItem(i, 1, QTableWidgetItem(age))

        # Add to main horizontal layout (Table on Left, List container on Right)
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.list_container)

    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExampleWidget()
    window.show()
    sys.exit(app.exec_())    



    
    
    
    
    
    
    
    