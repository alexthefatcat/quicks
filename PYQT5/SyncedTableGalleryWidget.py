

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


import math
from PyQt5.QtCore import QRectF, QPointF




import pandas as pd


print_debug = lambda *args, **kwargs:print(*args, **kwargs) if DEBUG else None

DEBUG = True






        
class LineOverlay(QWidget):
    """A transparent overlay widget that paints horizontal lines synchronized with scrolling."""
    def __init__(self, target_list_widget, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.list_widget = target_list_widget
        
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
            if 0 <= v <= self.height():
                painter.drawLine(0, v, full_width, v)

        painter.end()

def chunk_by_size(items: list, chunk_size: int = 6) -> list[list]:
    return [items[i : i + chunk_size] for i in range(0, len(items), chunk_size)]






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



























class SyncedTableGallery(QWidget):
    def __init__(self, parent=None, df=None, ListWidget=None, TableWidget=None, fixed_no_images=6):
        super().__init__(parent)
        self.LIST_ROW_HEIGHT = 22
        self.fixed_no_images = fixed_no_images # if None expands when explanding
        
        self.df = df
        self.index__sorting_mask_default = pd.Series(True, index=self.df.index)
        self.index__sorting_mask = self.index__sorting_mask_default.copy()
        self.columns = list(df.columns)
        self.ratings_columns_index = [i for i,e in enumerate(self.columns) if 'Rating' in e]

        self.ListWidget = QListWidget if ListWidget is None else ListWidget
        self.TableWidget = QTableWidget if TableWidget is None else TableWidget

        self.init_table()
        self.init_gridlist()
        self.init_ui()
        self.create_default_icon()
        
        self.sync_scrolling_two_widgets()        
        self.refresh_view
        self.reset_grid_item_sizes()
        self.sort_func_dict = {}

        self.star_changes = []
        self.refresh_view()

        # Create overlay attached to grid_list
        self.line_overlay = LineOverlay(target_list_widget=self.gridlist, parent=self)

        def _on_grid_resize(event):
            # Call original resize event
            super(type(self.gridlist), self.gridlist).resizeEvent(event)
            # Stretch overlay over the entire grid area
            self.line_overlay.setGeometry(self.rect())    
        

        # Keep overlay dimensions synced with grid_list viewport
        self.gridlist.resizeEvent = _on_grid_resize
        


    @property
    def df_view(self):
        mask = self.index__sorting_mask
        df = self.df
        df_view = df.loc[mask.index]    
        df_view = df_view[mask]
        return df_view

        
    def create_default_icon(self):
        pixmap = QPixmap(90, 90)
        pixmap.fill(Qt.darkGray)
        self.default_icon = QIcon(pixmap)
    
    def init_gridlist(self):
        self.gridlist = self.ListWidget()  
        self.gridlist.setViewMode(QListWidget.IconMode)
        self.gridlist.setIconSize(QSize(90, 90))
        self.gridlist.setResizeMode(QListWidget.Adjust)
        self.gridlist.setMovement(QListWidget.Static)
        self.gridlist.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.gridlist.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.gridlist.setStyleSheet(" QListWidget::item { border:none; padding-top: 18px}")  

        #self.gridlist.setStyleSheet(" QListWidget::item { border-top: 1px solid lightgray;padding-top: 18px;}")  

        
    def sync_scrolling_two_widgets(self):
        vbar_a = self.gridlist.verticalScrollBar()
        vbar_b = self.table.verticalScrollBar()  
        
        def nearist_value(value, container):
            return min(container,key=lambda x:abs(x-value))



        def covnert(value, total_rows1, total_rows2):
            
            sum1 = sum(total_rows1)
            sum2 = sum(total_rows2)
            ratio = sum2/sum1
            print('-----', ratio, value)
            value2 = value*int(ratio)
            return value2

        def sync_scroll2(value):
            #tidy this up
            
            
            
            #            COLUMNS = 6  # Number of thumbnail columns in grid
            
            # def sync_grid_to_table_row():
            #     # Find the top visible row in the table
                
            #     if top_row >= 0:
            #         # Get corresponding grid item index
            #         grid_item = self.grid.item(top_row)
            #         if grid_item:
            #             self.grid.scrollToItem(grid_item, QAbstractItemView.PositionAtTop)
                        
  
            vbar = self.table.verticalScrollBar()
            total_rows1 = (vbar.maximum(), vbar.pageStep()  )  
            vbar = self.gridlist.verticalScrollBar()
            total_rows2 = (vbar.maximum(), vbar.pageStep()  )
            print(total_rows1, sum(total_rows1),total_rows2, sum(total_rows2),sum(total_rows2)/sum(total_rows1) )
            
  
            if False:
                print('Compare', vbar_a.maximum(), vbar_b.maximum(),vbar_a.maximum()/ vbar_b.maximum(),(vbar_a.maximum()+1)/(vbar_b.maximum()+1),(vbar_a.maximum()-1)/(vbar_b.maximum()-1))     
                if False:
                          
                    #Compare 1044 46 22.695652173913043 22.23404255319149 23.177777777777777
                    rat = 23
                    points = [rat*n for n in range(vbar_b.maximum())]
                else:
                    max_a = vbar_a.maximum()
                    max_b = vbar_b.maximum()
                    rat = (max_a / max_b)
                    points = [round(n * rat) for n in range(max_b + 1)]
                    
                    
                top_left_point = self.table.viewport().rect().topLeft()
                top_row = self.table.indexAt(top_left_point).row()
                
                
                print(top_row,'top row')
                    
                    
                    
                    
                    
                
                points.append(vbar_a.maximum())
                print(points,points[value])
                
                
                j = (vbar_a.maximum())/len(self.df_view) #13.05
                print(j)
                
                ratio = vbar_a.maximum()/max(vbar_b.maximum(),1)
                
    
                value2 = int((value*ratio))
                v = value2
                
                value2 = value2 #-value2%23
                value2 = points[value]
                
                #value2 = 13*value
                
                
                print_debug('sync_scroll2', value, ratio, v, value2)      
            value2 = covnert(value, total_rows1, total_rows2)
            #vbar_b.blockSignals(True)  # Prevent vbar_b from firing back!
            vbar_a.setValue(value2)
            vbar_b.setValue(value)            
            #vbar_b.blockSignals(False)    
    
        self.scrollbar.valueChanged.connect(sync_scroll2)          
           
        def sync_scroll3(value):
            vbar_b.blockSignals(True)  # Prevent vbar_b from firing back!
            self.scrollbar.setValue(value)
            vbar_b.blockSignals(False)
            print_debug('sync_scroll3', value)  
        
        vbar_b.valueChanged.connect(sync_scroll3)  
        
        def sync_scroll4(value):
            ratio = vbar_b.maximum()/max(vbar_a.maximum(),1)
            value2 = int(value*ratio) 
            print_debug('sync_scroll4', value, value2, ratio)  
            vbar_a.blockSignals(True) 
            vbar_b.setValue(value2)
            vbar_a.blockSignals(False)
            #self.scrollbar.setValue(value2)
        
        vbar_a.valueChanged.connect(sync_scroll4) 
        

        
    # def sync_scrolling_two_widgets(self):
    #     vbar_a = self.gridlist.verticalScrollBar()
    #     vbar_b = self.table.verticalScrollBar()       

    #     def sync_scroll2(value):
    #         print_debug('max',)
    #         ratio = vbar_a.maximum()/max(vbar_b.maximum(),1)
    #         value2 = int(value*ratio)
    #         value2 = value2 -value2%23
    #         #vbar_b.blockSignals(True)  # Prevent vbar_b from firing back!
    #         vbar_a.setValue(value2)
    #         vbar_b.setValue(value)            
    #         #vbar_b.blockSignals(False)    
    
    #     self.scrollbar.valueChanged.connect(sync_scroll2)          
           
    #     def sync_scroll3(value):
    #         vbar_b.blockSignals(True)  # Prevent vbar_b from firing back!
    #         self.scrollbar.setValue(value)
    #         vbar_b.blockSignals(False)         
        
    #     vbar_b.valueChanged.connect(sync_scroll3)  
        
    #     def sync_scroll4(value):
    #         ratio = vbar_b.maximum()/max(vbar_a.maximum(),1)
    #         value2 = int(value*ratio)        
    #         vbar_a.blockSignals(True) 
    #         vbar_b.setValue(value2)
    #         vbar_a.blockSignals(False)
    #         #self.scrollbar.setValue(value2)
        
    #     vbar_a.valueChanged.connect(sync_scroll4) 
        

        

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
      
    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.addWidget(self.table)

        # to add spacing at the top of grid to be same as list
        column_header_height_debug = 23
        self.right_container = QWidget()
        self.right_layout = QHBoxLayout()
        self.scrollbar = QScrollBar()       
        

        self.right_layout.addWidget(self.gridlist)         
        self.right_layout.addWidget(self.scrollbar)           
        
       
        self.right_layout.setContentsMargins(0, column_header_height_debug, 0, 0)        
        self.right_container.setLayout(self.right_layout)
        
        
        self.splitter.addWidget(self.right_container)

        layout.addWidget(self.splitter)
        
  
        
        
    
    def refresh_view(self):
        self.table.clear()
        self.gridlist.clear()
        
        df_view = self.df_view
        
        if df_view.empty:
            return

        total_items = len(df_view)
        total_items_incl_buffer = self.__round_up(total_items, 6)

        self.table.setColumnCount(len(self.df_view.columns))
        self.table.setHorizontalHeaderLabels([str(c) for c in df_view.columns])
        self.table.setRowCount(total_items_incl_buffer)
        
        
        chunks = chunk_by_size(list(enumerate(df_view.iterrows())))
        counter = 0
        for ichunk, chunk in enumerate(chunks):
            chunk_items = []
            for irow, (_, row_data) in chunk:
                self.table.setRowHeight(irow, self.LIST_ROW_HEIGHT)
                item_name = f"Item {irow + 1}"  # Fallback name
                 
                for icol, (_, val) in enumerate(row_data.items()):

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
                        
                    if icol == 0:
                        item_name = str(val)

                image = self.get_image_from_row(row_data)
                chunk_items.append([item_name, image])         
                
            for item_name, image in chunk_items:
                item = QListWidgetItem(image, item_name)
                item.setTextAlignment(Qt.AlignCenter)
                item.setData(Qt.UserRole, {"id": counter})
                counter +=1                
                item = self.modify_grid_item(item)                
                self.gridlist.addItem(item)
    



        for row in range(total_items, total_items_incl_buffer):
            self.create_blank_row(row)


    def on_rating_changed(self, col, row, new_rating):
        mask = self.index__sorting_mask
        irow = mask[mask].index[row]        
        
        print(f"Database Sync: '{row}' set to {new_rating} stars.{irow}, {col=}")        
        #song_title = self.table.item(row, 1).text()


        col_name = self.columns[col]

        self.star_changes.append([irow, col_name, new_rating])        
        self.df.loc[irow,col_name] = new_rating

        
        
            
    def modify_grid_item(self, item):
        return item

    def __round_up(self, x, n):
        return ((x + n - 1) // n) * n
    
    def get_image_from_row(self, row_data):
        return self.default_icon

    def create_blank_row(self, row):
        self.table.setVerticalHeaderItem(row, QTableWidgetItem(""))
        self.table.setRowHeight(row, self.LIST_ROW_HEIGHT)
        ncols = self.table.columnCount()
        for col in range(ncols):
            buffer_item = QTableWidgetItem("")
            buffer_item.setFlags(Qt.NoItemFlags) 
            buffer_item.setBackground(self.table.palette().base())
            self.table.setItem(row, col, buffer_item)
        self.table.setSpan(row, 0, 1, ncols)     

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

    
    # def resizeEvent(self, event):
    #         """Keep overlay sized dynamically with the main window."""
    #         super().resizeEvent(event)
    #         if hasattr(self, 'overlay'):
    #             self.overlay.setGeometry(0, 0, self.width(), self.height())
    #             self.overlay.raise_()
    
  
              
    
    # def resizeEvent(self, event):
    #     super().resizeEvent(event)        

    #     source = self.table.verticalScrollBar()
    #     target = self.scrollbar
        
    #     # Copy properties
    #     target.setOrientation(source.orientation())
    #     target.setRange(source.minimum(), source.maximum())
    #     target.setPageStep(source.pageStep())
    #     target.setSingleStep(source.singleStep())
    #     target.setValue(source.value())
    #     print_debug("Source")
    #     print_debug(source.minimum(), source.maximum(), source.pageStep())
    #     print_debug("Target")
    #     print_debug(target.minimum(), target.maximum(), target.pageStep())



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
    
    
    def resizeEvent(self, event):
        super().resizeEvent(event)        
        self.copy_scrollbar_properties()

    def showEvent(self, event):
        super().showEvent(event)
        self.copy_scrollbar_properties()

    




    def table_column_sort(self, logical_index):    
        if not hasattr(self, 'table_column_sort_column'):
           self.table_column_sort_column = None
           
        if self.table_column_sort_column == logical_index:
            self.table_column_sort_ascending = not self.table_column_sort_ascending # Toggle direction
        else:
            self.table_column_sort_column = logical_index
            self.table_column_sort_ascending = True # Default to ascending
        self.apply_sort()
        



    def apply_sort(self):
        print('apply sort')
        """Sorts self.filtered_df directly based on selected column index."""
        if self.table_column_sort_column == -1 or self.df_view.empty:
            return
        
        df = self.df
        col_name = df.columns[self.table_column_sort_column] 
        sort_series = df[col_name].str.lower()
        ascending = self.table_column_sort_ascending
        
        if False:
            if self.sort_col == 1:
                sort_series = pd.to_datetime(df[col_name], format="%d/%m/%Y %H:%M")
    
            if 'size' in col_name.lower():
                print('Sort by size')
                sort_series = df[col_name].str.replace(" KB", "", regex=False).astype(int)

        print(f'Filtering Column, sort_func_dict {list(self.sort_func_dict.keys())}')
        if col_name in self.sort_func_dict:
            func = self.sort_func_dict[col_name]
            sort_series = self.df[col_name].apply(func)

        df = self.df[[col_name]].sort_values(by=col_name, key= lambda _: sort_series, ascending=ascending )
        self.index__sorting_mask = self.index__sorting_mask.loc[df.index]
        
        self.refresh_view()








    