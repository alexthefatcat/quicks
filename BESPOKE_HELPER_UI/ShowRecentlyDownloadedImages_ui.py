

import sys
import time
from pathlib import Path
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout, 
                             QVBoxLayout, QLabel, QMenu, QAction, QGroupBox)
from PyQt5.QtCore import Qt, pyqtSignal, QObject, QTimer
from PyQt5.QtGui import QPixmap
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp'}

class WatcherSignal(QObject):
    """Bridge signal to communicate thread-safely from watchdog to PyQt GUI."""
    file_changed = pyqtSignal()


class DownloadHandler(FileSystemEventHandler):
    """Monitors folder creation and file rename (browser completion) events."""
    def __init__(self, signal):
        super().__init__()
        self.signal = signal

    def on_created(self, event):
        if not event.is_directory and Path(event.src_path).suffix.lower() in IMAGE_EXTENSIONS:
            self.signal.file_changed.emit()

    def on_moved(self, event):
        if not event.is_directory and Path(event.dest_path).suffix.lower() in IMAGE_EXTENSIONS:
            self.signal.file_changed.emit()


class ImageTrackerApp(QMainWindow):
    def __init__(self, watch_folder):
        super().__init__()
        self.watch_folder = Path(watch_folder)

        self.setWindowTitle(f"PyQt5 Image Monitor - {self.watch_folder}")
        self.resize(950, 580)
        self.apply_dark_theme()

        # Connect watchdog signal to GUI slot
        self.watcher_signal = WatcherSignal()
        self.watcher_signal.file_changed.connect(self.on_file_changed)

        self.setup_ui()
        self.refresh_images()
        self.start_file_watcher()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)

        # Left Side - Most Recent Image (Bigger)
        self.group_main = QGroupBox(" Most Recent ")
        left_layout = QVBoxLayout(self.group_main)
        self.lbl_main = QLabel("No Image")
        self.lbl_main.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(self.lbl_main)
        main_layout.addWidget(self.group_main, stretch=2)

        # Right Side - Previous 2 Images (Smaller stacked)
        right_container = QWidget()
        right_layout = QVBoxLayout(right_container)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(10)

        self.group_sub1 = QGroupBox(" Previous #1 ")
        sub1_layout = QVBoxLayout(self.group_sub1)
        self.lbl_sub1 = QLabel("No Image")
        self.lbl_sub1.setAlignment(Qt.AlignCenter)
        sub1_layout.addWidget(self.lbl_sub1)
        right_layout.addWidget(self.group_sub1)

        self.group_sub2 = QGroupBox(" Previous #2 ")
        sub2_layout = QVBoxLayout(self.group_sub2)
        self.lbl_sub2 = QLabel("No Image")
        self.lbl_sub2.setAlignment(Qt.AlignCenter)
        sub2_layout.addWidget(self.lbl_sub2)
        right_layout.addWidget(self.group_sub2)

        main_layout.addWidget(right_container, stretch=1)

    # --- Right Click Context Menu ("Always on Top") ---
    def contextMenuEvent(self, event):
        menu = QMenu(self)

        always_on_top_action = QAction("Always on Top", self)
        always_on_top_action.setCheckable(True)

        # Read current window state flag
        is_on_top = bool(self.windowFlags() & Qt.WindowStaysOnTopHint)
        always_on_top_action.setChecked(is_on_top)

        always_on_top_action.triggered.connect(self.toggle_always_on_top)
        menu.addAction(always_on_top_action)

        menu.exec_(event.globalPos())

    def toggle_always_on_top(self, checked):
        flags = self.windowFlags()
        if checked:
            flags |= Qt.WindowStaysOnTopHint
        else:
            flags &= ~Qt.WindowStaysOnTopHint

        self.setWindowFlags(flags)
        self.show()  # Re-render window to apply flag changes immediately

    # --- Image Handling ---
    def get_latest_images(self, count=3):
        try:
            files = [
                f for f in self.watch_folder.iterdir()
                if f.is_file() and f.suffix.lower() in IMAGE_EXTENSIONS
            ]
            files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
            return files[:count]
        except Exception as e:
            print(f"Error accessing directory: {e}")
            return []

    def refresh_images(self):
        images = self.get_latest_images(3)
        slots = [
            (self.lbl_main, 550, 500),
            (self.lbl_sub1, 260, 220),
            (self.lbl_sub2, 260, 220)
        ]

        for index, (label, w, h) in enumerate(slots):
            if index < len(images):
                img_path = str(images[index])
                pixmap = QPixmap(img_path)
                if not pixmap.isNull():
                    scaled_pix = pixmap.scaled(w, h, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    label.setPixmap(scaled_pix)
                else:
                    label.setText("Loading Error")
            else:
                label.setText("No Image")

    def on_file_changed(self):
        # Brief delay to allow the browser to release write locks on the file
        QTimer.singleShot(350, self.refresh_images)

    def start_file_watcher(self):
        event_handler = DownloadHandler(self.watcher_signal)
        self.observer = Observer()
        self.observer.schedule(event_handler, str(self.watch_folder), recursive=False)
        self.observer.start()

    def closeEvent(self, event):
        self.observer.stop()
        self.observer.join()
        event.accept()

    def apply_dark_theme(self):
        self.setStyleSheet("""
            QMainWindow { background-color: #1e1e2e; }
            QGroupBox {
                color: #cdd6f4;
                border: 1px solid #45475a;
                border-radius: 8px;
                margin-top: 10px;
                font-weight: bold;
            }
            QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px; }
            QLabel { color: #6c7086; font-size: 13px; }
            QMenu {
                background-color: #181825;
                color: #cdd6f4;
                border: 1px solid #45475a;
            }
            QMenu::item:selected { background-color: #313244; }
        """)


if __name__ == "__main__":
    target_downloads = Path.home() / "Downloads"
    app = QApplication(sys.argv)
    window = ImageTrackerApp(target_downloads)
    window.show()
    sys.exit(app.exec_())







import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class ImageThumbnailApp(QWidget):
    def __init__(self, image_path):
        super().__init__()
        self.setWindowTitle("PyQt5 Thumbnail Viewer")
        self.resize(300, 300)

        layout = QVBoxLayout(self)

        # 1. Load full image into QPixmap
        pixmap = QPixmap(image_path)

        # 2. Create a thumbnail (200x200 max bounding box)
        if not pixmap.isNull():
            thumbnail = pixmap.scaled(
                200, 200, 
                Qt.KeepAspectRatio, 
                Qt.SmoothTransformation
            )
        else:
            thumbnail = QPixmap()

        # 3. Display in QLabel
        label = QLabel()
        if not thumbnail.isNull():
            label.setPixmap(thumbnail)
        else:
            label.setText("Failed to load image")
            
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Replace with the path to your image
    window = ImageThumbnailApp("example.jpg")
    window.show()
    sys.exit(app.exec_())









































