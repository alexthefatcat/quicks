# -*- coding: utf-8 -*-
'''
#Create a pyqt5_utils
QText_find

3) get multi searches dispalayed with differnt colors
4) add replace and repalce all on search box
5) create a subclass highlight so textedit.highlight.lines([45,57])
6) so the bar and the textedit link up better so theres an itnerface
7) current line is differnt color?
8) find bar ahouldnt be a global


'''

text = """{}Any other word shouldn\'t be highlighted\nTo search Ctrl+F\n\n\nwho wants to eat a ham sandwhich\n\nthought\nvader was lukes father\n\nnever never\n"""
text = ''.join(["In this text I want to highlight this word and only this word.\n", (text*15).format(*[str(e)+') =======\n' for e in range(15)])])
text2 = ''.join("Line- {:03}\n".format(e) for e in range(200))



import sys
# from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit
# from PyQt5.QtGui import QColor, QTextCursor, QTextCharFormat


from PyQt5 import *
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import regex as re

SET_FOCUS = False


def visibility_manager_dec(cls):
    class VisibilityManagerWrapper(cls):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.hidden = False
            self.__hide_jobs_stack = []
            self.__show_jobs_stack = []            
            self.toggle_visibility()
            if not hasattr(self, 'focus_widget'):
                self.focus_widget = True
            
        def toggle_visibility(self, hidden=None):
           assert hidden in (True, False, None)
           self.hidden = not self.hidden if hidden is None else hidden 
           if self.hidden:
               self.hide()
               for jobs in self.__hide_jobs_stack:
                   jobs()
           else:
               self.show()
               for jobs in self.__show_jobs_stack:
                   jobs()               
               if self.focus_widget == True:
                   self.setFocus() 
               elif self.focus_widget is None: 
                   pass
               else:
                   self.focus_widget.setFocus()
    VisibilityManagerWrapper.__name__ = cls.__name__+'__VisibilityManagerWrapper'
    VisibilityManagerWrapper.__doc__ = cls.__doc__
    return VisibilityManagerWrapper

@visibility_manager_dec
class findBar(QWidget):
    def __init__(self):
        super().__init__()
        find_bar_layout = QHBoxLayout()
        self.find_edit = QLineEdit(self)
        self.find_edit.setPlaceholderText('Find...')
        self.up_button = QPushButton('▲', self)
        self.up_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.down_button = QPushButton('▼', self)
        self.down_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.result_label = QLabel('', self)
        self.update_label(None, None)
        
        find_bar_layout.addWidget(self.find_edit)
        find_bar_layout.addWidget(self.up_button)
        find_bar_layout.addWidget(self.down_button)
        find_bar_layout.addWidget(self.result_label)

        layout = QVBoxLayout()
        layout.addLayout(find_bar_layout)
        self.setLayout(layout)
        self.focus_widget = self.find_edit      
        
    def update_label(self, location, locations):
        if locations in (None, 0) or location in (None,):
            self.result_label.setText('              ')
        else:
            self.result_label.setText(' {} out of {} '.format(location, locations))
    
    def text(self):
        return self.find_edit.text()
    @property
    def returnPressed(self, *args, **kwargs):
        return self.find_edit.returnPressed
   

#------------------------------------------------------------------------------      
VisableLineEdit = findBar        
 

