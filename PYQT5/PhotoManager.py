'''



add at the end of say 2 rows

number of rows has to be deviable by 6 or you get line up problems






I have create a pyqt5 window beflow the idea
is on the left it shows info about the image 
and on the right it shows an image
it is done in a way where the lines  are 1/6 the highet of the image but there are 6 images enxtotgeht 
whcih means an image is always next to its info

so at the moment it contains QTableWidget and QListWidget
I next want to add a search bar that will dynamically filter the table when typed in
also you can click the columns and they will be ordered
but also the images on the right now match there filtering and ordering
I assume you will need differnt classes of widget
I want there to be a bespoke function that performs the filtering




'''
    

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
        



import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QSplitter, QTableWidget, 
                             QTableWidgetItem, QListWidget, QListWidgetItem,
                             QAbstractItemView, QWidget, QVBoxLayout, QSpacerItem, QSizePolicy)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QIcon

class PhotoManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Synchronized Image Gallery")
        self.resize(1300, 800)
        
        self.LIST_ROW_HEIGHT = 30
        self.GRID_ITEM_WIDTH = 130
        self.GRID_ITEM_HEIGHT = 180#160
        self.GRID_SPACING = 30
        
        splitter = QSplitter(Qt.Horizontal)
        self.setCentralWidget(splitter)
        
        # 1. Left Table Layout
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Name", "Date Modified", "Type", "Size"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setVerticalScrollMode(QAbstractItemView.ScrollPerItem)
        splitter.addWidget(self.table)
        
        # 2. Right Pane: Container Widget to hold Spacer + Grid List
        self.right_container = QWidget()
        self.right_layout = QVBoxLayout(self.right_container)
        
        # Remove all default padding/margins around the right layout container
        self.right_layout.setContentsMargins(0, 0, 0, 0)
        self.right_layout.setSpacing(0)
        
        # CRITICAL UI FIX: Create a blank placeholder widget to mimic the header height
        # Most default windows headers are around 25 to 30 pixels high.
        self.header_spacer = QWidget()
        self.header_spacer.setFixedHeight(25) 
        self.right_layout.addWidget(self.header_spacer)
        
        # Create the actual Grid List
        self.grid_list = QListWidget()
        self.grid_list.setViewMode(QListWidget.IconMode)
        self.grid_list.setResizeMode(QListWidget.Adjust)
        self.grid_list.setMovement(QListWidget.Static)
        self.grid_list.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.grid_list.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        # Frame borders can throw off alignment slightly, so we clean it up
        self.grid_list.setStyleSheet("QListWidget { border: none; }")
        
        self.grid_list.setIconSize(QSize(120, 120))
        self.grid_list.setGridSize(QSize(self.GRID_ITEM_WIDTH, self.GRID_ITEM_HEIGHT)) 
        self.grid_list.setSpacing(self.GRID_SPACING)
        
        # Add the list below our spacer in the container layout
        self.right_layout.addWidget(self.grid_list)
        
        # Add the full container to the splitter instead of just the list
        splitter.addWidget(self.right_container)
        
        splitter.setSizes([450, 850])
        
        # 3. Connect Scrollbars
        self.table_scrollbar = self.table.verticalScrollBar()
        self.grid_scrollbar = self.grid_list.verticalScrollBar()
        
        self.table_scrollbar.valueChanged.connect(self.sync_from_table)
        self.grid_scrollbar.valueChanged.connect(self.sync_from_grid)
        
        self.populate_data()
        
        # Fine-tune the header spacer dynamically after window rendering
        self.adjust_header_spacer()

    def adjust_header_spacer(self):
        """Dynamically matches the blank space height to the real table header height."""
        header_height = self.table.horizontalHeader().height()
        if header_height > 0:
            self.header_spacer.setFixedHeight(header_height)

    def populate_data(self):
        total_items = 633
        fileinfos = create_dummy_table(total_items)
        
        def round_up(x, n=6):
            return ((x + n -1) // n) * n
        
        total_items_incl_buffer = round_up(total_items)
        self.table.setRowCount(total_items_incl_buffer)
        
        pixmap = QPixmap(125, 125)
        pixmap.fill(Qt.darkGray)
        icon = QIcon(pixmap)
        
        for irow, row in enumerate(fileinfos):
            self.table.setRowHeight(irow, self.LIST_ROW_HEIGHT)
            for i,e in enumerate(row):            
                self.table.setItem(irow, i, QTableWidgetItem(e))
                if i==0:
                    item = QListWidgetItem(icon, e)
                    item.setTextAlignment(Qt.AlignCenter)
                self.grid_list.addItem(item)
        

        for row in range(total_items, total_items_incl_buffer):
            print(row)
            self.buffer_rows(row)

                    
    def get_normalized_scroll_value(self):
        """Returns exactly 0.0 at the top and 1.0 at the bottom."""
        val = self.table_scrollbar.value()
        min_val = self.table_scrollbar.minimum()
        max_val = self.table_scrollbar.maximum()
        if max_val - min_val > 0:
            return (val - min_val) / (max_val - min_val)
        return 0.0            

    def sync_from_table(self, value):
        value = self.get_normalized_scroll_value()
        self.grid_scrollbar.blockSignals(True)
        
        current_row_index = value
        grid_row = current_row_index / 6.0
        grid_row_pixel_step = self.GRID_ITEM_HEIGHT + self.GRID_SPACING
        target_pixel = int(grid_row * grid_row_pixel_step)
        

        min_val = self.grid_scrollbar.minimum()
        max_val = self.grid_scrollbar.maximum()       
        target_pixel = ((max_val-min_val)*value)+min_val
        
        
        self.grid_scrollbar.setValue(int(target_pixel))
        self.grid_list.viewport().update()
        
        self.grid_scrollbar.blockSignals(False)
        

    def sync_from_grid(self, value):      
        self.table_scrollbar.blockSignals(True)
        
        grid_row_pixel_step = self.GRID_ITEM_HEIGHT + self.GRID_SPACING
        grid_rows_scrolled = value / grid_row_pixel_step
        table_row_target = int(grid_rows_scrolled * 6)
        
        self.table_scrollbar.setValue(table_row_target)
        self.table.viewport().update()
        
        self.table_scrollbar.blockSignals(False)


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




















if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PhotoManager()
    window.show()
    sys.exit(app.exec_())
    
    
    
    
    
    
    