# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 04:00:00 2026

@author: Alexm







1) searcher +box size
2) sorter click on columns and sort properly
3) scrolling down
4) add text in cell and update
5) sycronize clicking on rows highlights image
6) clean up code
7) make sure items are the same size and dont change aspect ratio based on the image
8) stop tool when stop hovering over image
9) bar with favorite actress to search




2) Automatically rezie row size if the number of columns changes
3) Chagne Search Box size, and advanced searches, time:32:21

6) if clicked on row or element of row corrosnding image is hihglighted
7) can change an elements value to actress or tags
8) stars
9) link everything togetehr

ranker
playelists



clean code up
search implement again















"""

import os, platform, subprocess
import pandas as pd
import sys, math
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QSplitter, QTableWidget, 
                             QTableWidgetItem, QListWidget, QListWidgetItem, QFrame, QLabel,
                             QAbstractItemView, QWidget, QVBoxLayout, QLineEdit)
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QPixmap, QIcon, QColor

def create_dummy_table(nrows=1001):
    fileinfos = []
    for i in range(nrows):
        extra = ('Sarah','Bob','Kate','Tom','Brian')[i%5]
        file_name = f"Image_File_{i:04}_{extra}.jpg"
        size = 100 + ((123*(i%5)) +(5*(i%11)))
        day = 1+ (i%23)
        month =  4+ ((i//100)%5)
        row = [file_name, f"{day:02}/{month:02}/2026 02:44", "JPG File", f"{size} KB"]  
        fileinfos.append(row)
    return fileinfos

from quick_example import fileinfo_df 



from quick_pandas import update_database

df_database =  update_database('pyvideo_film_info.csv')


dummy_table = create_dummy_table()
dummy_df = pd.DataFrame(columns=["Name", "Date Modified", "Type", "Size"], data = dummy_table)
dummy_df['Ducks'] = 'Quack'


dummy_df = df_database



USE_DATAFRAME = True


                 












class ResponsiveGridList(QListWidget):

    def __init__(self, default_row_height=None, parent_self=None,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent_self = parent_self
        self.GRID_INFO = self.parent_self.GRID_INFO
        self._current_cols = -1
        self.default_row_height = default_row_height
        self.setResizeMode(QListWidget.Fixed)
        self.skip_resize = False
        
        temp = self.GRID_INFO.CURRENT_NITEMS
        self.values = []
        for n in range(20):
            self.GRID_INFO.recalculate(n)
            w = self.GRID_INFO.WIDGET_HEIGHT_DEFAULT  
            self.values.append([n, w])
        self.GRID_INFO.recalculate(temp)         
            

    def resizeEvent(self, event):
        super().resizeEvent(event)
        current_width = event.size().width()
        cell_width = self.gridSize().width()
        cols, rows, total_items = self.get_grid_row_count()
        # if cols==5:
        #     self.parent_self.resize_gird_item(nwidth=5, widget_width=None)
        #     self.setGridSize(QSize(5,))
        
        if False:
            self.parent_self.resize_gird_item(nwidth=5, widget_width=None)
            
            # Calculate cell width for 5 columns based on available space
            left, top, right, bottom = self.getContentsMargins()
            available_width = self.viewport().width() - left - right
            cell_width = available_width // 5
            
            # Use existing height or set a fixed height (e.g., 120px)
            cell_height = self.gridSize().height() if self.gridSize().height() > 0 else 120
            
            self.setGridSize(QSize(cell_width, cell_height))    
                
        print(current_width)
        if not self.skip_resize:     
            for i1,v1 in self.values:
                if v1>current_width:
                    break
                v0 = v1
            i0 = i1-1
                
            current_nitems = self.GRID_INFO.CURRENT_NITEMS    
            print((i0,v0), (i1,v1), current_width, current_nitems)            
            if current_nitems != i0: 
                self.GRID_INFO.recalculate(i0)
                self.reset_sizes()

                self.skip_resize = True
                self.setResizeMode(QListWidget.Adjust)
                self.resize(v0+5, self.height())
                self.setResizeMode(QListWidget.Fixed)
                #self.resize(current_width, self.height())
                self.skip_resize = False
                print('new number of icons on a row',self.GRID_INFO.CURRENT_NITEMS  )
                self.parent_self.refresh_ui()



        
        return
        
        
        
        

        est_nwidgets = self.GRID_INFO.calculate_n_items_from_width(current_width)
        
        if self.GRID_INFO.CURRENT_NITEMS != est_nwidgets:
            print(self.values)
            print('Resize', est_nwidgets[0],)
            
            print(f'*Change_Number_of_Items_on_Row: {est_nwidgets[0]=}, {self.GRID_INFO.CURRENT_NITEMS=}')
            

            self.GRID_INFO.recalculate(est_nwidgets[0])
            self.reset_sizes()
        

        print(current_width, est_nwidgets,self.GRID_INFO.WIDGET_HEIGHT_MIN)

        
        print(f'{cols=}, {rows=}, {total_items=}')


        # Use a 0ms timer to let the items visually snap into their new rows first
        QTimer.singleShot(0, self.check_columns)












    def check_columns(self):
        if self.count() == 0:
            return
            
        # Find the vertical position of the first image
        first_y = self.visualItemRect(self.item(0)).y()
        cols = self.count()
        
        # Count how many items are on that exact same horizontal line
        for i in range(1, self.count()):
            if self.visualItemRect(self.item(i)).y() > first_y:
                cols = i
                break
        
        
        #self.parent_self.calucate_number_of_items(widget_width)
        
        if False:
            # If the number changed, emit our custom signal
            if cols != self._current_cols and cols > 0:
                print(f'Columnes changes from {self._current_cols} to {cols}')            
                self._current_cols = cols
        
    
                grid_height = self.gridSize().height()
                spacing = self.spacing()
                row_pixel_height = grid_height + (2 * spacing)
                actual_row_height = self.visualRect(self.model().index(0, 0)).height()
                print(f'{row_pixel_height=}; {actual_row_height=}')
                #row_pixel_height=240; actual_row_height=159
        
                grid_row_height = self.gridSize().height()
                actual_item_height = self.visualRect(self.model().index(0, 0)).height()
                
                print(f'{grid_row_height=}; {actual_item_height=}')
                grid_row_height = self.gridSize().height()
                actual_row_height = self.visualRect(self.model().index(0, 0)).height()
                
                print(f'Columns changed to {cols} | {grid_row_height=}; {actual_row_height=}')

        

    
    def get_grid_row_count(self):
        total_items = self.count()
        if total_items == 0:
            return 0, 0, 0
    
        # 1. gridSize().width() ALREADY includes spacing, do not add self.spacing()
        cell_width = self.gridSize().width()
        
        # Fallback if gridSize wasn't set on the list widget
        if cell_width <= 0:
            cell_width = self.visualItemRect(self.item(0)).width() + self.spacing()
    
        # 2. Unpack the tuple: (left, top, right, bottom)
        left, top, right, bottom = self.getContentsMargins()
        usable_width = self.viewport().width() - left - right
    
        # 3. Calculate columns and rows
        cols = max(1, usable_width // cell_width)
        rows = math.ceil(total_items / cols)
    
        return cols, rows, total_items


    def reset_sizes(self):
        self.setIconSize(QSize(self.GRID_INFO.ICON_SIZE, self.GRID_INFO.ICON_SIZE))
        self.setGridSize(QSize(self.GRID_INFO.ITEM_WIDTH, self.GRID_INFO.ITEM_HEIGHT)) 
        self.setSpacing(self.GRID_INFO.SPACING)     
        #self.setMinimumWidth(self.GRID_INFO.WIDGET_HEIGHT_MIN)



ListWidget = QListWidget
ListWidget = ResponsiveGridList



            


class GridItemProperties:
    def __init__(self, get__table_row_height, nrows=10):
        self.__get__table_row_height = get__table_row_height
        self.FONT_SIZE = 14
        self.grid_spacing = 30
        self.SPACING = self.grid_spacing
        self.recalculate(nrows)
    
    @property
    def table_row_height(self):
        return self.__get__table_row_height()
        
        
    def calculate_n_items_from_width(self, grid_width):
        import math
        """
        Inverts the grid sizing logic to calculate how many items (columns)
        fit into a given grid_width.
        """
        # Quadratic formula coefficients: a*N^2 + b*N + c = 0
        FONT_SIZE = self.FONT_SIZE
        list_row_height = self.table_row_height
        
        a = list_row_height
        b = -FONT_SIZE
        c = -grid_width
    
        # Quadratic formula solution: (-b + sqrt(b^2 - 4ac)) / (2a)
        discriminant = (b ** 2) - (4 * a * c)
        
        if discriminant < 0:
            return 0 # Invalid width or dimensions
    
        n_items_exact = (-b + math.sqrt(discriminant)) / (2 * a)
        n_items = math.floor(n_items_exact)
        return max(1, n_items), n_items_exact # Ensure at least 1 item is returned
            

    def recalculate(self, nwidth=10):
        self.CURRENT_NITEMS = nwidth
        self.ITEM_HEIGHT = self.table_row_height*self.CURRENT_NITEMS 
        self.ITEM_HEIGHT = self.ITEM_HEIGHT +{5:6,6:6,10:9}.get(self.CURRENT_NITEMS, 9)
        
        self.ITEM_WIDTH = self.ITEM_HEIGHT -self.FONT_SIZE
        
        self.ICON_SIZE = self.ITEM_WIDTH -self.SPACING
        self.WIDGET_HEIGHT_DEFAULT = self.ITEM_WIDTH*self.CURRENT_NITEMS
        self.WIDGET_HEIGHT_MIN = (self.ITEM_WIDTH*5  )+1# I dont know why 1 is needed      
        #print(f'\n\t{self.GRID_ITEM_HEIGHT=}\n\t{self.GRID_ITEM_WIDTH=}\n\t{self.icon_size=}\n\t{self.GRID_SPACING=}\n\t{font_size=}\n\t{self.GRID_CURRENT_NITEMS=}\n\t')



# turn off tool tips when not directly hovering over image
# class CustomListWidget(QListWidget):
#     def __init__(self, parent=None, *args, **kwargs):
#         super().__init__(parent, *args, **kwargs)
#         self.setMouseTracking(True)  # Required to track movement without clicking
#         self.itemEntered.connect(self.handle_item_entered)

#     def handle_item_entered(self, item: QListWidgetItem):
#         # Find where the icon sits inside the item row
#         index = self.indexFromItem(item)
#         rect = self.visualRect(index)
#         icon_size = self.iconSize()

#         # Get mouse position relative to the item
#         mouse_pos = self.mapFromGlobal(self.cursor().pos())
        
#         # Check if cursor is over the icon area (left side of item)
#         icon_rect = rect.adjusted(0, 0, icon_size.width() - rect.width(), 0)

#         if icon_rect.contains(mouse_pos):
#             image_fp = item.data(Qt.UserRole)  # Retrieve image path stored on item
#             tooltip_html = f'<img src="{image_fp}" style="max-width: 400px; max-height: 400px;">'
#             QToolTip.showText(self.cursor().pos(), tooltip_html, self)
#         else:
#             QToolTip.hideText()

#     super().__init__(parent, *args, **kwargs)

# TypeError: QListWidget(parent: QWidget = None): argument 1 has unexpected type 'QIcon'









class PhotoManager(QMainWindow):
    def __init__(self, df):
        super().__init__()
        self.setWindowTitle("Synchronized Image Gallery")
        self.df = df
        self.columns = list(self.df.columns)

        self.LIST_ROW_HEIGHT = 22 
        self.GRID_INFO = GridItemProperties(lambda : self.LIST_ROW_HEIGHT)
        
        
    
        
        # State variables for sorting and filtering
        self.all_data = create_dummy_table(21)
        self.filtered_data = self.all_data.copy()
        self.filtered_df = self.df.copy()
        
        
        
        self.sort_col = -1
        self.sort_asc = True
        
        # Create default icon once for performance

        
        pixmap = QPixmap(self.GRID_INFO.ICON_SIZE, self.GRID_INFO.ICON_SIZE)
        pixmap.fill(Qt.darkGray)
        self.default_icon = QIcon(pixmap)

        splitter = QSplitter(Qt.Horizontal)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(5, 5, 5, 5)

        
        # 1. Left Pane: Search Bar + Table Layout
        self.left_container = QWidget()
        self.left_layout = QVBoxLayout(self.left_container)
        self.left_layout.setContentsMargins(0, 0, 0, 0)
        
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search by name...")
        self.search_bar.textChanged.connect(self.apply_filter)
        main_layout.addWidget(self.search_bar)


        self.table = QTableWidget()
        self.table.setColumnCount(len(self.columns))
        self.table.setHorizontalHeaderLabels(self.columns)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setVerticalScrollMode(QAbstractItemView.ScrollPerItem)
        self.table.doubleClicked.connect(self.on_cell_clicked)

        # Enable sorting triggers
        self.table.horizontalHeader().setSectionsClickable(True)
        self.table.horizontalHeader().sectionClicked.connect(self.on_header_clicked)
        self.left_layout.addWidget(self.table)
        
        splitter.addWidget(self.left_container)
        
        # 2. Right Pane: Spacer + Grid List
        self.right_container = QWidget()
        self.right_layout = QVBoxLayout(self.right_container)
        self.right_layout.setContentsMargins(0, 0, 0, 0)
        self.right_layout.setSpacing(0)
        
        self.header_spacer = QWidget()
        self.header_spacer.setFixedHeight(0) 
        self.right_layout.addWidget(self.header_spacer)



        
        self.grid_list = ListWidget(default_row_height=self.LIST_ROW_HEIGHT,parent_self=self )
     
        self.grid_list.setViewMode(QListWidget.IconMode)
        #self.grid_list.setResizeMode(QListWidget.Adjust)
        self.grid_list.setMovement(QListWidget.Static)
        self.grid_list.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.grid_list.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.grid_list.reset_sizes()
        self.grid_list.setFlow(QListWidget.LeftToRight)
        self.grid_list.setWrapping(True)
        self.grid_list.itemDoubleClicked.connect(self.on_item_double_clicked)

        

        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.ExtendedSelection)
        if False:
            print('---> 427')
            self.table.itemSelectionChanged.connect(self.sync_selection_from_table)
            self.grid_list.itemSelectionChanged.connect(self.sync_selection_from_grid)    


        self.grid_list.setStyleSheet("""QListWidget { border: none; }
                                        QListWidget::item { border-top: 1px solid lightgray;padding-top: 18px;}""")  
                                        
                       
                                        
  
        self.right_layout.addWidget(self.grid_list)
        splitter.addWidget(self.right_container)
        splitter.setSizes([450, self.GRID_INFO.WIDGET_HEIGHT_DEFAULT])  
        

        
        
        main_layout.addWidget(splitter)

        
        # 3. Connect Scrollbars
        self.table_scrollbar = self.table.verticalScrollBar()
        self.grid_scrollbar = self.grid_list.verticalScrollBar()
        
        self.table_scrollbar.valueChanged.connect(self.sync_from_table)
        self.grid_scrollbar.valueChanged.connect(self.sync_from_grid)
        
        # Initial Population
        self.resize(self.GRID_INFO.WIDGET_HEIGHT_DEFAULT+450+20,800)
        self.refresh_ui()
        self.adjust_header_spacer()
        real_height = self.table.verticalHeader().defaultSectionSize()
        print(f"My actual table default row height is: {real_height}")
        
        

    
    


    def adjust_header_spacer(self):
        # Match right gap to table header + search bar height
        header_height = self.table.horizontalHeader().height()
        total_offset = header_height + self.left_layout.spacing()-4
        if total_offset > 0:
            self.header_spacer.setFixedHeight(total_offset)

    ## --- NEW: Filtering and Sorting Logic --- ##

    def apply_filter(self, text):
        """Bespoke function to filter the dataset."""
        text = text.lower()
        if not text:
            self.filtered_data = self.all_data.copy()
            self.filtered_df = self.df.copy()
        else:
            # Filters based on the "Name" column (index 0)
            self.filtered_data = [row for row in self.all_data if text in row[0].lower()]
            self.filtered_df = self.df[self.df['Name'].apply(lambda x: text in x.lower())]
            
            
        if not USE_DATAFRAME:
            self.apply_sort()
        else:
            self.apply_sort2()  
        self.refresh_ui()

    def on_header_clicked(self, logical_index):
        """Triggered when a column header is clicked."""
        if self.sort_col == logical_index:
            self.sort_asc = not self.sort_asc # Toggle direction
        else:
            self.sort_col = logical_index
            self.sort_asc = True # Default to ascending
            
        if not USE_DATAFRAME:
            self.apply_sort()
        else:
            self.apply_sort2()            
        self.refresh_ui()

    def apply_sort(self):
        """Sorts the current filtered data based on the selected column."""
        if self.sort_col == -1:
            return

        def sort_key(row):
            sort_col = self.sort_col
            val = row[sort_col]
            # Handle specialized sorting for Dates and Sizes
            if sort_col == 1: 
                return datetime.strptime(val, "%d/%m/%Y %H:%M")
            elif sort_col == 3: 
                return int(val.replace(" KB", ""))
            return val.lower() # Default alphabetical sorting

        self.filtered_data.sort(key=sort_key, reverse=not self.sort_asc)
        
    
    def apply_sort2(self):
        """Sorts self.filtered_df directly based on selected column index."""
        if self.sort_col == -1 or self.filtered_df.empty:
            return
        col_name = self.filtered_df.columns[self.sort_col]

        if self.sort_col == 1:
            sort_series = pd.to_datetime(self.filtered_df[col_name], format="%d/%m/%Y %H:%M")
        elif self.sort_col == 3:
            sort_series = self.filtered_df[col_name].str.replace(" KB", "", regex=False).astype(int)
        else:
            sort_series = self.filtered_df[col_name].str.lower()
    
        self.filtered_df = self.filtered_df.sort_values(by=col_name,  key=lambda _: sort_series, ascending=self.sort_asc, ignore_index=True )


    ## --- UI Refresh Logic --- ##

    def refresh_ui(self):
        """Clears and repopulates both lists based on self.filtered_data."""
        # Block signals so clearing doesn't trigger scroll synchronization
        self.table_scrollbar.blockSignals(True)
        self.grid_scrollbar.blockSignals(True)
        
        self.table.setRowCount(0)
        self.grid_list.clear()

        if USE_DATAFRAME:
            total_items = len(self.filtered_df)
        else:
            total_items = len(self.filtered_data)
        
        def round_up(x, n=6):
            return ((x + n - 1) // n) * n
        
        total_items_incl_buffer = round_up(total_items, self.GRID_INFO.CURRENT_NITEMS)
        self.table.setRowCount(total_items_incl_buffer)
        print('**refresh_ui',total_items_incl_buffer, self.GRID_INFO.CURRENT_NITEMS)
        
        if USE_DATAFRAME:
            
            video_extensions = ['.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.m4v']  
            
            for irow, (row, row_data) in enumerate(self.filtered_df.iterrows()):
                image_fp = None
                video_fp = None
                self.table.setRowHeight(irow, self.LIST_ROW_HEIGHT)
                for icol, (col, val) in enumerate(row_data.items()):
                    self.table.setItem(irow, icol, QTableWidgetItem(str(val)))
                    if icol==0:
                       name = val
                    if 'vs.jpg' in str(val):
                        image_fp = str(val)
                    if any(str(val).lower().endswith(ext) for ext in video_extensions):
                        video_fp = val
                if image_fp is None:
                    item = QListWidgetItem(self.default_icon, name)
                else:
                    item = QListWidgetItem(QIcon(image_fp), name)  
                    tooltip_html = f'<img src="{image_fp}" style="max-width: 400px; max-height: 400px;">'
                    item.setToolTip(tooltip_html)
                if video_fp is not None:
                    item.setData(Qt.UserRole, video_fp)
                    
                    
                    
                item.setTextAlignment(Qt.AlignCenter)
                self.grid_list.addItem(item)
        else:
            for irow, row in enumerate(self.filtered_data):
                self.table.setRowHeight(irow, self.LIST_ROW_HEIGHT)
                for i, e in enumerate(row):            
                    self.table.setItem(irow, i, QTableWidgetItem(e))
                    if i == 0:
                        if True:
                            item = QListWidgetItem(self.default_icon, e)
                            item.setTextAlignment(Qt.AlignCenter)
                            self.grid_list.addItem(item)


        for row in range(total_items, total_items_incl_buffer):
            self.buffer_rows(row)

        self.table_scrollbar.blockSignals(False)
        self.grid_scrollbar.blockSignals(False)

    def buffer_rows(self, row):
        self.table.setVerticalHeaderItem(row, QTableWidgetItem(""))
        self.table.setRowHeight(row, self.LIST_ROW_HEIGHT)
        ncols = self.table.columnCount()
        for col in range(ncols):
            buffer_item = QTableWidgetItem("")
            buffer_item.setFlags(Qt.NoItemFlags) 
            buffer_item.setBackground(self.table.palette().base())
            self.table.setItem(row, col, buffer_item)
        self.table.setSpan(row, 0, 1, ncols)     

    ## --- Scroll Sync Logic (Unchanged) --- ##

    def get_normalized_scroll_value(self):
        val = self.table_scrollbar.value()
        min_val = self.table_scrollbar.minimum()
        max_val = self.table_scrollbar.maximum()
        if max_val - min_val > 0:
            return (val - min_val) / (max_val - min_val)
        return 0.0            

    def sync_from_table(self, value):
        norm_value = self.get_normalized_scroll_value()
        self.grid_scrollbar.blockSignals(True)
        
        min_val = self.grid_scrollbar.minimum()
        max_val = self.grid_scrollbar.maximum()       
        target_pixel = ((max_val - min_val) * norm_value) + min_val
        
        self.grid_scrollbar.setValue(int(target_pixel))
        self.grid_list.viewport().update()
        self.grid_scrollbar.blockSignals(False)
        
    def sync_from_grid(self, value):      
        self.table_scrollbar.blockSignals(True)
        
        grid_row_pixel_step = self.GRID_INFO.ITEM_HEIGHT + self.GRID_INFO.SPACING
        grid_rows_scrolled = value / grid_row_pixel_step
        table_row_target = int(grid_rows_scrolled * 6)
        
        self.table_scrollbar.setValue(table_row_target)
        self.table.viewport().update()
        self.table_scrollbar.blockSignals(False)


    def on_cell_clicked(self, index):
            """
            Triggers when a cell is clicked. Checks if the cell (or any other cell 
            in the same row) contains a valid video file and plays it.
            """
            if not index.isValid():
                return
    
            video_extensions = ['.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.m4v']
            target_video_path = None
            
            # 1. First, check if the clicked cell itself is a valid video
            clicked_value = str(self.filtered_df.iat[index.row(), index.column()]).strip()
            if any(clicked_value.lower().endswith(ext) for ext in video_extensions) and os.path.isfile(clicked_value):
                target_video_path = clicked_value
            
            # 2. If not, scan all columns in this row to find the first valid video path
            else:
                row_data = self.filtered_df.iloc[index.row()]
                for value in row_data:
                    candidate = str(value).strip()
                    if any(candidate.lower().endswith(ext) for ext in video_extensions) and os.path.isfile(candidate):
                        target_video_path = candidate
                        break  # Stop searching once we find the first available video path
    
            # 3. If a video path was found anywhere in the row, launch it
            if target_video_path:
                print(f"Opening video from row {index.row()}: {target_video_path}")
            
                
                try:
                    if platform.system() == "Windows":
                        os.startfile(target_video_path)
                    elif platform.system() == "Darwin":  # macOS
                        subprocess.Popen(["open", target_video_path])
                    else:  # Linux
                        subprocess.Popen(["xdg-open", target_video_path])
                except Exception as e:
                    print(f"Error launching video player: {e}")

    def on_item_double_clicked(self, item):
            # Retrieve the original file path stored in UserRole
            video_fp = item.data(Qt.UserRole)
            item_text = item.text()
            os.startfile(video_fp)






    

    def sync_selection_from_table(self):
        """Highlights the grid item when a table row is clicked."""
        # Block signals to prevent an infinite loop of selection changes
        self.grid_list.blockSignals(True)
        self.grid_list.clearSelection()
        
        # Get selected rows in the table
        selected_ranges = self.table.selectedRanges()
        if selected_ranges:
            for selectionRange in selected_ranges:
                for row in range(selectionRange.topRow(), selectionRange.bottomRow() + 1):
                    # Ensure we don't select the empty buffer rows
                    if row < len(self.filtered_data):
                        grid_item = self.grid_list.item(row)
                        if grid_item:
                            grid_item.setSelected(True)
        
        self.grid_list.blockSignals(False)

    def sync_selection_from_grid(self):
        """Highlights the table row when a grid item is clicked."""
        # Block signals to prevent an infinite loop of selection changes
        self.table.blockSignals(True)
        self.table.clearSelection()
        
        # Get selected items in the grid
        selected_items = self.grid_list.selectedItems()
        for item in selected_items:
            row = self.grid_list.row(item)
            if row < len(self.filtered_data):
                # Select the corresponding row in the table
                self.table.selectRow(row)
                
        self.table.blockSignals(False)









if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PhotoManager(dummy_df)
    window.show()
    sys.exit(app.exec_())
    
    
    