class QTextEdit__Highlightable(QTextEdit):
    def __init__(self, text=None, parent=None):
        super().__init__()
        self.selections = []
        self.pattern = None
        if not text is None:
            self.setText(text)

    def highlight_lines(self, at_lines=(), at_indexs=(), color='lightgrey'):
        nblocks = self.document().blockCount()
        cursor = self.textCursor()
        for index in at_indexs:
            cursor.setPosition(index)
            at_lines = at_lines + type(at_lines)([cursor.blockNumber()])      
        cursor.movePosition(QTextCursor.Start)        
        for i in range(nblocks):
            if i in at_lines:
                cursor.movePosition(QTextCursor.StartOfBlock)
                selection = self.highlight_using_cursor(cursor, color)
                self.selections.append(selection)                
            cursor.movePosition(QTextCursor.NextBlock)

    def highlight_words(self, indexs, color):
        cursor = self.textCursor()
        for start_index, end_index in indexs:
            cursor.setPosition(start_index)
            cursor.setPosition(end_index, QTextCursor.KeepAnchor)        
            selection = self.highlight_using_cursor(cursor, color)
            self.selections.append(selection)
    
    def highlight_all(self, color='white'):
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.End, QTextCursor.KeepAnchor) 
        selection = self.highlight_using_cursor(cursor, color)
        self.setExtraSelections([selection])

    def highlight_using_cursor(self, cursor, color): 
        selection = QTextEdit.ExtraSelection()
        selection.cursor = cursor
        if not cursor.hasSelection():
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
        selection.format.setBackground(QColor(color))   
        return selection
    
    def __given_indexs_find_start_and_of_block(self, indexs):
        out = []
        cursor = self.textCursor()
        for index in indexs:
            cursor.setPosition(index)
            cursor.movePosition(QTextCursor.StartOfBlock)
            start = cursor.position()
            cursor.movePosition(QTextCursor.EndOfBlock) 
            end = cursor.position()
            out.append((start,end))
        return out
    
    def find_and_highlight(self, pattern, text, index_change=+1):
        self.selections = []       
        if self.pattern!=pattern:
            self.location = None
        
        self.locs =[ (m.start(0), m.end(0)) for m in re.finditer(pattern, text)]
        self.locations = len(self.locs)
        start_indexs = [e[0] for e in self.locs]
        
        if self.locations>0:
            self.location = 0 if self.location is None else (self.location+index_change)%(len(self.locs))
            blocks_indexs = self.__given_indexs_find_start_and_of_block([e[0] for e in self.locs])            
            
            self.highlight_lines(at_indexs=start_indexs, color='lightgreen')
            self.highlight_words(blocks_indexs, color='lightblue') 
            self.highlight_words(self.locs, color='lightyellow')  
            self.highlight_words([self.locs[self.location]], color='red') 
            
            cursor = self.textCursor()
            cursor.setPosition(self.locs[self.location][0])
            self.setTextCursor(cursor)                    
            self.ensureCursorVisible()
            self.setExtraSelections(self.selections)

        find_bar.update_label(self.location, self.locations)    
        self.pattern = pattern  
        
    
    
class MainWindow(QWidget):
   def __init__(self,text):
      super().__init__()
      self.text_ui = QTextEdit__Highlightable(text)
      layout = QVBoxLayout()
      global find_bar
      find_bar = VisableLineEdit()
      self.find_bar = find_bar
      layout.addWidget(self.text_ui)
      layout.addWidget(self.find_bar)      
      self.setLayout(layout)
      
      self.setWindowTitle("Search Bar Demo")
      self.make_connections()
      self.setGeometry(200, 600, 1500, 900)
      

   def pressed_find(self, index_change=+1):
        pattern = self.find_bar.text()
        text = self.text_ui.toPlainText()
        self.text_ui.find_and_highlight(pattern, text, index_change)

   def keyPressEvent(self, event):
        if event.key() == Qt.Key_F and event.modifiers() == Qt.ControlModifier:
            find_bar.update_label(None, None)   
            cursor = self.text_ui.textCursor()
            if cursor.hasSelection():
                text = cursor.selectedText()
                self.find_bar.toggle_visibility(hidden=False)               
                self.find_bar.find_edit.setText(text)
                self.pressed_find()
            else:
                self.find_bar.toggle_visibility()
                self.text_ui.highlight_all()

   def make_connections(self):
       self.find_bar.returnPressed.connect(self.pressed_find)
       self.find_bar.down_button.clicked.connect(lambda : self.pressed_find(+1))       
       self.find_bar.up_button.clicked.connect(lambda : self.pressed_find(-1))
       #self.text_ui.textChanged.connect(lambda : self.pressed_find(0))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet("QWidget{font-size: 10pt;}")
    window = MainWindow(text)
    window.show()
    sys.exit(app.exec_())    










