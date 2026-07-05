# -*- coding: utf-8 -*-
"""
Created on Thu Jul 17 16:05:09 2025

@author: Alexm


dropdown with type

so example country pick

not quite working

"""






from PyQt5.QtWidgets import QApplication, QComboBox, QMainWindow, QCompleter, QStyledItemDelegate
from PyQt5.QtCore import Qt, QStringListModel
from PyQt5.QtGui import QPainter, QPen
import sys

class SeparatorDelegate(QStyledItemDelegate):
    """Custom delegate to draw a horizontal line for the separator item."""
    def paint(self, painter, option, index):
        if index.data() == "SEPARATOR":
            painter.save()
            pen = QPen(Qt.black, 1)
            painter.setPen(pen)
            y = option.rect.center().y()
            painter.drawLine(option.rect.left(), y, option.rect.right(), y)
            painter.restore()
        else:
            super().paint(painter, option, index)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Editable ComboBox with Line Separator")
        self.setGeometry(100, 100, 300, 200)

        # Sample list of items
        self.items = ["Apple", "Banana", "Cherry", "Date", "Elderberry", "Fig", "Grape"]
        self.priority_items = ["Cherry", "Date"]  # Items to prioritize at the top
        self.all_items = sorted(self.items)  # Full list in alphabetical order

        # Create ComboBox
        self.combo = QComboBox(self)
        self.combo.setEditable(True)
        self.combo.setGeometry(50, 50, 200, 30)

        # Set custom delegate for the combobox
        self.combo.setItemDelegate(SeparatorDelegate())

        # Populate ComboBox with prioritized items and separator
        self.populate_combobox()
        self.combo.setCurrentIndex(-1)  # No item selected
        self.combo.lineEdit().setText("")  # Ensure text field is empty

        # Set up QCompleter with all items
        self.completer = QCompleter(self.all_items, self.combo)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setFilterMode(Qt.MatchContains)
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
        self.combo.setCompleter(self.completer)

        # Connect text changed signal to filter function
        self.combo.lineEdit().textEdited.connect(self.filter_items)

        # Connect dropdown show signal to reset items
        self.combo.activated.connect(self.on_dropdown)

    def populate_combobox(self):
        """Populate the combobox with priority items, a separator, and all items."""
        self.combo.clear()
        # Add priority items
        for item in self.priority_items:
            self.combo.addItem(item)
        # Add separator
        self.combo.addItem("SEPARATOR")
        self.combo.model().item(self.combo.count() - 1).setEnabled(False)  # Disable separator
        # Add all items in alphabetical order
        for item in self.all_items:
            self.combo.addItem(item)

    def filter_items(self, text):
        # Clear current items
        self.combo.clear()
        # Filter items based on input text
        if text:
            
            # Base filtered items (items containing the input text)
            filtered_items = [item for item in self.all_items if text.lower() in item.lower()]
            # Special case: include "Banana" when "yellow" or "yell" is typed
            if text.lower() in "yellow" and "Banana" not in filtered_items:
                filtered_items.append("Banana")
            # Sort filtered items
            filtered_items = sorted(filtered_items)
            # Add priority items (if they match the filter or are "Banana" for "yellow"/"yell")
            priority_added = False
            print(filtered_items)
            for item in self.priority_items:
                if text.lower() in item.lower() or (text.lower() in "yellow" and item == "Banana"):
                    self.combo.addItem(item)
                    priority_added = True
            # Add separator if there are priority items in the filtered list
            if priority_added:
                self.combo.addItem("SEPARATOR")
                self.combo.model().item(self.combo.count() - 1).setEnabled(False)
            # Add filtered items
            for item in filtered_items:
                self.combo.addItem(item)
            # Update completer with filtered items
            self.completer.setModel(QStringListModel(filtered_items, self.completer))
        else:
            # If text is empty, show prioritized list
            self.populate_combobox()
            # Reset completer to full item list
            self.completer.setModel(QStringListModel(self.all_items, self.completer))

        # Restore the current text to preserve free-form input
        self.combo.lineEdit().setText(text)

    def on_dropdown(self):
        # When dropdown is clicked and input is empty, show prioritized list
        current_text = self.combo.lineEdit().text()
        if not current_text:
            self.populate_combobox()
            # Reset completer to full item list
            self.completer.setModel(QStringListModel(self.all_items, self.completer))
        # Ensure current text is preserved
        self.combo.lineEdit().setText(current_text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())




