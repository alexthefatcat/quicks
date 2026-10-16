# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 04:11:21 2026

@author: alexm
"""



'''

idea how to do a print debug
class print_debug

with print_debug('Title') as (data, flag):
    if flag:
        content = file.read()
        print(content)

'''


from PyQt5.QtWidgets import QSplitter, QTableWidget, QHBoxLayout, QScrollBar,  QTableWidgetItem, QListWidget, QListWidgetItem, QWidget, QFrame, QVBoxLayout
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtGui import  QPainterPath, QLinearGradient
from PyQt5.QtGui import QPixmap, QIcon, QColor, QPainter, QPen
from PyQt5.QtCore import QTimer

import math
from PyQt5.QtCore import QRectF, QPointF
from PyQt5.QtWidgets import QApplication

import pandas as pd
from pandas.api.types import is_string_dtype, is_numeric_dtype

from contextlib import contextmanager

from types import SimpleNamespace


@contextmanager
def block_signals(*widgets):
    """Temporarily block signals for one or more widgets."""
    for widget in widgets:
        widget.blockSignals(True)
    try:
        yield
    finally:
        for widget in widgets:
            widget.blockSignals(False)

def print_debug(*args,**kwargs):
    if DEBUG:
        args = list(args)+['#* print_debug']
        print(*args, **kwargs)





DEBUG = True



debug_tl = False # travel laptop
# fixes black line






class StarRating(QWidget):
    """
    High-fidelity vector star rating widget with smooth gradients and hover effects.
    """
    ratingChanged = pyqtSignal(int)

    def __init__(self, rating=0, max_stars=5, parent=None):
        super().__init__(parent)
        self._rating = rating
        self._max_stars = max_stars
        self._hover_rating = 0
        self.setMouseTracking(True)
        
        # --- Appearance Config ---
        # Active Star Colors (Golden Gradient)
        self.color_active_start = QColor(255, 215, 0) # Gold
        self.color_active_end = QColor(255, 165, 0)   # Orange
        self.color_outline_active = QColor(218, 165, 32) # Goldenrod

        # Inactive/Background Star Colors
        self.color_inactive_fill = QColor(240, 240, 240) # Very Light Gray
        self.color_outline_inactive = QColor(200, 200, 200) # Light Gray

        # Define the basic geometric path for a single star once
        self.star_path = self._create_star_path()

    def _create_star_path(self):
        """Calculates a perfect 5-pointed star geometry (normalized 0.0 to 1.0)."""
        path = QPainterPath()
        center = QPointF(0.5, 0.5)
        r_outer = 0.5
        r_inner = 0.2  # Controls how 'pointy' the star is
        
        points = []
        angle = -math.pi / 2  # Start pointing straight up
        
        for i in range(10):
            r = r_outer if i % 2 == 0 else r_inner
            points.append(QPointF(
                center.x() + r * math.cos(angle),
                center.y() + r * math.sin(angle)
            ))
            angle += math.pi / 5 # 36 degrees
            
        path.moveTo(points[0])
        for pt in points[1:]:
            path.lineTo(pt)
        path.closeSubpath()
        return path

    def minimumSizeHint(self):
        return QSize(24 * self._max_stars, 24)

    def sizeHint(self):
        return QSize(30 * self._max_stars, 30)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Clear background (ensure transparency in table cells)
        painter.fillRect(self.contentsRect(), Qt.transparent)

        # 1. Determine dimensions and spacing
        w = self.width()
        h = self.height()
        
        # Fixed size stars, centered within the available space
        star_size = min(h, w / self._max_stars) * 0.85 # 85% of cell height
        total_width = star_size * self._max_stars
        
        # Center horizontally if cell is wider
        start_x = (w - total_width) / 2
        
        # 2. Determine active rating level (hover takes precedence)
        effective_rating = self._hover_rating if self._hover_rating > 0 else self._rating

        # 3. Draw Stars
        for i in range(1, self._max_stars + 1):
            star_rect = QRectF(
                start_x + (i - 1) * star_size,
                (h - star_size) / 2, # Center vertically
                star_size,
                star_size
            )
            
            is_active = i <= effective_rating
            self._draw_single_star(painter, star_rect, is_active)

    def _draw_single_star(self, painter, rect, is_active):
        """Renders one vector star with gradients and outlines."""
        painter.save()
        
        # Move coordinate system to the star's rectangle and scale up the 0-1 path
        painter.translate(rect.x(), rect.y())
        painter.scale(rect.width(), rect.height())

        if is_active:
            # Golden Gradient Fill
            grad = QLinearGradient(0, 0, 0, 1) # Vertical gradient
            grad.setColorAt(0.0, self.color_active_start)
            grad.setColorAt(1.0, self.color_active_end)
            painter.setBrush(grad)
            
            # Sharp Outline
            painter.setPen(QPen(self.color_outline_active, 0.05, Qt.SolidLine))
        else:
            # Subtle Inactive Fill
            painter.setBrush(self.color_inactive_fill)
            # Subtle Outline
            painter.setPen(QPen(self.color_outline_inactive, 0.04, Qt.SolidLine))

        # Draw the predefined geometry path
        painter.drawPath(self.star_path)
        
        painter.restore()

    def mouseMoveEvent(self, event):
        """Tracks hover position to update preview rating."""
        # Recalculate start_x, star_size just like in paintEvent to map accurately
        w = self.width()
        h = self.height()
        star_size = min(h, w / self._max_stars) * 0.85
        total_width = star_size * self._max_stars
        start_x = (w - total_width) / 2
        
        # Check if mouse is within the star area
        if event.x() < start_x or event.x() > (start_x + total_width):
            new_hover = 0
        else:
            # Determine which star index is under the mouse
            relative_x = event.x() - start_x
            new_hover = int(relative_x / star_size) + 1
            
        new_hover = max(0, min(new_hover, self._max_stars))

        if self._hover_rating != new_hover:
            self._hover_rating = new_hover
            self.update()

    def leaveEvent(self, event):
        """Reset hover state when mouse leaves the widget."""
        if self._hover_rating != 0:
            self._hover_rating = 0
            self.update()

    def mousePressEvent(self, event):
        """Lock in the rating on click."""
        if event.button() == Qt.LeftButton:
            # We already know the hover rating is where the mouse is
            if self._hover_rating > 0:
                self.setRating(self._hover_rating)

    def rating(self): return self._rating

    def setRating(self, rating):
        if self._rating != rating:
            self._rating = rating
            self.ratingChanged.emit(self._rating)
            self.update()
    
    def __str__(self):
        return str(self.rating())






        
class LineOverlay(QWidget):
    """A transparent overlay widget that paints horizontal lines synchronized with scrolling."""
    def __init__(self, target_list_widget, parent=None, top_hidden=0):
        super().__init__(parent)
        self.parent = parent
        self.list_widget = target_list_widget
        self.top_hidden = top_hidden
        
        # Pass-through mouse clicks to underlying widgets
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.setAttribute(Qt.WA_NoSystemBackground, True)

        # Trigger a repaint automatically whenever the user scrolls
        self.list_widget.verticalScrollBar().valueChanged.connect(self.update)

    def paintEvent(self, event):
        painter = QPainter(self)
        
        # Define line style
        pen = QPen(QColor(0, 0, 0), 1)
        painter.setPen(pen)

        offset = 23
        row_height = 138
        
        # Get the current vertical scroll position in pixels
        scroll_y = self.list_widget.verticalScrollBar().value()
        
        scrollbar_width_debug = 24
        full_width = self.width()-scrollbar_width_debug

        for n in range(1, 100):  # Extend range to cover scrolled content
            # Subtract scroll_y so the line position shifts upward as you scroll down
            v = (n * row_height) + offset - scroll_y
            
            # Only draw lines currently visible inside the viewport frame
            if self.top_hidden <= v <= self.height():
                painter.drawLine(0, v, full_width, v)
        if False:
            painter.drawLine(0, self.top_hidden, full_width, self.top_hidden)
                    
        painter.end()

def chunk_by_size(items: list, chunk_size: int = 6) -> list[list]:
    return [items[i : i + chunk_size] for i in range(0, len(items), chunk_size)]


































class SyncedTableGallery0(QWidget):
    def __init__(self, parent=None, df=None, ListWidget=None, TableWidget=None, fixed_no_images=6):
        super().__init__(parent)
        
        self.options = SimpleNamespace()
        self.options.fixed_no_images = fixed_no_images
        self.options.show_lines = True
        self.options.widgets_sync_locked = True
        self.options._is_syncing = False
        
        self.df = df
        self.index__sorting_mask_default = pd.Series(True, index=self.df.index)
        self.index__sorting_mask = self.index__sorting_mask_default.copy()
        self.columns = list(df.columns)
        self.ratings_columns_index = [i for i,e in enumerate(self.columns) if 'Rating' in e]
        self.ListWidget = QListWidget if ListWidget is None else ListWidget
        self.TableWidget = QTableWidget if TableWidget is None else TableWidget        




    @property
    def df_view(self):
        mask = self.index__sorting_mask
        df = self.df
        df_view = df.loc[mask.index]    
        df_view = df_view[mask]
        return df_view

    def init_gridlist(self):
        self.gridlist = self.ListWidget()  
        self.gridlist.setViewMode(QListWidget.IconMode)
        self.gridlist.setIconSize(QSize(90, 90))
        self.gridlist.setResizeMode(QListWidget.Adjust)
        self.gridlist.setMovement(QListWidget.Static)
        self.gridlist.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.gridlist.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.gridlist.setStyleSheet(" QListWidget::item { border:none; padding-top: 18px}")
        self.gridlist.currentItemChanged.connect(self.selection_changed)
        
        # Add this where self.gridlist is initialized (e.g., in __init__)
        self.gridlist.setStyleSheet("""
            QListWidget::item:selected {
                color: #000000;             /* Keeps the text black when selected */
                background-color: #e0e0e0;  /* Light grey highlight (or set 'transparent') */
            }
            QListWidget::item:selected:has-focus {  color: #000000; }""")


    def init_table(self):
        self.table = self.TableWidget()
        self.table.verticalHeader().setDefaultSectionSize(self.LIST_ROW_HEIGHT)
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet(" QTableWidget { background-color: white; alternate-background-color: #FFF0F0;  padding-bottom: 2px; }")        
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table.horizontalHeader().setStyleSheet("QHeaderView::section {  background-color: rgb(240, 240, 240);  }")
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.table.horizontalHeader().setSectionsClickable(True)
        self.table.horizontalHeader().sectionClicked.connect(self.table_column_sort)
        self.table.itemSelectionChanged.connect(self.selection_changed)        
      

    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.addWidget(self.table)
        
        # Determine header height based on debug flag
        header_height = 36 if debug_tl else 23
        
        # Setup right container and layout
        self.right_container = QWidget()
        self.right_layout = QHBoxLayout(self.right_container)
        self.right_layout.setContentsMargins(0, header_height, 0, 0)
        
        self.scrollbar = QScrollBar()
        self.right_layout.addWidget(self.gridlist)
        self.right_layout.addWidget(self.scrollbar)
        
        self.splitter.addWidget(self.right_container)
        layout.addWidget(self.splitter)
        

    def table_column_sort(self, logical_index):    
        if not hasattr(self, 'table_column_sort_column'):
           self.table_column_sort_column = None
           
        if self.table_column_sort_column == logical_index:
            self.table_column_sort_ascending = not self.table_column_sort_ascending # Toggle direction
        else:
            self.table_column_sort_column = logical_index
            self.table_column_sort_ascending = True # Default to ascending
        self.apply_sort()

    def setup_sync_scrolling(self):
        print('setup_sync_scrolling')
        self.options._is_syncing = False  # Initialize re-entrancy guard flag
        self.copy_scrollbar_properties()
    
        table_vertical_scrollbar = self.table.verticalScrollBar()
        gridlist_vertical_scrollbar = self.gridlist.verticalScrollBar()
        main_scrollbar = self.scrollbar
    
        gridlist_vertical_scrollbar.valueChanged.connect(self.sync_scrollbars)
        table_vertical_scrollbar.valueChanged.connect(self.sync_scrollbars)
        main_scrollbar.valueChanged.connect(self.sync_scrollbars)
    
        # Optional: Keep main_scrollbar's range updated when table changes
        table_vertical_scrollbar.rangeChanged.connect(
            lambda min_val, max_val: main_scrollbar.setRange(min_val, max_val)
        )
    
    
    def sync_scrollbars(self):
        # Prevent infinite recursive signal loops while allowing internal Qt updates
        if self.options._is_syncing:
            return
    
        sender = self.sender()
        if not sender:
            return
    
        table_vertical_scrollbar = self.table.verticalScrollBar()
        gridlist_vertical_scrollbar = self.gridlist.verticalScrollBar()
        main_scrollbar = self.scrollbar 
    
        # 1. Calculate normalized scroll percentage (0.0 to 1.0)
        rng = sender.maximum() - sender.minimum()
        if rng <= 0:
            return
        pct = (sender.value() - sender.minimum()) / rng
    
        # 2. Helper to set target scrollbar value from percentage
        def set_by_pct(sb, ratio):
            sb_range = sb.maximum() - sb.minimum()
            target_val = int(sb.minimum() + ratio * sb_range)
            if sb.value() != target_val:
                sb.setValue(target_val)
    
        # 3. Synchronize using re-entrancy flag
        self.options._is_syncing = True
        try:
            if sender != main_scrollbar:
                set_by_pct(main_scrollbar, pct)
                
            if sender != table_vertical_scrollbar:
                set_by_pct(table_vertical_scrollbar, pct)
                
            if sender != gridlist_vertical_scrollbar:
                set_by_pct(gridlist_vertical_scrollbar, pct)
        finally:
            self.options._is_syncing = False

    def copy_scrollbar_properties(self):
        source = self.table.verticalScrollBar()
        target = self.scrollbar
        
        # Copy properties
        target.setOrientation(source.orientation())
        target.setRange(source.minimum(), source.maximum())
        target.setPageStep(source.pageStep())
        target.setSingleStep(source.singleStep())
        target.setValue(source.value())
        print_debug("Source")
        print_debug(source.minimum(), source.maximum(), source.pageStep())
        print_debug("Target")
        print_debug(target.minimum(), target.maximum(), target.pageStep())        

    def __round_up(self, x, n):
        return ((x + n - 1) // n) * n    
    
    def resizeEvent(self, event):
        super().resizeEvent(event)        
        self.copy_scrollbar_properties()

    def showEvent(self, event):
        super().showEvent(event)
        self.copy_scrollbar_properties()    
    
    def selection_changed(self, row_idx=None):
        if self.options._is_syncing:
            return
        self.options._is_syncing = True
        try:
            if row_idx is False:
                if self.gridlist.currentRow() != -1:
                    self.gridlist.clearSelection()
                if self.table.currentRow() != -1:
                    self.table.clearSelection()   
                self.changed_item(row_idx)
                return
        
            # 1. Normalize row_idx if Qt signal passed an item object or unexpected type
            if hasattr(row_idx, "row"):
                row_idx = row_idx.row()
            if not isinstance(row_idx, int):
                row_idx = None
    
            if row_idx is None and self.sender() and hasattr(self.sender(), "currentRow"):
                row_idx = self.sender().currentRow()
                    
            # 3. Guard against missing or out-of-bounds row index
            if row_idx is None or row_idx < 0:
                return
        
            round_up = lambda n, v=6: -(-n // v) * v
            round_up_gridlist_count = round_up(self.gridlist.count())
        
            if self.table.rowCount() != round_up_gridlist_count:
                return
        
            if not (0 <= row_idx < self.table.rowCount()):
                return
    
        # 4. Perform synchronization

            if self.gridlist.currentRow() != row_idx:
                grid_item = self.gridlist.item(row_idx)
                if grid_item:
                    self.gridlist.setCurrentItem(grid_item)
                    self.gridlist.scrollToItem(grid_item)
    
            if self.table.currentRow() != row_idx:
                self.table.selectRow(row_idx)
                for col in range(self.table.columnCount()):
                    table_item = self.table.item(row_idx, col)
                    if table_item:
                        self.table.scrollToItem(table_item)
                        break      
        finally:
            self.options._is_syncing = False
    
        self.changed_item(row_idx)    

    def create_default_icon(self):
        pixmap = QPixmap(90, 90)
        pixmap.fill(Qt.darkGray)
        self.default_icon = QIcon(pixmap)
        
    def apply_sort(self):
        print('apply sort')
        """Sorts self.filtered_df directly based on selected column index."""
        if self.table_column_sort_column == -1 or self.df_view.empty:
            return
        
        df = self.df
        col_name = df.columns[self.table_column_sort_column] 

        ascending = self.table_column_sort_ascending
        
        if is_string_dtype(df[col_name]):
            print_debug(f'   Sort by {col_name} which IS sting')
            sort_series = df[col_name].str.lower()        
            
            if False:
                if self.sort_col == 1:
                    sort_series = pd.to_datetime(df[col_name], format="%d/%m/%Y %H:%M")
        
                # if 'size' in col_name.lower():
                    print('Sort by size')
                    sort_series = df[col_name].str.replace(" KB", "", regex=False).astype(int)
    
            print(f'Filtering Column, sort_func_dict {list(self.sort_func_dict.keys())}')
            if col_name in self.sort_func_dict:
                func = self.sort_func_dict[col_name]
                sort_series = self.df[col_name].apply(func)
                
        if is_numeric_dtype(df[col_name]): 
            print_debug(f'   Sort by {col_name} which is NOT sting')               
            sort_series = -df[col_name].fillna(0)               
                
        df = self.df[[col_name]].sort_values(by=col_name, key= lambda _: sort_series, ascending=ascending )
        self.index__sorting_mask = self.index__sorting_mask.loc[df.index]
        self.refresh_view()

    def get_image_from_row(self, row_data):
        return self.default_icon

    def create_blank_table_row(self, row):
        self.table.setVerticalHeaderItem(row, QTableWidgetItem(""))
        self.table.setRowHeight(row, self.LIST_ROW_HEIGHT)
        ncols = self.table.columnCount()
        for col in range(ncols):
            buffer_item = QTableWidgetItem("")
            buffer_item.setFlags(Qt.NoItemFlags) 
            buffer_item.setBackground(self.table.palette().base())
            self.table.setItem(row, col, buffer_item)
        self.table.setSpan(row, 0, 1, ncols)    

#%% Refesh View Related Methods
    def changed_item(self, row_idx):
        #print(row_idx)
        pass    
    def modify_grid_item(self, item):
        return item
    def refresh_view_set_table_item(self, irow, icol, val):
        if icol in self.ratings_columns_index:
            star_widget = StarRating(rating=val)
            star_widget.ratingChanged.connect( lambda new_rating, r=irow, c=icol: self.on_rating_changed(c, r, new_rating)  )
            container = QFrame()
            container_layout = QVBoxLayout(container)
            container_layout.addWidget(star_widget)
            container_layout.setContentsMargins(0, 0, 0, 0) # No margins
            container_layout.setAlignment(Qt.AlignCenter) # Center horizontally/vertically
            self.table.setCellWidget(irow, icol, container)
        else:
            self.table.setItem(irow, icol, QTableWidgetItem(str(val)))     
    def refresh_view_set_gridlist_item(self, item_name, image, counter):
        item = QListWidgetItem(image, item_name)
        item.setTextAlignment(Qt.AlignCenter)
        item.setData(Qt.UserRole, {"id": counter})             
        item = self.modify_grid_item(item)                
        self.gridlist.addItem(item)        
    def refresh_view_add_items(self):
        df_view = self.df_view
        
        if df_view.empty:
            return

        total_items = len(df_view)
        total_items_incl_buffer = self.__round_up(total_items, 6)

        self.table.setColumnCount(len(self.df_view.columns))
        self.table.setHorizontalHeaderLabels([str(c) for c in df_view.columns])
        self.table.setRowCount(total_items_incl_buffer)
        
        chunks = chunk_by_size(list(enumerate(df_view.iterrows())))
        counter = -1
        for ichunk, chunk in enumerate(chunks):
            chunk_items = []
            for irow, (_, row_data) in chunk:
                self.table.setRowHeight(irow, self.LIST_ROW_HEIGHT)
                item_name = f"Item {irow + 1}"  # Fallback name
                 
                for icol, (_, val) in enumerate(row_data.items()):

                    self.refresh_view_set_table_item(irow, icol, val)
                        
                    if icol == 0:
                        item_name = str(val)

                image = self.get_image_from_row(row_data)
                chunk_items.append([item_name, image])         
                
            for item_name, image in chunk_items:
                counter +=1
                self.refresh_view_set_gridlist_item(item_name, image, counter)
                
        print(f'    Refesh View, Total Rows = {total_items}<<')                      
        for row in range(total_items, total_items_incl_buffer):
            self.create_blank_table_row(row)
            
    def refresh_view(self):
        self.selection_changed(False)                     
        self.table.clear()
        self.table.clearSpans()
        self.gridlist.clear()

        self.refresh_view_add_items()
        QApplication.processEvents()
        self.copy_scrollbar_properties()

        self.gridlist.verticalScrollBar().setValue(0)
        self.table.verticalScrollBar().setValue(0)
        self.selection_changed(0)
        


        


 
                    
    
    
    




class SyncedTableGallery(SyncedTableGallery0):
    def __init__(self, parent=None, df=None, ListWidget=None, TableWidget=None, fixed_no_images=6):
        super().__init__(parent, df, ListWidget, TableWidget, fixed_no_images)
        print('  >>SyncedTableGalleryWidget2<<\n\t\t-removed stars')
        self.LIST_ROW_HEIGHT = 22
        if debug_tl:
            self.LIST_ROW_HEIGHT = 35
        
        self.init_table()
        self.init_gridlist()
        self.init_ui()
        
        self.splitter
        
        self.create_default_icon()
        self.setup_sync_scrolling()
        
        self.reset_grid_item_sizes()
        self.sort_func_dict = {}


        QTimer.singleShot(0, self.__init__post)

            
    def __init__post(self):#not working
        self.refresh_view()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    # def refresh_view(self):
    #     super().refresh_view() 
    #     top_hidden=37        
    #     self.line_overlay = LineOverlay(target_list_widget=self.gridlist, parent=self, top_hidden=top_hidden)
    #     print('line overlay')

    # def paintEvent(self, event):
    #     self.step = 2
    #     # 1. Let QListWidget draw all standard items, text, and selection highlights
    #     super().paintEvent(event)

    #     count = self.gridlist.count()
    #     if count < self.step:
    #         return

    #     # 2. Paint lines directly on top of the rendered viewport
    #     painter = QPainter(self.gridlist.viewport())
    #     painter.setPen(QPen(QColor(0, 0, 0), 2))

    #     vw = self.gridlist.viewport().width()
    #     vh = self.gridlist.viewport().height()

    #     for idx in range(self.step - 1, count, self.step):
    #         item = self.gridlist.item(idx)
    #         if item:
    #             rect = self.gridlist.visualItemRect(item)
    #             y = rect.bottom()
    #             if 0 <= y <= vh:
    #                 painter.drawLine(0, y, vw, y)
    #                 print(0, y, vw, y)
    #     painter.end()








    #     top_hidden = 0

    #     

    #     def _on_grid_resize(event):
    #         # Call original resize event
    #         super(type(self.gridlist), self.gridlist).resizeEvent(event)
    #         # Stretch overlay over the entire grid area
    #         self.line_overlay.setGeometry(self.rect())    
        

    #     # Keep overlay dimensions synced with grid_list viewport
    #     self.gridlist.resizeEvent = _on_grid_resize
    
 

    def reset_grid_item_sizes(self):
        if not hasattr(self, 'gridlist_fixed'):
            grid_item_height = (self.LIST_ROW_HEIGHT+1)*6
            grid_row_width = (grid_item_height*6 +10)
            print_debug(self.LIST_ROW_HEIGHT, grid_item_height, grid_row_width, 'gridlist_fixed')
            
            self.gridlist.setIconSize(QSize(100, 100))
            self.gridlist.setGridSize(QSize(grid_item_height, grid_item_height)) 
            self.gridlist.setSpacing(0)  
            
            self.gridlist.setFixedWidth(grid_row_width)
            self.gridlist.setResizeMode(QListWidget.Fixed) 

            self.splitter.setStretchFactor(0, 1) 
            self.splitter.setStretchFactor(1, 0)                             
                                        
            if False:
                table_width, grid_width = self.splitter.sizes()            
                self.right_container.setMinimumWidth(grid_row_width+10)        
    
    
                print_debug(table_width,grid_width)
                self.splitter.setSizes([600, grid_row_width])
                print_debug(grid_row_width,'<<')

            # current_height = self.gridlist.height()
            # current_width = self.gridlist.width()
            # self.gridlist.resize(grid_row_width, current_height)
            
            # self.gridlist.resize(current_width, current_height)  
            self.gridlist_fixed = True          





    
    








# class SyncedTableGallery(SyncedTableGallery0):
#     def __init__(self, parent=None, df=None, ListWidget=None, TableWidget=None, fixed_no_images=6):
#         super().__init__(parent, df, ListWidget, TableWidget, fixed_no_images)
#         print('  >>SyncedTableGalleryWidget2<<\n\t\t-removed stars')
#         self.LIST_ROW_HEIGHT = 22
#         if debug_tl:
#             self.LIST_ROW_HEIGHT = 35
        
#         self.init_table()
#         self.init_gridlist()
#         self.init_ui()
        
#         self.create_default_icon()
#         self.setup_sync_scrolling()
        
#         self.reset_grid_item_sizes()
#         self.sort_func_dict = {}

#         if True:
#             QTimer.singleShot(0, self.__init__post)
#         else:
#             self.refresh_view()
    
#             # Create overlay attached to grid_list
#             top_hidden = 0
#             if debug_tl:
#                 top_hidden=37
#             self.line_overlay = LineOverlay(target_list_widget=self.gridlist, parent=self, top_hidden=top_hidden)
    
#             def _on_grid_resize(event):
#                 # Call original resize event
#                 super(type(self.gridlist), self.gridlist).resizeEvent(event)
#                 # Stretch overlay over the entire grid area
#                 self.line_overlay.setGeometry(self.rect())    
            
    
#             # Keep overlay dimensions synced with grid_list viewport
#             self.gridlist.resizeEvent = _on_grid_resize
            
#     def __init__post(self):#not working
#         self.refresh_view()

#         top_hidden = 0
#         if debug_tl:
#             top_hidden=37
#         self.line_overlay = LineOverlay(target_list_widget=self.gridlist, parent=self, top_hidden=top_hidden)

#         def _on_grid_resize(event):
#             # Call original resize event
#             super(type(self.gridlist), self.gridlist).resizeEvent(event)
#             # Stretch overlay over the entire grid area
#             self.line_overlay.setGeometry(self.rect())    
        

#         # Keep overlay dimensions synced with grid_list viewport
#         self.gridlist.resizeEvent = _on_grid_resize
    
 

#     def reset_grid_item_sizes(self):
#         if not hasattr(self, 'gridlist_fixed'):
#             grid_item_height = (self.LIST_ROW_HEIGHT+1)*6
#             grid_row_width = (grid_item_height*6 +10)
#             print_debug(self.LIST_ROW_HEIGHT, grid_item_height, grid_row_width, 'gridlist_fixed')
            
#             self.gridlist.setIconSize(QSize(100, 100))
#             self.gridlist.setGridSize(QSize(grid_item_height, grid_item_height)) 
#             self.gridlist.setSpacing(0)  
            
#             self.gridlist.setFixedWidth(grid_row_width)
#             self.gridlist.setResizeMode(QListWidget.Fixed) 

#             self.splitter.setStretchFactor(0, 1) 
#             self.splitter.setStretchFactor(1, 0)                             
                                        
#             if False:
#                 table_width, grid_width = self.splitter.sizes()            
#                 self.right_container.setMinimumWidth(grid_row_width+10)        
    
    
#                 print_debug(table_width,grid_width)
#                 self.splitter.setSizes([600, grid_row_width])
#                 print_debug(grid_row_width,'<<')

#             # current_height = self.gridlist.height()
#             # current_width = self.gridlist.width()
#             # self.gridlist.resize(grid_row_width, current_height)
            
#             # self.gridlist.resize(current_width, current_height)  
#             self.gridlist_fixed = True          













# import sys
# from PyQt5.QtCore import Qt
# from PyQt5.QtGui import QPainter, QPen, QColor
# from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QWidget, QVBoxLayout


# class LineListWidget(QListWidget):
#     """A QListWidget subclass that natively paints horizontal divider lines every N rows."""

#     def __init__(self, parent=None, step=6):
#         super().__init__(parent)
#         self.step = step

#     def paintEvent(self, event):
#         # 1. Let QListWidget draw all standard items, text, and selection highlights
#         super().paintEvent(event)

#         count = self.count()
#         if count < self.step:
#             return

#         # 2. Paint lines directly on top of the rendered viewport
#         painter = QPainter(self.viewport())
#         painter.setPen(QPen(QColor(0, 0, 0), 2))

#         vw = self.viewport().width()
#         vh = self.viewport().height()

#         for idx in range(self.step - 1, count, self.step):
#             item = self.item(idx)
#             if item:
#                 rect = self.visualItemRect(item)
#                 y = rect.bottom()
#                 if 0 <= y <= vh:
#                     painter.drawLine(0, y, vw, y)
#         painter.end()


# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.resize(400, 600)
#         central_widget = QWidget(self)
#         self.setCentralWidget(central_widget)
#         layout = QVBoxLayout(central_widget)
#         self.list_widget = LineListWidget(step=6)
#         layout.addWidget(self.list_widget)
#         for i in range(1, 101):
#             self.list_widget.addItem(f"Row Item {i}")


# if __name__ == "__main__":
#     app = QApplication.instance() or QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec_())








# from PyQt5.QtCore import Qt, QPoint
# from PyQt5.QtGui import QPainter, QPen, QColor
# from PyQt5.QtWidgets import QWidget, QListWidget, QVBoxLayout


# class TransparentOverlay(QWidget):
#     """Pass-through overlay that delegates painting to its parent."""
#     def __init__(self, parent):
#         super().__init__(parent)
#         self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
#         self.setAttribute(Qt.WA_TranslucentBackground, True)

#     def paintEvent(self, event):
#         # Forward painting directly to the parent method
#         self.parent().draw_gridlist_overlay(self)


# class ParentContainerWidget(QWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.step = 2

#         layout = QVBoxLayout(self)
#         self.gridlist = QListWidget(self)
#         layout.addWidget(self.gridlist)

#         # 1. Create overlay attached to parent
#         self.overlay = TransparentOverlay(self)

#         # 2. Trigger redraw when user scrolls
#         self.gridlist.verticalScrollBar().valueChanged.connect(self.overlay.update)





#     def resizeEvent(self, event):
#         """Keep the overlay positioned directly over gridlist."""
#         super().resizeEvent(event)
#         self.overlay.setGeometry(self.gridlist.geometry())
#         self.overlay.raise_()

#     def draw_gridlist_overlay(self, overlay_target):
#         """All paint logic lives inside the PARENT container here."""
#         count = self.gridlist.count()
#         if count < self.step:
#             return

#         viewport = self.gridlist.viewport()
#         vh = viewport.height()

#         # Target painter to the overlay widget (stacked over gridlist)
#         painter = QPainter(overlay_target)
#         painter.setPen(QPen(QColor(0, 0, 0), 2))

#         # Map X-bounds from list viewport to overlay coordinates
#         start_x = viewport.mapTo(overlay_target, QPoint(0, 0)).x()
#         end_x = start_x + viewport.width()

#         for idx in range(self.step - 1, count, self.step):
#             item = self.gridlist.item(idx)
#             if item:
#                 rect = self.gridlist.visualItemRect(item)
                
#                 # Map item bottom Y position from viewport to overlay coordinates
#                 y = viewport.mapTo(overlay_target, QPoint(0, rect.bottom())).y()

#                 # Only draw if visible inside viewport bounds
#                 if 0 <= rect.bottom() <= vh:
#                     painter.drawLine(start_x, y, end_x, y)

#         painter.end()



# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.resize(400, 600)
#         central_widget = QWidget(self)
        
        
#         self.setCentralWidget(central_widget)
#         layout = QVBoxLayout(central_widget)
#         self.list_widget = LineListWidget(step=6)
#         layout.addWidget(self.list_widget)
#         for i in range(1, 101):
#             self.list_widget.addItem(f"Row Item {i}")


# if __name__ == "__main__":
#     app = QApplication.instance() or QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec_())



# from PyQt5.QtWidgets import QSplitter, QTableWidget, QHBoxLayout, QScrollBar,  QTableWidgetItem, QListWidget, QListWidgetItem, QWidget, QFrame, QVBoxLayout





































