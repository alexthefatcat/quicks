# -*- coding: utf-8 -*-
"""Created on Mon Mar  9 00:08:08 2026@author: Alexm"""



import numpy as np
from quick_image import show_image, read_image


import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget, QScrollArea, QMenu, QAction
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QTimer, QRect







class QImageView(QWidget):
    def __init__(self, image_data):
        super().__init__()

        self.image_data = image_data  # keep reference for QImage

        # ---- Layout ----
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # ---- Scroll area ----
        self.scroll_area = self.QScrollArea(self)
        self.scroll_area.setWidgetResizable(False)  # important: don't stretch child
        self.scroll_area.setContentsMargins(0, 0, 0, 0)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.layout.addWidget(self.scroll_area)

        # ---- Label ----
        self.label = self.QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.scroll_area.setWidget(self.label)

        # ---- Load image ----
        self.update(image_data)

        # ---- Context menu ----
        self.context_menu = self.ContextMenu(self.label)
        
        #  Fix tiny image on startup
        QTimer.singleShot(0, lambda : self.resizeEvent(None))

    
            
    # -----------------------------
    #   IMAGE LOADING / UPDATE
    # -----------------------------

    # keep signature compatible with your old code
    def update(self, image_data=None, reset_widget_size=True, update_label=False):
        if isinstance(image_data, str):
            image_data = (255*read_image(image_data)).astype('uint8')
        if image_data is not None:
            self.image_data = image_data

        h, w, ch = self.image_data.shape
        bytes_per_line = ch * w

        qimage = QImage(self.image_data.tobytes(),w,h,bytes_per_line,QImage.Format_RGB888)

        self.pixmap = QPixmap.fromImage(qimage)

        if not update_label:
            self.label.setPixmap(self.pixmap)
            self.label.resize(self.pixmap.size())
        else:
            # keep current label size, just replace pixmap
            area_size = self.scroll_area.viewport().size()
            scaled = self.pixmap.scaled(
                area_size,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.label.setPixmap(scaled)

    # -----------------------------
    #   RESIZE HANDLING
    # -----------------------------
    def resizeEvent(self, event):
        if not hasattr(self, "pixmap") or self.pixmap.isNull():
            return

        area_size = self.scroll_area.viewport().size()

        scaled = self.pixmap.scaled(
            area_size,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        self.label.setPixmap(scaled)
        self.label.resize(scaled.size())


    # -----------------------------
    #   PIXMAP RECTANGLE
    # -----------------------------
    def displayed_pixmap_rect(self):
        """
        QRect where the pixmap is actually drawn inside the label.
        (Centered, with possible borders.)
        """
        pm = self.label.pixmap()
        if pm is None:
            return QRect()

        pm_w = pm.width()
        pm_h = pm.height()
        label_w = self.label.width()
        label_h = self.label.height()

        x = (label_w - pm_w) // 2
        y = (label_h - pm_h) // 2

        return QRect(x, y, pm_w, pm_h)

    # -----------------------------
    #   POSITION → IMAGE PIXEL
    # -----------------------------
    def position_to_pixel(self, x, y):
        """
        Widget coords (x, y) → image pixel (px, py), plus inside flag.
        """
        rect = self.displayed_pixmap_rect()
        if not rect.contains(x, y):
            return -1, -1, False

        img_h, img_w, _ = self.image_data.shape

        px = (x - rect.x()) * img_w / rect.width()
        py = (y - rect.y()) * img_h / rect.height()

        return int(px), int(py), True

    # -----------------------------
    #   IMAGE PIXEL → POSITION
    # -----------------------------
    def pixel_to_position(self, px, py):
        """
        Image pixel (px, py) → widget coords (x, y).
        """
        rect = self.displayed_pixmap_rect()
        img_h, img_w, _ = self.image_data.shape

        x = rect.x() + px * rect.width() / img_w
        y = rect.y() + py * rect.height() / img_h

        return int(x), int(y)

    # -----------------------------
    #   CUSTOM SUBCLASSES
    # -----------------------------
    class QScrollArea(QScrollArea):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.parent = parent

    class QLabel(QLabel):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.parent = parent

    # -----------------------------
    #   CONTEXT MENU
    # -----------------------------
    class ContextMenu:
        def __init__(self, label):
            self.label = label
            self.window = label.window()
            self.setcontextmenu(self.label)
    
        def setcontextmenu(self, label):
            label.setContextMenuPolicy(Qt.CustomContextMenu)
            label.customContextMenuRequested.connect(self.showContextMenu)
    
        def showContextMenu(self, pos):
            menu = QMenu(self.window)
    
            saveAction = QAction('Save Image', self.window)
            saveAction.triggered.connect(self.saveImage)
            menu.addAction(saveAction)
    
            copyAction = QAction('Copy Image', self.window)
            copyAction.triggered.connect(self.copyImage)
            menu.addAction(copyAction)
    
            # ⭐ NEW: Reset zoom to 1:1
            resetAction = QAction('Reset Zoom (1:1)', self.window)
            resetAction.triggered.connect(self.resetZoom)
            menu.addAction(resetAction)
    
            menu.exec_(self.label.mapToGlobal(pos))
    
        def saveImage(self):
            filePath, _ = QFileDialog.getSaveFileName(
                self.window, 'Save Image', '', 'Image Files (*.png *.jpg *.bmp)'
            )
            if filePath and self.label.pixmap() is not None:
                self.label.pixmap().save(filePath)
    
        def copyImage(self):
            pm = self.label.pixmap()
            if pm is not None:
                QApplication.clipboard().setPixmap(pm)
    
        def resetZoom(self):
            parent = self.label.parent
        
            # Restore original pixmap
            self.label.setPixmap(parent.pixmap)
        
            # Disable auto-resizing so scroll area shrinks to label
            parent.scroll_area.setWidgetResizable(False)
        
            # Resize label to raw image size
            self.label.resize(parent.pixmap.size())
        
            # Shrink the QImageView widget
            parent.adjustSize()
        
            #  Shrink the QMainWindow too
            parent.window().adjustSize()
        
            self.label.update()
        
            





class MainWindow(QMainWindow):
    def __init__(self, filepath):
        super().__init__()
        self.setWindowTitle("QuickImage Example line-234")
        self.central_widget = QImageView(filepath)
        self.setCentralWidget(self.central_widget)
 
        
 

 
    
if __name__ == '__main__':
    
    fp = r"C:\Users\Alexm\Pictures\sz_-ijiuji.png"
    image0 = (255*read_image(fp)).astype('uint8')
    image = image0[::2,::2,:3]      
    show_image(image0)
    show_image(image)        
    
    
    app = QApplication(sys.argv)
    window = MainWindow(fp)
    window.show()  
    sys.exit(app.exec_())















    
    
   
    
    