#--------------------------------------------------------------------------------
assert False





























import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget
from PyQt5.QtGui import QColor, QTextCursor, QKeySequence
from PyQt5.QtCore import Qt

class CustomTextEdit(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setPlainText("Line 1\nLine 2\nLine 3\nLine 4\nLine 5\nLine 6\nLine 7\nLine 8\nLine 9\nLine 10")
        self.original_selections = []  # Store the original selections for resetting

    def highlight_block(self, index, color):
        cursor = self.textCursor()
        cursor.setPosition(index)
        cursor.select(QTextCursor.BlockUnderCursor)

        selection = QTextEdit.ExtraSelection()
        selection.cursor = cursor
        selection.format.setBackground(QColor(color))

        # Retrieve existing selections and add the new one
        selections = self.extraSelections()
        selections.append(selection)
        self.setExtraSelections(selections)
        self.original_selections = selections.copy()  # Save the selections

    def clear_highlights(self):
        # Set all previously highlighted blocks to white
        white_selections = []
        for sel in self.original_selections:
            sel.format.setBackground(QColor('white'))
            white_selections.append(sel)
        self.setExtraSelections(white_selections)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 800, 600)
        
        self.text_edit = CustomTextEdit()
        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Highlight multiple lines using setExtraSelections more than once
        self.text_edit.highlight_block(10, 'yellow')
        self.text_edit.highlight_block(30, 'lightblue')
        self.text_edit.highlight_block(50, 'lightgreen')

        # Create a shortcut for Ctrl+F to clear highlights
        self.shortcut = QKeySequence(Qt.CTRL + Qt.Key_F)
        self.text_edit.shortcut_action = self.text_edit.addAction(self.shortcut)
        self.text_edit.shortcut_action.triggered.connect(self.text_edit.clear_highlights)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())






































#-----------------------------------

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit
from PyQt5.QtGui import QColor, QTextCursor, QTextCharFormat

class CustomTextEdit(QTextEdit):
    def __init__(self):
        super().__init__()

    def highlight_lines(self, at_lines=(), at_indexs=()):
        nblocks = self.document().blockCount()
        color = QColor('lightgrey')
        cursor = self.textCursor()
        
        for index in at_indexs:
            cursor.setPosition(index)
            at_lines = at_lines + type(at_lines)([cursor.blockNumber()])      
        
        cursor.movePosition(QTextCursor.Start)        
        selections = []
        for i in range(nblocks):
            if i in at_lines:
                cursor.movePosition(QTextCursor.StartOfBlock)
                selection = QTextEdit.ExtraSelection()
                selection.cursor = cursor
                selection.format.setProperty(QTextFormat.FullWidthSelection, True)
                selection.format.setBackground(color)
                selections.append(selection)
            cursor.movePosition(QTextCursor.NextBlock)
        self.setExtraSelections(selections)
        
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 800, 600)
        self.text_edit = CustomTextEdit()
        self.setCentralWidget(self.text_edit)
        self.text_edit.setPlainText(text)
        self.text_edit.highlight_lines(at_lines=(30,), at_indexs=(113,))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())



#-----------------------------------

#modify this so both the line and the word get selected and show
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit
from PyQt5.QtGui import QColor, QTextCursor, QTextCharFormat
class CustomTextEdit(QTextEdit):
    def __init__(self):
        super().__init__()
        
    def highlight_lines(self, at_lines=(), at_indexs=()):
        nblocks = self.document().blockCount()
        color = QColor('lightgrey')
        cursor = self.textCursor() 
        for index in at_indexs:
            cursor.setPosition(index)
            at_lines = at_lines + type(at_lines)([cursor.blockNumber()])
        cursor.movePosition(QTextCursor.Start)                
        selections = []        
        for i in range(nblocks):            
            if i in at_lines:                
                cursor.movePosition(QTextCursor.EndOfBlock)                
                selection = QTextEdit.ExtraSelection()                
                selection.cursor = cursor                
                selection.format.setProperty(QTextFormat.FullWidthSelection, True)                
                selection.format.setBackground(color)                
                selections.append(selection)            
            cursor.movePosition(QTextCursor.NextBlock)        
        self.setExtraSelections(selections)        
           