# how to control combobox filling with own filtering



    
    
    
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QListWidget, QVBoxLayout, QFrame
from PyQt5.QtCore import Qt, QEvent

class CustomComboBox(QWidget):
    def __init__(self, items, parent=None):
        super().__init__(parent)
        self.all_items = items
        self.filtered_items = items.copy()
        self.is_initializing = True  # Flag to prevent popup during init

        # Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Line edit for text input
        self.line_edit = QLineEdit(self)
        self.line_edit.setPlaceholderText("Type to filter...")
        layout.addWidget(self.line_edit)

        # Popup list
        self.popup = QFrame(self, Qt.Popup)
        self.popup.setFrameShape(QFrame.StyledPanel)
        self.popup_layout = QVBoxLayout(self.popup)
        self.list_widget = QListWidget(self.popup)
        self.popup_layout.addWidget(self.list_widget)
        self.popup.hide()  # Ensure popup is hidden initially

        # Populate list initially
        self.filter_items("")
        self.list_widget.setCurrentRow(-1)  # No item selected

        # Connect signals
        self.line_edit.textEdited.connect(self.on_text_edited)
        self.line_edit.installEventFilter(self)
        self.list_widget.itemClicked.connect(self.on_item_clicked)

        self.is_initializing = False  # Initialization complete

    def eventFilter(self, obj, event):
        if obj == self.line_edit:
            if event.type() == QEvent.FocusIn and not self.is_initializing:
                self.filter_items(self.line_edit.text())
                if self.filtered_items:
                    self.show_popup()
                return False  # Allow normal focus behavior
            elif event.type() == QEvent.KeyPress:
                key = event.key()
                if key in (Qt.Key_Enter, Qt.Key_Return):
                    if self.list_widget.currentItem():
                        self.line_edit.setText(self.list_widget.currentItem().text())
                        self.popup.hide()
                        self.line_edit.setFocus()
                    return True
                elif key == Qt.Key_Escape:
                    self.popup.hide()
                    self.line_edit.setFocus()
                    return True
                elif key in (Qt.Key_Up, Qt.Key_Down):
                    if self.popup.isVisible():
                        self.list_widget.event(event)
                    return True
                else:
                    # Allow QLineEdit to handle text input and show popup
                    if not self.popup.isVisible() and not self.is_initializing:
                        self.show_popup()
                    return False  # Let QLineEdit process the key
        return super().eventFilter(obj, event)

    def show_popup(self):
        """Show the popup below the line edit."""
        if self.filtered_items and not self.is_initializing:
            point = self.line_edit.mapToGlobal(self.line_edit.rect().bottomLeft())
            self.popup.move(point)
            self.popup.setFixedWidth(self.line_edit.width())
            self.popup.show()

    def filter_items(self, text):
        """Filter items based on the input text."""
        self.list_widget.clear()
        if text:
            self.filtered_items = [item for item in self.all_items if text.lower() in item.lower()]
        else:
            self.filtered_items = self.all_items.copy()
        self.list_widget.addItems(self.filtered_items)
        self.list_widget.setCurrentRow(-1)  # No item selected

    def on_text_edited(self, text):
        """Handle text changes and filter the list."""
        self.filter_items(text)
        if self.filtered_items and not self.is_initializing:
            self.show_popup()
        else:
            self.popup.hide()

    def on_item_clicked(self, item):
        """Handle item selection."""
        self.line_edit.setText(item.text())
        self.popup.hide()
        self.line_edit.setFocus()

