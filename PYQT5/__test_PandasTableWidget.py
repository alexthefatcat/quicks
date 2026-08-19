

import os
import sys
import pandas as pd
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLineEdit, QVBoxLayout, 
    QWidget, QLabel, QToolTip
)

import platform
# Importing base class from your separate file
from PandasTableWidget import QPandasTableWidget
from quick_example import film_df, country_df
import subprocess

class ImageHoverTooltip(QLabel):
    """A custom floating window that displays an image preview in its native resolution."""
    def __init__(self, parent=None):
        # Qt.ToolTip flag ensures it floats; FramelessWindowHint removes window borders
        super().__init__(parent, Qt.ToolTip | Qt.FramelessWindowHint)
        self.setStyleSheet("border: 2px solid #888; background-color: black;")
        self.setScaledContents(True)
        self.setAttribute(Qt.WA_ShowWithoutActivating)

    def show_image(self, file_path, global_pos):
        if os.path.exists(file_path):
            pixmap = QPixmap(file_path)
            
            if not pixmap.isNull():
                # 1. Get the natural width and height of the loaded file
                natural_size = pixmap.size()
                
                # 2. Resize the tooltip window to match the exact resolution
                self.resize(natural_size)
                self.setPixmap(pixmap)
                
                # 3. Position the window slightly offset from the mouse cursor
                self.move(global_pos + QPoint(15, 15))
                self.show()
            else:
                self.hide()
        else:
            self.hide()

class QPandasTableWidget_ImageHover(QPandasTableWidget):
    """Inherits QPandasTableWidget and adds image previews when hovering over filepaths."""
    def __init__(self, df=None, parent=None):
        super().__init__(df, parent)

        self.setWordWrap(False)
        # 1. Enable Mouse Tracking to receive hover events without needing a mouse-click
        self.setMouseTracking(True)
        
        # 2. Instantiate our floating image preview widget
        self.image_popup = ImageHoverTooltip()
        
        # 3. Connect PyQt's internal hover signal
        self.entered.connect(self.on_cell_hovered)
        self.doubleClicked.connect(self.on_cell_clicked)

    def on_cell_hovered(self, index):
        """Triggers every time the cursor moves over a new cell coordinate."""
        if not index.isValid():
            self.image_popup.hide()
            return

        # Retrieve the raw data value from our model view
        cell_value = str(self.df_view.iat[index.row(), index.column()]).strip()

        # Simple verification: check if value matches common image paths or valid files
        is_image_path = (
            any(cell_value.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.bmp', '.webp']) 
            and os.path.isfile(cell_value)
        )

        if is_image_path:
            # Map widget tracking space to global desktop space
            global_cursor_pos = self.mapToGlobal(self.visualRect(index).center())
            self.image_popup.show_image(cell_value, global_cursor_pos)
        else:
            self.image_popup.hide()

    def leaveEvent(self, event):
        """Ensure the preview closes immediately when the mouse exits the table grid."""
        self.image_popup.hide()
        super().leaveEvent(event)

    
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
            clicked_value = str(self.df_view.iat[index.row(), index.column()]).strip()
            if any(clicked_value.lower().endswith(ext) for ext in video_extensions) and os.path.isfile(clicked_value):
                target_video_path = clicked_value
            
            # 2. If not, scan all columns in this row to find the first valid video path
            else:
                row_data = self.df_view.iloc[index.row()]
                for value in row_data:
                    candidate = str(value).strip()
                    if any(candidate.lower().endswith(ext) for ext in video_extensions) and os.path.isfile(candidate):
                        target_video_path = candidate
                        break  # Stop searching once we find the first available video path
    
            # 3. If a video path was found anywhere in the row, launch it
            if target_video_path:
                print(f"Opening video from row {index.row()}: {target_video_path}")
                
                # Hide the image preview popup so it doesn't block the screen
                self.image_popup.hide()
                
                try:
                    if platform.system() == "Windows":
                        os.startfile(target_video_path)
                    elif platform.system() == "Darwin":  # macOS
                        subprocess.Popen(["open", target_video_path])
                    else:  # Linux
                        subprocess.Popen(["xdg-open", target_video_path])
                except Exception as e:
                    print(f"Error launching video player: {e}")



class MainWindow(QMainWindow):
    def __init__(self, table_widget):
        super().__init__()
        self.setWindowTitle("Pandas Table with Live Search & Image Hover")
        #self.resize(750, 500)
        
        # Central layout container
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        
        # 1. Add Search Box
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Type to filter columns...")
        layout.addWidget(self.search_box)
        
        # 2. Add Custom Inherited Table
        self.table_widget = table_widget
        layout.addWidget(self.table_widget)
        
        # 3. Connect Search Box keystrokes to the filtering logic
        self.search_box.textChanged.connect(self.table_widget.set_search_filter)
        
        self.setCentralWidget(central_widget)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    #pandastablewidget = QPandasTableWidget_ImageHover(film_df)
    pandastablewidget = QPandasTableWidget_ImageHover(df_database)
    window = MainWindow(pandastablewidget)
    window.show()
    sys.exit(app.exec_())
    
    
    
    
    