class MainWindow(QMainWindow):    
    def __init__(self):        
        super().__init__()        
        self.setGeometry(100, 100, 800, 600)        
        self.text_edit = CustomTextEdit()        
        self.setCentralWidget(self.text_edit)        
        self.text_edit.setPlainText(text)        
        self.text_edit.highlight_lines(at_lines=(30,), at_indexs=(113,))                
        color_brush = QTextCharFormat()        
        color_brush.setBackground(QBrush(QColor('lightblue')))        
        self.cursor = self.text_edit.textCursor()        
        self.cursor.setPosition(84)        
        self.cursor.setPosition(88, self.cursor.KeepAnchor)                    
        self.cursor.mergeCharFormat(color_brush)        
if __name__ == '__main__':    
    app = QApplication(sys.argv)    
    window = MainWindow()    
    window.show()    
    sys.exit(app.exec_())













import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit
from PyQt5.QtGui import QColor, QTextCursor, QTextCharFormat, QBrush, QTextFormat

class CustomTextEdit(QTextEdit):
    def __init__(self):
        super().__init__()

    def highlight_lines(self, at_lines=(), at_indexs=()):
        nblocks = self.document().blockCount()
        color = QColor('lightgrey')
        cursor = self.textCursor()

        for index in at_indexs:
            cursor.setPosition(index)
            at_lines = at_lines + type(at_lines)([cursor.blockNumber()])

        cursor.movePosition(QTextCursor.Start)
        selections = []
        for i in range(nblocks):
            cursor.movePosition(QTextCursor.StartOfBlock)
            cursor.movePosition(QTextCursor.EndOfBlock, QTextCursor.KeepAnchor)
            if i in at_lines:
                selection = QTextEdit.ExtraSelection()
                selection.cursor = cursor
                selection.format.setProperty(QTextFormat.FullWidthSelection, True)
                selection.format.setBackground(color)
                selections.append(selection)
            cursor.movePosition(QTextCursor.NextBlock)

        self.setExtraSelections(selections)

    def highlight_subselection(self, start_index, end_index, color):
        cursor = self.textCursor()
        cursor.setPosition(start_index)
        cursor.setPosition(end_index, QTextCursor.KeepAnchor)
        format = QTextCharFormat()
        format.setBackground(QColor(color))
        cursor.mergeCharFormat(format)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 800, 600)
        self.text_edit = CustomTextEdit()
        self.setCentralWidget(self.text_edit)

        self.text_edit.setPlainText(text)

        # Highlight entire lines first
        #self.text_edit.highlight_lines(at_lines=(3, 6), at_indexs=(15,))
        
        # Highlight subselections
        self.text_edit.highlight_subselection(15, 17, 'lightblue')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())










                # cursor.movePosition(QTextCursor.StartOfBlock)
                # selection = QTextEdit.ExtraSelection()
                # selection.cursor = cursor
                # selection.format.setProperty(QTextFormat.FullWidthSelection, True)
                # selection.format.setBackground(color)
                # selections.append(selection)
########################################
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit
from PyQt5.QtGui import QColor, QTextCursor, QTextCharFormat, QBrush, QTextFormat