class Demo(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        items = ['Alpha', 'Beta', 'Gamma', 'Delta', 'Epsilon']
        self.combo = CustomComboBox(items)
        layout.addWidget(self.combo)
        self.setWindowTitle("Custom ComboBox Demo")

if __name__ == '__main__':
    app = QApplication([])
    w = Demo()
    w.show()
    app.exec_()    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLineEdit, QPushButton, QListWidget,
    QVBoxLayout, QHBoxLayout, QFrame
)
from PyQt5.QtCore import Qt, QPoint

class CustomComboBox(QWidget):
    def __init__(self, items, parent=None):
        super().__init__(parent)
        self.items = items

        # Main input and button layout
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.line_edit = QLineEdit(self)
        self.button = QPushButton("▼", self)
        self.button.setFixedWidth(24)
        self.button.setFocusPolicy(Qt.NoFocus)

        self.layout.addWidget(self.line_edit)
        self.layout.addWidget(self.button)

        # Popup list
        self.popup = QListWidget()
        self.popup.setWindowFlags(Qt.Popup)
        self.popup.setFocusPolicy(Qt.NoFocus)
        self.popup.setFrameStyle(QFrame.Box)
        self.popup.addItems(self.items)

        # Signals
        self.button.clicked.connect(self.toggle_popup)
        self.line_edit.textEdited.connect(self.filter_items)
        self.popup.itemClicked.connect(self.select_item)

    def toggle_popup(self):
        if self.popup.isVisible():
            self.popup.hide()
        else:
            self.show_popup()

    def show_popup(self):
        self.popup.move(self.mapToGlobal(QPoint(0, self.height())))
        self.popup.resize(self.width(), min(100, 20 * len(self.items)))
        self.popup.show()

    def filter_items(self, text):
        self.popup.clear()
        filtered = [item for item in self.items if text.lower() in item.lower()]
        self.popup.addItems(filtered)
        if filtered:
            self.show_popup()
        else:
            self.popup.hide()

    def select_item(self, item):
        self.line_edit.setText(item.text())
        self.popup.hide()

class Demo(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        items = ['Alpha', 'Beta', 'Gamma', 'Delta', 'Epsilon']
        self.combo = CustomComboBox(items)
        layout.addWidget(self.combo)

if __name__ == '__main__':
    app = QApplication([])
    w = Demo()
    w.show()
    app.exec_()    
    
    
    
    
    
    
    
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLineEdit, QPushButton, QListView,
    QVBoxLayout, QHBoxLayout, QFrame
)
from PyQt5.QtCore import Qt, QPoint, QStringListModel


