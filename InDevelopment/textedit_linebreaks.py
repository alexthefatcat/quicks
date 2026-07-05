# -*- coding: utf-8 -*-
"""Created on Sun Nov 10 16:19:39 2024@author: Alexm"""


import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtWidgets import QTextEdit, QMenu
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCursor


    
class QTextEdit_Linebreak(QTextEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.line_break_chars = {Qt.Key_Minus:'-',  Qt.Key_Equal:'='}
        self.line_break_len = 40       
    
    def keyPressEvent(self, event):
        key = event.key()
        if key in self.line_break_chars.keys() and event.modifiers() == Qt.ControlModifier:
            self.insert_text(self.line_break_chars[key] * self.line_break_len+'\n')
            return
        super().keyPressEvent(event)
        
    def insert_text(self, text):
        cursor = self.textCursor()
        cursor.insertText(text)
        self.setTextCursor(cursor)
 
 
class QTextEdit_RemoveTrailingSpaces(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

    def contextMenuEvent(self, event):
        context_menu = self.createStandardContextMenu()
        clean_action = context_menu.addAction("Clean Trailing Spaces")
        clean_action.triggered.connect(self.clean_selected_text)
        context_menu.exec_(event.globalPos())

    def clean_selected_text(self):
        cursor = self.textCursor()
        if cursor.hasSelection():
            selected_text = cursor.selectedText()
            cleaned_text = self.clean_text(selected_text)
            if False: # in future keep text selected
                cursor.beginEditBlock()
            cursor.insertText(cleaned_text)
            if False:
                cursor.insertText(cleaned_text)
                start = cursor.selectionStart()
                end = start + len(cleaned_text)
                cursor.setPosition(start)
                cursor.setPosition(end, QTextCursor.KeepAnchor)
                cursor.endEditBlock()
                self.setTextCursor(cursor)



    def clean_text(self, text):
        cleaned_lines = [line.rstrip() for line in text.splitlines()]
        cleaned_text = "\n".join(cleaned_lines)
        return cleaned_text



#%%----------------------------------------------------------------------------
   
CustomTextEdit_Classes = [QTextEdit_Linebreak, QTextEdit_RemoveTrailingSpaces]
class CustomTextEdit(*CustomTextEdit_Classes):
     def __init__(self, parent):
         super().__init__(parent=None)
    
class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.text_edit = CustomTextEdit(self)
        self.setCentralWidget(self.text_edit)
        self.setWindowTitle('Text Adder')
        self.setGeometry(100, 100, 600, 400)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MyWindow()
    main_window.show()
    sys.exit(app.exec_())