class CustomTextEdit(QTextEdit):
    def __init__(self):
        super().__init__()

    def highlight_lines(self, at_lines=(), at_indexs=()):
        nblocks = self.document().blockCount()
        color1 = QColor('lightgreen')
        color2 = QColor('lightgrey')
        self.selections = []
        cursor = self.textCursor()

        for i in range(nblocks):
            color = (color1, color2)[i%2]
            cursor.movePosition(QTextCursor.StartOfBlock)
            if True:
                #cursor.movePosition(QTextCursor.EndOfBlock, QTextCursor.KeepAnchor)
                selection = QTextEdit.ExtraSelection()
                selection.cursor = cursor
                selection.format.setProperty(QTextFormat.FullWidthSelection, True)
                selection.format.setBackground(color)
                self.selections.append(selection)
            else:
                cursor.select(QTextCursor.BlockUnderCursor)
                block_format = QTextBlockFormat()
                block_format.setBackground(QColor(color))
                cursor.setBlockFormat(block_format)
            cursor.movePosition(QTextCursor.NextBlock)
        

    def highlight_subselection(self, start_index, end_index, color):
        cursor = self.textCursor()
        cursor.setPosition(start_index)
        cursor.setPosition(end_index, QTextCursor.KeepAnchor)
        format = QTextCharFormat()
        format.setBackground(QColor(color))
        cursor.mergeCharFormat(format)
        
    def highlight_subselection2(self, start_index, end_index, color):
        cursor = self.textCursor()
        cursor.setPosition(start_index)
        cursor.setPosition(end_index, QTextCursor.KeepAnchor)
        selection = QTextEdit.ExtraSelection()
        selection.cursor = cursor
        #selection.format.setProperty(QTextFormat.FullWidthSelection, True)
        selection.format.setBackground(QColor(color))
        self.selections.append(selection)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 800, 600)
        self.text_edit = CustomTextEdit()
        self.setCentralWidget(self.text_edit)
        self.text_edit.setPlainText(text)
        self.text_edit.highlight_lines(at_lines=(3, 6), at_indexs=(15,))
        self.text_edit.highlight_subselection2(15, 17, 'lightblue')
        self.text_edit.setExtraSelections(self.text_edit.selections)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())








import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit
from PyQt5.QtGui import QColor, QTextCursor, QTextCharFormat

class CustomTextEdit(QTextEdit):
    def __init__(self):
        super().__init__()

    def highlight_lines(self, at_lines=(), at_indexs=()):
        nblocks = self.document().blockCount()
        color = QColor('lightgrey')
        cursor = self.textCursor()
        
        for index in at_indexs:
            cursor.setPosition(index)
            at_lines = at_lines + type(at_lines)([cursor.blockNumber()])      
        
        cursor.movePosition(QTextCursor.Start)        
        selections = []
        for i in range(nblocks):
            if i in at_lines:
                cursor.movePosition(QTextCursor.StartOfBlock)
                selection = QTextEdit.ExtraSelection()
                selection.cursor = cursor
                selection.format.setProperty(QTextFormat.FullWidthSelection, True)
                selection.format.setBackground(color)
                selections.append(selection)
            cursor.movePosition(QTextCursor.NextBlock)
        self.setExtraSelections(selections)
        
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 800, 600)
        self.text_edit = CustomTextEdit()
        self.setCentralWidget(self.text_edit)
        self.text_edit.setPlainText(text)
        self.text_edit.highlight_lines(at_lines=(30,), at_indexs=(113,))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())






















# import sys
# from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit
# from PyQt5.QtGui import QColor, QTextCursor, QTextCharFormat, QBrush, QTextFormat

# class CustomTextEdit(QTextEdit):
#     def __init__(self):
#         super().__init__()

#     def highlight_lines(self, at_lines=(), at_indexs=()):
#         nblocks = self.document().blockCount()
#         color = QColor('lightgrey')
#         cursor = self.textCursor()

#         for index in at_indexs:
#             cursor.setPosition(index)
#             at_lines = at_lines + type(at_lines)([cursor.blockNumber()])