class CustomComboBox(QWidget):
    def __init__(self, items, parent=None):
        super().__init__(parent)
        self.items = items
        self.model = QStringListModel(self.items)

        # Main layout
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Line edit
        self.line_edit = QLineEdit(self)
        self.layout.addWidget(self.line_edit)

        # Dropdown button
        self.button = QPushButton("▼", self)
        self.button.setFixedWidth(24)
        self.button.setFocusPolicy(Qt.NoFocus)
        self.layout.addWidget(self.button)

        # Popup frame
        self.popup = QFrame(self, Qt.Popup | Qt.FramelessWindowHint)
        self.popup.setStyleSheet("background: white; border: 1px solid #888;")
        self.popup_layout = QVBoxLayout(self.popup)
        self.popup_layout.setContentsMargins(0, 0, 0, 0)

        # Styled list view
        self.list_view = QListView(self.popup)
        self.list_view.setModel(self.model)
        self.list_view.setEditTriggers(QListView.NoEditTriggers)
        self.list_view.setSpacing(2)
        self.list_view.setStyleSheet("""
            QListView {
                padding: 4px;
                background: white;
                font-size: 14px;
            }
            QListView::item:hover {
                background: #e6f3ff;
            }
            QListView::item:selected {
                background: #cce4ff;
            }
        """)
        self.popup_layout.addWidget(self.list_view)

        # Signals
        self.button.clicked.connect(self.show_popup)
        self.line_edit.textEdited.connect(self.filter_items)
        self.list_view.clicked.connect(self.select_item)

    def show_popup(self):
        self.popup.move(self.mapToGlobal(QPoint(0, self.height())))
        self.popup.resize(self.width(), 120)
        self.popup.show()

    def filter_items(self, text):
        filtered = [item for item in self.items if text.lower() in item.lower()]
        self.model.setStringList(filtered)
        if filtered:
            self.show_popup()
        else:
            self.popup.hide()

    def select_item(self, index):
        self.line_edit.setText(self.model.data(index, Qt.DisplayRole))
        self.popup.hide()

    def keyPressEvent(self, event):
        key = event.key()
        print(key)
        if key in (Qt.Key_Up, Qt.Key_Down):
            # Shift focus to list view on arrow key press
            self.list_view.setFocus()
            self.list_view.setCurrentIndex(self.list_view.model().index(0, 0))
        else:
            self.line_edit.setFocus()
            super().keyPressEvent(event)
            