#         cursor.movePosition(QTextCursor.Start)
#         for i in range(nblocks):
#             cursor.movePosition(QTextCursor.StartOfBlock)
#             if i in at_lines:
#                 cursor.movePosition(QTextCursor.EndOfBlock, QTextCursor.KeepAnchor)
#                 cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, 2)
#                 # format = QTextCharFormat()
#                 # format.setBackground(QColor('lightgrey'))
#                 # cursor.mergeCharFormat(format)
#                 selection = QTextEdit.ExtraSelection()
#                 selection.cursor = cursor
#                 selection.format.setBackground(QColor('lightgrey'))  
#                 self.setExtraSelections([selection])
#                 cursor.movePosition(QTextCursor.Left, QTextCursor.KeepAnchor, 2)   
#             cursor.movePosition(QTextCursor.NextBlock)
# cursor.select(QTextCursor.BlockUnderCursor)

#     def highlight_subselection(self, start_index, end_index, color):
#         cursor = self.textCursor()
#         cursor.setPosition(start_index)
#         cursor.setPosition(end_index, QTextCursor.KeepAnchor)
#         format = QTextCharFormat()
#         format.setBackground(QColor(color))
#         cursor.mergeCharFormat(format)

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setGeometry(100, 100, 800, 600)
#         self.text_edit = CustomTextEdit()
#         self.setCentralWidget(self.text_edit)

#         self.text_edit.setPlainText(text)

#         # Highlight entire lines first
#         self.text_edit.highlight_lines(at_lines=(3, 6), at_indexs=(15,))
        
#         # Highlight subselections
#         self.text_edit.highlight_subselection(15, 17, 'lightblue')

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec_())























#selection.format.setProperty(QTextFormat.FullWidthSelection, True)
               
# cursor.setPosition(5)
# cursor.setPosition(10, QTextCursor.KeepAnchor)
# #do stuff 1
# cursor.setPosition(6, QTextCursor.MoveAnchor)
# # do stuff 2
# cursor.setPosition(11, QTextCursor.KeepAnchor)
# # do stuff 3


# # Step 1: Select the text between the 5th and 10th characters
# cursor.setPosition(5)
# cursor.setPosition(10, QTextCursor.KeepAnchor)
# self.setTextCursor(cursor,'blue'

# # Step 2: Extend the selection to include the 11th character
# cursor.setPosition(11, QTextCursor.KeepAnchor)
# self.setTextCursor(cursor,'red')
# end_position = cursor.position()


# # Step 3: Move the anchor to the 6th character and keep the selection end at the 11th character
# cursor.setPosition(6, QTextCursor.MoveAnchor)
# self.setTextCursor(cursor,'green')
# cursor.setPosition(end_position, QTextCursor.KeepAnchor)    



# from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QRegExp
# from PyQt5.QtCore import Qt

# class CQSyntaxHighlighterSelectionMatch(QSyntaxHighlighter):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.m_strSelectionTerm = ""
#         self.m_HighlightRuleSelectionTerm = self.HighlightingRule()
#         self.m_HighlightRuleSelectionTerm.format.setBackground(QColor(255, 210, 120))

#     class HighlightingRule:
#         def __init__(self):
#             self.pattern = QRegExp()
#             self.format = QTextCharFormat()

#     def SetSelectionTerm(self, term):
#         if term == self.m_strSelectionTerm:
#             return

#         if term:
#             term = r"\b" + term + r"\b"
#             if term == self.m_strSelectionTerm:
#                 return

#         self.m_strSelectionTerm = term
#         cs = Qt.CaseSensitive
#         self.m_HighlightRuleSelectionTerm.pattern = QRegExp(self.m_strSelectionTerm, cs)
#         self.rehighlight()

#     def highlightBlock(self, text):
#         if len(self.m_strSelectionTerm) > 1:
#             self.ApplySelectionTermHighlight(text)