class Demo(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        items = ['Alpha', 'Beta', 'Gamma', 'Delta', 'Epsilon']
        self.combo = CustomComboBox(items)
        layout.addWidget(self.combo)

if __name__ == '__main__':
    app = QApplication([])
    w = Demo()
    w.resize(300, 100)
    w.show()
    app.exec_()
    








from PyQt5.QtWidgets import (
    QApplication, QWidget, QLineEdit, QPushButton, QListView,
    QVBoxLayout, QHBoxLayout, QFrame
)
from PyQt5.QtCore import Qt, QPoint, QStringListModel, QEvent


class CustomComboBox(QWidget):
    def __init__(self, items, parent=None):
        super().__init__(parent)
        self.items = items
        self.model = QStringListModel(self.items)

        # Main layout
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Line edit
        self.line_edit = QLineEdit(self)
        self.layout.addWidget(self.line_edit)
        self.line_edit.installEventFilter(self)  # intercept key presses

        # Dropdown button
        self.button = QPushButton("▼", self)
        self.button.setFixedWidth(24)
        self.button.setFocusPolicy(Qt.NoFocus)
        self.layout.addWidget(self.button)

        # Popup frame and list view
        self.popup = QFrame(self, Qt.Popup | Qt.FramelessWindowHint)
        self.popup.setStyleSheet("background: white; border: 1px solid #888;")
        self.popup_layout = QVBoxLayout(self.popup)
        self.popup_layout.setContentsMargins(0, 0, 0, 0)

        self.list_view = QListView(self.popup)
        self.list_view.setModel(self.model)
        self.list_view.setEditTriggers(QListView.NoEditTriggers)
        self.list_view.setSpacing(2)
        self.list_view.setStyleSheet("""
            QListView {
                padding: 4px;
                background: white;
                font-size: 14px;
            }
            QListView::item:hover {
                background: #e6f3ff;
            }
            QListView::item:selected {
                background: #cce4ff;
            }
        """)
        self.popup_layout.addWidget(self.list_view)

        # Signals
        self.button.clicked.connect(self.show_popup)
        self.line_edit.textEdited.connect(self.filter_items)
        self.list_view.clicked.connect(self.select_item)

    def show_popup(self):
        self.popup.move(self.mapToGlobal(QPoint(0, self.height())))
        self.popup.resize(self.width(), 120)
        self.popup.show()
        self.line_edit.setFocus()



    def filter_items(self, text):
        filtered = [item for item in self.items if text.lower() in item.lower()]
        self.model.setStringList(filtered)
        if filtered:
            self.show_popup()
        else:
            self.popup.hide()

    def select_item(self, index):
        self.line_edit.setText(self.model.data(index, Qt.DisplayRole))
        self.popup.hide()

    def eventFilter(self, obj, event):
        
        if obj == self.line_edit and event.type() == QEvent.KeyPress:
            print(event.key())
            key = event.key()
            if key in (Qt.Key_Up, Qt.Key_Down):
                self.list_view.setFocus()
                self.list_view.setCurrentIndex(self.model.index(0, 0))
                return True  # consume event
        return super().eventFilter(obj, event)

class Demo(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        items = ['Alpha', 'Beta', 'Gamma', 'Delta', 'Epsilon']
        self.combo = CustomComboBox(items)
        layout.addWidget(self.combo)

if __name__ == '__main__':
    app = QApplication([])
    w = Demo()
    w.resize(300, 100)
    w.show()
    app.exec_()













from PyQt5.QtWidgets import (
    QApplication, QWidget, QLineEdit, QPushButton, QListView,
    QVBoxLayout, QHBoxLayout, QFrame
)
from PyQt5.QtCore import Qt, QPoint, QStringListModel, QEvent


class CustomComboBox(QWidget):
    def __init__(self, items, parent=None):
        super().__init__(parent)
        self.items = items
        self.model = QStringListModel(self.items)

        # Main layout
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Line edit
        self.line_edit = QLineEdit(self)
        self.layout.addWidget(self.line_edit)
        self.line_edit.installEventFilter(self)

        # Dropdown button
        self.button = QPushButton("▼", self)
        self.button.setFixedWidth(24)
        self.button.setFocusPolicy(Qt.NoFocus)
        self.layout.addWidget(self.button)

        # Popup (not Qt.Popup to preserve focus behavior)
        self.popup = QFrame(None, Qt.Window | Qt.FramelessWindowHint)
        self.popup.setParent(self)
        self.popup.setStyleSheet("background: white; border: 1px solid #888;")
        self.popup.setFocusPolicy(Qt.NoFocus)

        popup_layout = QVBoxLayout(self.popup)
        popup_layout.setContentsMargins(0, 0, 0, 0)

        # List view inside popup
        self.list_view = QListView(self.popup)
        self.list_view.setModel(self.model)
        self.list_view.setEditTriggers(QListView.NoEditTriggers)
        self.list_view.setSpacing(2)
        self.list_view.setFocusPolicy(Qt.NoFocus)
        self.list_view.setStyleSheet("""
            QListView {
                padding: 4px;
                background: white;
                font-size: 14px;
            }
            QListView::item:hover {
                background: #e6f3ff;
            }
            QListView::item:selected {
                background: #cce4ff;
            }
        """)
        popup_layout.addWidget(self.list_view)

        # Signals
        self.button.clicked.connect(self.show_popup)
        self.line_edit.textEdited.connect(self.filter_items)
        self.list_view.clicked.connect(self.select_item)

    def show_popup(self):
        self.popup.move(self.mapToGlobal(QPoint(0, self.height())))
        self.popup.resize(self.width(), 120)
        self.popup.show()
        self.line_edit.setFocus()  # Retain focus explicitly

    def filter_items(self, text):
        filtered = [item for item in self.items if text.lower() in item.lower()]
        self.model.setStringList(filtered)
        if filtered:
            self.show_popup()
        else:
            self.popup.hide()

    def select_item(self, index):
        self.line_edit.setText(self.model.data(index, Qt.DisplayRole))
        self.popup.hide()

    def eventFilter(self, obj, event):
        if obj == self.line_edit and event.type() == QEvent.KeyPress:
            key = event.key()
            if key in (Qt.Key_Up, Qt.Key_Down):
                self.list_view.setFocus()
                self.list_view.setCurrentIndex(self.model.index(0, 0))
                return True
        return super().eventFilter(obj, event)


class Demo(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        items = ['Alpha', 'Beta', 'Gamma', 'Delta', 'Epsilon']
        self.combo = CustomComboBox(items)
        layout.addWidget(self.combo)


if __name__ == '__main__':
    app = QApplication([])
    w = Demo()
    w.resize(300, 100)
    w.show()
    app.exec_()






from PyQt5.QtWidgets import (
    QApplication, QWidget, QLineEdit, QPushButton, QListView,
    QVBoxLayout, QHBoxLayout, QFrame
)
from PyQt5.QtCore import Qt, QPoint, QStringListModel, QEvent


class CustomComboBox(QWidget):
    def __init__(self, items, parent=None):
        super().__init__(parent)
        self.items = items
        self.model = QStringListModel(self.items)

        # Main layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Line edit
        self.line_edit = QLineEdit(self)
        layout.addWidget(self.line_edit)
        self.line_edit.installEventFilter(self)

        # Dropdown button
        self.button = QPushButton("▼", self)
        self.button.setFixedWidth(24)
        self.button.setFocusPolicy(Qt.NoFocus)
        layout.addWidget(self.button)

        # Popup (not Qt.Popup to avoid auto-hide on focus change)
        self.popup = QFrame(None, Qt.Window | Qt.FramelessWindowHint)
        self.popup.setParent(self)
        self.popup.setStyleSheet("background: white; border: 1px solid #888;")
        self.popup.setFocusPolicy(Qt.NoFocus)
        self.popup.hide()  # 🧼 start hidden

        popup_layout = QVBoxLayout(self.popup)
        popup_layout.setContentsMargins(0, 0, 0, 0)

        # List view
        self.list_view = QListView(self.popup)
        self.list_view.setModel(self.model)
        self.list_view.setEditTriggers(QListView.NoEditTriggers)
        self.list_view.setSpacing(2)
        self.list_view.setFocusPolicy(Qt.NoFocus)
        self.list_view.setStyleSheet("""
            QListView {
                padding: 4px;
                background: white;
                font-size: 14px;
            }
            QListView::item:hover {
                background: #e6f3ff;
            }
            QListView::item:selected {
                background: #cce4ff;
            }
        """)
        popup_layout.addWidget(self.list_view)

        # Signals
        self.button.clicked.connect(self.show_popup)
        self.line_edit.textEdited.connect(self.filter_items)
        self.list_view.clicked.connect(self.select_item)

    def show_popup(self):
        self.popup.move(self.mapToGlobal(QPoint(0, self.height())))
        self.popup.resize(self.width(), 120)
        self.popup.show()
        self.line_edit.setFocus()  # 🔐 retain focus on input

def filter_items(self, text):
    filtered = [item for item in self.items if text.lower() in item.lower()]
    self.model.setStringList(filtered)

    if text.strip():  # Only show popup for non-empty input
        if filtered:
            self.popup.show()
        else:
            self.popup.hide()
    else:
        self.popup.hide()

    self.line_edit.setFocus()  # Ensure focus stays on line_edit

    def select_item(self, index):
        self.line_edit.setText(self.model.data(index, Qt.DisplayRole))
        self.popup.hide()

    def eventFilter(self, obj, event):
        if obj == self.line_edit and event.type() == QEvent.KeyPress:
            key = event.key()
            if key in (Qt.Key_Up, Qt.Key_Down):
                self.list_view.setFocus()
                self.list_view.setCurrentIndex(self.model.index(0, 0))
                return True
        return super().eventFilter(obj, event)


class Demo(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        items = ['Alpha', 'Beta', 'Gamma', 'Delta', 'Epsilon']
        self.combo = CustomComboBox(items)
        layout.addWidget(self.combo)


if __name__ == '__main__':
    app = QApplication([])
    w = Demo()
    w.resize(300, 100)
    w.show()
    app.exec_()
    
    
    
    
    
    
    
    
    
    
    
    
    
class CustomComboBox(QWidget):
    def __init__(self, items, parent=None):
        super().__init__(parent)
        # ... [setup code omitted for brevity]

        # Signals
        self.button.clicked.connect(self.show_popup)
        self.line_edit.textEdited.connect(self.filter_items)  # ✅ Uses filter_items()
        self.list_view.clicked.connect(self.select_item)

    def filter_items(self, text):  # ✅ Method must be inside the class
        filtered = [item for item in self.items if text.lower() in item.lower()]
        self.model.setStringList(filtered)

        if text.strip():
            if filtered:
                self.popup.show()
            else:
                self.popup.hide()
        else:
            self.popup.hide()

        self.line_edit.setFocus()    
    
    
    
    
    
    
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLineEdit, QPushButton, QListView,
    QVBoxLayout, QHBoxLayout, QFrame
)
from PyQt5.QtCore import Qt, QPoint, QStringListModel, QEvent


class CustomComboBox(QWidget):
    def __init__(self, items, parent=None):
        super().__init__(parent)
        self.items = items
        self.model = QStringListModel(self.items)

        # Main layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Line edit
        self.line_edit = QLineEdit(self)
        layout.addWidget(self.line_edit)
        self.line_edit.installEventFilter(self)

        # Dropdown button
        self.button = QPushButton("▼", self)
        self.button.setFixedWidth(24)
        self.button.setFocusPolicy(Qt.NoFocus)
        layout.addWidget(self.button)

        # Floating popup panel
        self.popup = QFrame(None, Qt.Window | Qt.FramelessWindowHint)
        self.popup.setParent(self)
        self.popup.setStyleSheet("background: white; border: 1px solid #888;")
        self.popup.setFocusPolicy(Qt.NoFocus)
        self.popup.hide()  # Start hidden

        popup_layout = QVBoxLayout(self.popup)
        popup_layout.setContentsMargins(0, 0, 0, 0)

        # List view inside popup
        self.list_view = QListView(self.popup)
        self.list_view.setModel(self.model)
        self.list_view.setEditTriggers(QListView.NoEditTriggers)
        self.list_view.setSpacing(2)
        self.list_view.setFocusPolicy(Qt.NoFocus)
        self.list_view.setStyleSheet("""
            QListView {
                padding: 4px;
                background: white;
                font-size: 14px;
            }
            QListView::item:hover {
                background: #e6f3ff;
            }
            QListView::item:selected {
                background: #cce4ff;
            }
        """)
        popup_layout.addWidget(self.list_view)

        # Signals
        self.button.clicked.connect(self.show_popup)
        self.line_edit.textEdited.connect(self.filter_items)
        self.list_view.clicked.connect(self.select_item)

    def show_popup(self):
        print('show popup')
        self.popup.move(self.mapToGlobal(QPoint(0, self.height())))
        self.popup.resize(self.width(), 120)
        self.popup.show()
        self.line_edit.setFocus()

    def filter_items(self, text):
        filtered = [item for item in self.items if text.lower() in item.lower()]
        self.model.setStringList(filtered)

        if text.strip() and filtered:
            self.show_popup()
        else:
            self.popup.hide()

        self.line_edit.setFocus()

    def select_item(self, index):
        self.line_edit.setText(self.model.data(index, Qt.DisplayRole))
        self.popup.hide()

    def eventFilter(self, obj, event):
        if obj == self.line_edit and event.type() == QEvent.KeyPress:
            key = event.key()
            print('keypressed', event.key())
            if key in (Qt.Key_Up, Qt.Key_Down):
                self.list_view.setFocus()
                self.list_view.setCurrentIndex(self.model.index(0, 0))
                return True
        return super().eventFilter(obj, event)


class Demo(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        items = ['Alpha', 'Beta', 'Gamma', 'Delta', 'Epsilon']
        self.combo = CustomComboBox(items)
        layout.addWidget(self.combo)


if __name__ == '__main__':
    app = QApplication([])
    w = Demo()
    w.resize(300, 100)
    w.show()
    app.exec_()    
    