#     def ApplySelectionTermHighlight(self, text):
#         expression = QRegExp(self.m_HighlightRuleSelectionTerm.pattern)
#         index = expression.indexIn(text)
#         while index >= 0:
#             length = expression.matchedLength()
#             self.setFormat(index, length, self.m_HighlightRuleSelectionTerm.format)
#             index = expression.indexIn(text, index + length)


# from PyQt5.QtWidgets import QPlainTextEdit, QApplication
# from PyQt5.QtGui import QPainter, QColor
# from PyQt5.QtCore import Qt

# class TextEditor(QPlainTextEdit):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.m_uiCurrentBlock = 0
#         self.m_pHighlighter = CQSyntaxHighlighterSelectionMatch(self.document())
#         self.cursorPositionChanged.connect(self.CheckForCurrentBlockChange)
#         self.selectionChanged.connect(self.FilterSelectionForSingleWholeWord)

#     def paintEvent(self, event):
#         painter = QPainter(self.viewport())
#         rect = self.cursorRect()
#         rect.setLeft(0)
#         rect.setRight(self.width() - 1)
#         painter.setPen(Qt.NoPen)
#         painter.setBrush(QColor(228, 242, 244))
#         painter.drawRect(rect)
#         super().paintEvent(event)

#     def CheckForCurrentBlockChange(self):
#         tc = self.textCursor()
#         b = tc.blockNumber()
#         if b == self.m_uiCurrentBlock:
#             return
#         self.m_uiCurrentBlock = b
#         self.viewport().update()

#     def FilterSelectionForSingleWholeWord(self):
#         tc = self.textCursor()
#         currentSelection = tc.selectedText()
#         list = currentSelection.split(QRegExp(r"\s+"), QString.SkipEmptyParts)
#         if len(list) > 1:
#             self.m_pHighlighter.SetSelectionTerm("")
#             return
#         tc.movePosition(QTextCursor.StartOfWord)
#         tc.movePosition(QTextCursor.EndOfWord, QTextCursor.KeepAnchor)
#         word = tc.selectedText()
#         if currentSelection != word:
#             self.m_pHighlighter.SetSelectionTerm("")
#             return
#         self.m_pHighlighter.SetSelectionTerm(currentSelection)

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     editor = TextEditor()
#     editor.show()
#     sys.exit(app.exec_())
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit
from PyQt5.QtGui import QColor, QTextCursor, QTextCharFormat, QBrush, QTextFormat

class CustomTextEdit(QTextEdit):
    def __init__(self):
        super().__init__()

    def highlight_lines(self, at_lines=(), at_indexs=()):
        nblocks = self.document().blockCount()
        color1 = QColor('lightgreen')
        color2 = QColor('lightgrey')
        self.selections = []
        cursor = self.textCursor()

        for i in range(nblocks):
            color = (color1, color2)[i%2]
            cursor.movePosition(QTextCursor.StartOfBlock) # cursor.movePosition(QTextCursor.EndOfBlock, QTextCursor.KeepAnchor)
            print(cursor.hasSelection())
            selection = QTextEdit.ExtraSelection()
            selection.cursor = cursor
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.format.setBackground(color)
            self.selections.append(selection)
            cursor.movePosition(QTextCursor.NextBlock)
        
    def highlight_subselection(self, start_index, end_index, color):
        cursor = self.textCursor()
        cursor.setPosition(start_index)
        cursor.setPosition(end_index, QTextCursor.KeepAnchor)
        print(cursor.hasSelection())
        selection = QTextEdit.ExtraSelection()
        selection.cursor = cursor
        selection.format.setBackground(QColor(color))
        self.selections.append(selection)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 800, 600)
        self.text_edit = CustomTextEdit()
        self.setCentralWidget(self.text_edit)
        self.text_edit.setPlainText(text)
        self.text_edit.highlight_lines(at_lines=(3, 6), at_indexs=(15,))
        self.text_edit.highlight_subselection(15, 17, 'lightblue')
        self.text_edit.setExtraSelections(self.text_edit.selections)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

    
    
    
    


    
    
    
    
    
    
    
    
    
    