 

text = """{}Any other word shouldn\'t be highlighted\nTo search Ctrl+F\n\n\nwho wants to eat a ham sandwhich\n\nthought\nvader was lukes father\n\nnever never\neverton\n34342\n"""
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
   



#useful decortaot class
def add_ignore_missing_methods(cls):
    original_getattr = getattr(cls, '__getattr__', None)
    
    def __getattr__(self, name):
        if original_getattr:
            try:
                return original_getattr(self, name)
            except AttributeError:
                pass
        def method_missing(*args, **kwargs):
            print(f"Ignoring non-existent method call: {name}")
        return method_missing
    
    cls.__getattr__ = __getattr__
    return cls



assert False

@add_ignore_missing_methods
class findBar2(QWidget):
    def __init__(self):
        super().__init__()
        find_bar_layout = QHBoxLayout()
        self.find_edit = QLineEdit(self)
        self.find_edit.setPlaceholderText('Find...')
        self.up_button = QPushButton('▲', self)
        self.down_button = QPushButton('▼', self)
        self.result_label = QLabel('', self)
        self.result_label.setText('              ')
        
        find_bar_layout.addWidget(self.find_edit)
        find_bar_layout.addWidget(self.up_button)
        find_bar_layout.addWidget(self.down_button)
        find_bar_layout.addWidget(self.result_label)

        layout = QVBoxLayout()
        layout.addLayout(find_bar_layout)
        self.setLayout(layout)
        self.focus_widget = self.find_edit      

    def text(self):
        return self.find_edit.text()
    
    @property
    def returnPressed(self, *args, **kwargs):
        return self.find_edit.returnPressed
    
    # def __getattr__(self, name):
    #     def method_missing(*args, **kwargs):
    #         print(f"Ignoring non-existent method call: {name}")
    #     return method_missing



#------------------------------------------------------------------------------      
VisableLineEdit = findBar2        
 

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


@add_ignore_missing_methods
class QTextEdit__Highlightable(QTextEdit):
    def __init__(self, text=None, parent=None):
        super().__init__()
        self.selections = []
        self.pattern = None
        if not text is None:
            self.setText(text)

        

class QTextEdit__WithFindBar(QWidget):
    def __init__(self, text=None, parent=None):
        super().__init__()
        layout = QVBoxLayout()
        self.text_ui = QTextEdit__Highlightable(text, parent)
        global find_bar
        find_bar = VisableLineEdit()
        self.find_bar = find_bar
        layout.addWidget(self.text_ui)
        layout.addWidget(self.find_bar)      
        self.setLayout(layout)            
        self.make_connections()    
        
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



class MainWindow(QMainWindow): 
   def __init__(self, text=None):
      super().__init__()
      self.setWindowTitle("Search Bar Demo")
      self.setCentralWidget(QTextEdit__WithFindBar(text))
      self.setGeometry(200, 600, 1500, 900)
      
#------------------------------------------------------------------------------

if False:
    #if __name__ == "__main__":    
        Widget = (MainWindow, QTextEdit__WithFindBar, QTextEdit__Highlightable)[0]
        app = QApplication(sys.argv)
        app.setStyleSheet("QWidget{font-size: 9pt;}")    
        window = Widget(text)
        window.show()
        sys.exit(app.exec_())     
    
#------------------------------------------------------------------------------
# so try not to change the above
















@add_ignore_missing_methods
class findBar2(QWidget):
    def __init__(self):
        super().__init__()
        find_bar_layout = QHBoxLayout()
        self.find_edit = QLineEdit(self)
        self.find_edit.setPlaceholderText('Find...')
        self.up_button = QPushButton('▲', self)
        self.down_button = QPushButton('▼', self)
        self.result_label = QLabel('', self)
        self.result_label.setText('              ')
        find_bar_layout.addWidget(self.find_edit)
        find_bar_layout.addWidget(self.up_button)
        find_bar_layout.addWidget(self.down_button)
        find_bar_layout.addWidget(self.result_label)
        layout = QVBoxLayout()
        layout.addLayout(find_bar_layout)
        self.setLayout(layout)
        self.focus_widget = self.find_edit      
@add_ignore_missing_methods
class QTextEdit__Highlightable(QTextEdit):
    def __init__(self, text=None, parent=None):
        super().__init__()
        self.selections = []
        self.pattern = None
        if not text is None:
            self.setText(text)
class QTextEdit__WithFindBar(QWidget):
    def __init__(self, text=None, parent=None):
        super().__init__()
        layout = QVBoxLayout()
        self.text_ui = QTextEdit__Highlightable(text, parent)
        find_bar = VisableLineEdit()
        self.find_bar = find_bar
        layout.addWidget(self.text_ui)
        layout.addWidget(self.find_bar)      
        self.setLayout(layout)   
 






import sys
from PyQt5.QtWidgets import QApplication, QStyle, QWidget, QHBoxLayout, QTextEdit, QScrollBar, QFrame, QStyleOptionSlider
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QColor

text = ''.join([f"{i:03d} | This is some initial text in the QTextEdit.\n" for i in range(166)])
lines = [0,20,110,165]

DEBUG = False





WIDGET = (QWidget, QTextEdit__Highlightable, QTextEdit__WithFindBar)[2]
TEXTEDIT = (lambda : QTextEdit(), lambda : QTextEdit__Highlightable(text))[1]
print(str(WIDGET).split('.')[-1].split("'")[0])



class CustomTextEdit(WIDGET):
    def __init__(self, text):
        import inspect
        init_signature = inspect.signature(WIDGET.__init__)
        if 'text' in list(init_signature.parameters.keys()):
            super().__init__(text)            
        else:
            super().__init__()
        self.initUI(text)

    def initUI(self, text):
        self.layout = QHBoxLayout()
        self.layout.setSpacing(0)  

        if hasattr(self, 'text_ui' ):
            print('using parent')
            self.textEdit = self.text_ui 
        else:
            self.textEdit = TEXTEDIT()
            self.textEdit.setPlainText(text)  # Add initial text 
            
        if hasattr(self, 'find_bar' ):
            self.find_bar.toggle_visibility(hidden=False)  
        
        self.textEdit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        if not DEBUG:
            self.textEdit.verticalScrollBar().valueChanged.connect(self.updateExternalScroll)
            self.textEdit.textChanged.connect(self.updateScrollBarHeight)  # Connect textChanged signal

        # Create a frame for the grey bar
        self.greyBar = QFrame() if DEBUG else self.CustomQFrame()
        self.greyBar.setStyleSheet("background-color: lightgrey; min-width: 15px;")

        # Create the vertical scrollbar
        self.scrollBar = QScrollBar()
        self.scrollBar.setOrientation(Qt.Vertical)
        if not DEBUG:
            self.scrollBar.valueChanged.connect(self.syncScroll)
        
        style = self.scrollBar.style()
        option = QStyleOptionSlider()
        self.scrollBar.initStyleOption(option)
        sub_control_up = style.subControlRect(QStyle.CC_ScrollBar, option, QStyle.SC_ScrollBarSubLine, self.scrollBar)
        sub_control_down = style.subControlRect(QStyle.CC_ScrollBar, option, QStyle.SC_ScrollBarAddLine, self.scrollBar)
        self.greyBar.top_gap = sub_control_up.height()
        self.greyBar.bot_gap = sub_control_down.height()

    
        # Add widgets to the layout
        self.layout.addWidget(self.textEdit)
        self.layout.addWidget(self.greyBar)        
        self.layout.addWidget(self.scrollBar)

        # Set layout to the main widget
        self.setLayout(self.layout)
        if not DEBUG:
            self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("Custom QTextEdit with Grey Bar")
        
        # Update the scrollbar height based on the total number of lines
        if not DEBUG:
            QTimer.singleShot(100, self.updateScrollBarHeight)  # Delay to ensure text is rendered
            self.greyBar.updateSearchPositions(lines)

    def syncScroll(self, value):
        mvalue1, mvalue2 = self.textEdit.verticalScrollBar().maximum(), self.scrollBar.maximum()
        #print(mvalue1, mavalue2)
        value0 = 1+(value*mvalue1)//mvalue2
        print(value, value0, 'syncScroll', 124)
        self.textEdit.verticalScrollBar().setValue(value0)
        self.greyBar.updateSearchPositions(lines)
        
    def updateExternalScroll(self, value):
        mvalue1, mvalue2 = self.textEdit.verticalScrollBar().maximum(), self.scrollBar.maximum()
        #print(mvalue1, mavalue2)
        value0 = (value*mvalue2)//mvalue1
        print(value, 'updateExternalScroll',1613)
        self.scrollBar.setValue(value0)

    def updateScrollBarHeight(self):
        total_lines = self.textEdit.document().blockCount()
        visible_lines = self.textEdit.viewport().height() // self.textEdit.fontMetrics().lineSpacing()

        # Adjust the maximum value and page step of the scrollbar
        self.scrollBar.setMaximum(total_lines - visible_lines)
        self.scrollBar.setPageStep(visible_lines)

        # Align the external scrollbar with the internal scrollbar value
        self.scrollBar.setValue(self.textEdit.verticalScrollBar().value())

    def move_to_line(self, line_number):
        total_lines = self.textEdit.document().blockCount()
        if total_lines == 0:  # Avoid division by zero
            return
    
        # Calculate the scroll position
        scroll_pos = (line_number / total_lines) * self.textEdit.verticalScrollBar().maximum()
        self.textEdit.verticalScrollBar().setValue(int(scroll_pos))

    class CustomQFrame(QFrame):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.maximum = 162 #  get the number of lines??
            self.search_positions = []
            self.top_gap = 0
            self.bot_gap = 0
    
        def paintEvent(self, event):
            super().paintEvent(event)
            painter = QPainter(self)
            painter.setPen(QColor('orange'))
            painter.setBrush(QColor('orange'))
            rect_height = int(self.height()/self.maximum)
    
            self.height2 = self.height() -self.top_gap -self.bot_gap-16
            
            for pos in self.search_positions:
                y = int((pos / self.maximum) * self.height2)+self.top_gap
                painter.drawRect(0, y, self.width(), rect_height)
            painter.end()
    
        def updateSearchPositions(self, positions):
            self.search_positions = positions
            self.update()  
            
        def mousePressEvent(self, event):
            y = event.pos().y()
            scroll_pos = int((y - self.top_gap) / self.height2 * self.maximum)
            self.parentWidget().move_to_line(scroll_pos)
        
     



if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet("QWidget{font-size: 10pt;}")
    window = CustomTextEdit(text)
    window.show()
    sys.exit(app.exec_())

 


'''





'''

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel


class BaseWidget(QPushButton):
    def __init__(self):
        super().__init__()
        global p
        p = self.layout
        print(p(),)
        print(hasattr(self,'layout'))
        
        # Initialize layout
        self.layout = QVBoxLayout(self)
        
        # Add two widgets
        self.label = QLabel("This is a label", self)
        self.button = QPushButton("This is a button", self)
        
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.button)
        
        self.setLayout(self.layout)

class ExtendedWidget(BaseWidget):
    def __init__(self):
        super().__init__()
        
        # Add additional widgets at the bottom
        self.additional_label = QLabel("This is an additional label", self)
        self.additional_button = QPushButton("This is an additional button", self)
        
        layout = QVBoxLayout()
        layout.addWidget(self.additional_label)
        layout.addWidget(self.additional_button)
        self.setLayout(layout)        

# class BaseWidget(QWidget):
#     def __init__(self):
#         super().__init__()
#         global p
#         p = self.layout
#         print(p(),)
#         print(hasattr(self,'layout'))
        
#         # Initialize layout
#         self.layout = QVBoxLayout(self)
        
#         # Add two widgets
#         self.label = QLabel("This is a label", self)
#         self.button = QPushButton("This is a button", self)
        
#         self.layout.addWidget(self.label)
#         self.layout.addWidget(self.button)
        
#         self.setLayout(self.layout)

# class ExtendedWidget(BaseWidget):
#     def __init__(self):
#         super().__init__()
        
#         # Add additional widgets at the bottom
#         self.additional_label = QLabel("This is an additional label", self)
#         self.additional_button = QPushButton("This is an additional button", self)
        
#         self.layout.addWidget(self.additional_label)
#         self.layout.addWidget(self.additional_button)


from PyQt5.QtWidgets import QApplication

def main():
    app = QApplication([])
    window = ExtendedWidget()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()







##>>>

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QTextEdit
from PyQt5.QtWidgets import QApplication

class QTextEdit2(QTextEdit):
    def __init__(self):
        super().__init__()

class ExtendedWidget(QTextEdit2):
    def __init__(self):
        super().__init__()
        self.additional_label = QLabel("Label-A", self)
        self.additional_button = QPushButton("Button-B", self)
        #layout = self.layout
        layout = QVBoxLayout()
        layout.addWidget(self.additional_label)
        layout.addWidget(self.additional_button)
        #self.setLayout(layout)  
        
        p = QWidget()
        p.setLayout(layout) 
        pp = QVBoxLayout()
        pp.addWidget(p)
        self.setLayout(pp)  
              

def main():
    app = QApplication([])
    window = ExtendedWidget()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()









import sys
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QPushButton, QLabel, QTextEdit, QWidget
from PyQt5.QtCore import Qt

class QTextEdit2(QTextEdit):
    def __init__(self):
        super().__init__()

class ExtendedWidget(QTextEdit2):
    def __init__(self):
        super().__init__()

        # Create a container widget to hold the QTextEdit and other widgets
        container = QWidget(self)
        layout = QVBoxLayout()
        
        # Create the additional widgets
        self.additional_label = QLabel("Label-A", self)
        self.additional_button = QPushButton("Button-B", self)
        
        # Add widgets to the layout
        #layout.addWidget(self)
        layout.addWidget(self.additional_label)
        layout.addWidget(self.additional_button)
        
        # Set the layout for the container
        container.setLayout(layout)
        self.removeLayout()
        self.setLayout(layout)
    
    def removeLayout(self):
        # while self.layout.count():
        #     child = self.layout.takeAt(0)
        #     if child.widget():
        #         child.widget().deleteLater()
        #self.layout.deleteLater()
        self.layout = None
        self.adjustSize()


def main():
    app = QApplication([])
    window = ExtendedWidget()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()













import sys
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QPushButton, QLabel, QTextEdit, QWidget
from PyQt5.QtCore import Qt

class QTextEdit2(QTextEdit, QWidget, QPushButton):
    def __init__(self):
        super().__init__()

class ExtendedWidget(QTextEdit2):
    def __init__(self):
        super().__init__()

        # Create a container widget to hold the QTextEdit and other widgets
        container = QWidget(self)
        layout = QVBoxLayout()
        
        # Create the additional widgets
        self.additional_label = QLabel("Label-A", self)
        self.additional_button = QPushButton("Button-B", self)
        
        # Add widgets to the layout
        #layout.addWidget(self)
        layout.addWidget(self.additional_label)
        layout.addWidget(self.additional_button)
        
        # Set the layout for the container
        container.setLayout(layout)
        self.removeLayout()
        self.setLayout(layout)
    
    def removeLayout(self):
        # while self.layout.count():
        #     child = self.layout.takeAt(0)
        #     if child.widget():
        #         child.widget().deleteLater()
        #self.layout.deleteLater()
        self.layout = None
        self.adjustSize()


def main():
    app = QApplication([])
    window = ExtendedWidget()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()












from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        # Create a layout
        self.layout = QVBoxLayout(self)
        
        # Add some widgets to the layout
        self.layout.addWidget(QLabel("Label 1", self))
        self.layout.addWidget(QPushButton("Button 1", self))
        self.layout.addWidget(QLabel("Label 2", self))
        self.layout.addWidget(QPushButton("Button 2", self))

    def get_all_widgets(self):
        widgets = []
        for i in range(self.layout.count()):
            item = self.layout.itemAt(i)
            widget = item.widget()
            if widget is not None:
                widgets.append(widget)
        return widgets

# Example usage
if __name__ == '__main__':
    app = QApplication([])
    my_widget = MyWidget()
    my_widget.show()
    
    # Get all widgets in the layout
    all_widgets = my_widget.get_all_widgets()
    for w in all_widgets:
        print(w.text())  # Assuming widgets have text() method like QLabel and QPushButton
    
    app.exec_()



self = my_widget

widgets = [self.layout.itemAt(i).widget() for i in range(self.layout.count())]






d = QTextEdit()
dd = d.layout()
print(dd)










#------------------------------------------------------------------------------



var =222

# Unchanagable Class
class A:
    def __init__(self):
        print('aa')
        self.val = 45
    def p(self):
        print('ppp')
    

def wrap(A):
    class B(A):
        def __init__(self):
            self.__name__ = A.__name__+'__Wrapped'
            self.__wrap__ = A() # instead use super
        def __getattr__(self, name):
            return getattr(self.__wrap__, name)    
    return B
B = wrap(A) # avoid super


# Code 
class C(B):
    def __init__(self):
        super().__init__()

c = C()
print(isinstance(c, A))

c.p()
c.val


#------------------------------------------------------------------------------






















QTextEdit2 = QTextEdit

class QTextEdit2(QTextEdit):
    def __init__(self):
        #super().__init__()
        QWidget.__init__(self)
        self.wrapped = True
        self.__name__ = QTextEdit.__name__+'__Wrapped'
        self.__wrap__ = QTextEdit() # instead use super
    def __getattr__(self, name):
        return getattr(self.__wrap__, name)    


class ExtendedWidget(QTextEdit2):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.additional_label = QLabel("Label-A")
        self.additional_button = QPushButton("Button-B")
        layout.addWidget(self.additional_label)
        layout.addWidget(self.additional_button)
        self.setLayout(layout)



def main():
    app = QApplication([])
    window = ExtendedWidget()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()









#------------------------------------------------------------------------------

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QPushButton, QLabel, QTextEdit, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeyEvent


class QTextEditBase(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__()        
        self.textedit = self.QTextEdit()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.textedit)
        self.setLayout(self.layout)
        
    def __getattr__(self, name):
        return getattr(self.textedit, name)    

    class QTextEdit(QTextEdit):
        def __init__(self):
            print('QTextEdit- ran inside function')
            super().__init__()            

#------------------------------------------------------------------------------
            
class CustomTextEdit1(QTextEditBase):
    def __init__(self):
        super().__init__()

    class QTextEdit(QTextEditBase.QTextEdit):
        def __init__(self):
            print('testn')
            super().__init__()   
 
        def keyPressEvent(self, event):
            if event.key() == Qt.Key_Tab:
                cursor = self.textCursor()
                cursor.insertText("   ")  # Insert three spaces
                print('Pressed Tab')
            else:
                super().keyPressEvent(event)            

class CustomTextEdit2(QTextEditBase):
     def __init__(self):
         super().__init__()

     class QTextEdit(QTextEditBase.QTextEdit):
         def __init__(self):
             print('testn')
             super().__init__()   
  
         def keyPressEvent(self, event):
             if event.key() == Qt.Key_Space:
                 cursor = self.textCursor()
                 cursor.insertText("-SpaceBar-")  # Insert three spaces
                 print('pressed space bar')
             else:
                 super().keyPressEvent(event)            

class CustomTextEdit2(QTextEditBase):
     def __init__(self):
         super().__init__()

     class QTextEdit(QTextEditBase.QTextEdit):
         def __init__(self):
             print('testn')
             super().__init__()   
  
         def keyPressEvent(self, event):
             if event.key() == Qt.Key_Space:
                 cursor = self.textCursor()
                 cursor.insertText("-SpaceBar-")  # Insert three spaces
                 print('pressed space bar')
             else:
                 super().keyPressEvent(event)            
  
class CustomTextEdit3(QTextEditBase):
       def __init__(self):
           super().__init__()
           print('Dog')
           
 
    
#------------------------------------------------------------------------------

QTextEditPlus_classes = (CustomTextEdit1, CustomTextEdit2, CustomTextEdit3)

class QTextEditPlus(*QTextEditPlus_classes):
    def __init__(self, *args, **kwargs):
        super().__init__()
        
    class QTextEdit(*[e.QTextEdit for e in QTextEditPlus_classes]):
         def __init__(self):
             super().__init__()

central_widget = QTextEditPlus()

#------------------------------------------------------------------------------

class MainWindow(QMainWindow):
    def __init__(self, central_widget):
        super().__init__()
        self.setWindowTitle("-Main Window-")
        self.setCentralWidget(central_widget)
        

if __name__ == '__main__':
    app = QApplication([])  #sys.argv
    main_window = MainWindow(central_widget)
    main_window.show()
    sys.exit(app.exec_())

#------------------------------------------------------------------------------







# Get all subclasses of QTextEditBase
subclasses = get_subclasses(QTextEditBase)
print("Subclasses of QTextEditBase:", subclasses)

# To further find subclasses within CustomTextEdit1
subclasses_custom1 = get_subclasses(CustomTextEdit1.QTextEdit)
print("Subclasses of CustomTextEdit1.QTextEdit:", subclasses_custom1)


def get_subclasses(cls):
    subclasses = cls.__subclasses__()
    subclass_dict = {subclass.__name__: subclass for subclass in subclasses}
    return subclass_dict

get_subclasses(CustomTextEdit1)

QTextEditPlus_classes = (CustomTextEdit1, CustomTextEdit2, CustomTextEdit3)


import inspect
cls = CustomTextEdit1
inner_classes = [name for name, obj in inspect.getmembers(cls) if inspect.isclass(obj) and obj.__module__ == cls.__module__]

class QTextEditPlus(*QTextEditPlus_classes):
    def __init__(self, *args, **kwargs):
        for inner_class in inner_classes:
            class Foo(*[getattr(e,inner_class ) for e in QTextEditPlus_classes]):
                def 
        super().__init__()
        
    class QTextEdit(*[e.QTextEdit for e in QTextEditPlus_classes]):
         def __init__(self):
             super().__init__()

central_widget = QTextEditPlus()
QTextEditBase.__subclasses__()








class Foo1:
    def __init__(self):
        print('foo1')

class Foo2:
    def __init__(self):
        print('foo2')

class Foo(Foo1, Foo2):
    def __init__(self):
        super().__init__()

foo = Foo()



class Foo1:
    def __init__(self):
        print('foo1')

class Foo2:
    def __init__(self):
        print('foo2')

class Foo(Foo1, Foo2):
    def __init__(self):
        #pass
        #super().__init__()
        super(Foo1, self).__init__()
        #super(Foo2, self).__init__()

foo = Foo()
dp = Foo1()








class Base:
    def __init__(self):
        print('Foo')


class Foo1(Base):
    def __init__(self):
        super().__init__()        
        print('foo1')
        self.a = 3

class Foo2(Base):
    def __init__(self):
        print('foo2')
        super().__init__()
        self.b =5
    # def m(self):
    #     return self.a * self.b

class Foo(Foo1, Foo2):
    def __init__(self):
        super().__init__()



foo = Foo()
foo.m()








class Base:
    class Inner:
        def __init__(self):
            self.n = 1
            print('Base Inner')
    
    def __init__(self):
        self.inner = self.Inner()

class A(Base):
    class Inner(Base.Inner):
        def __init__(self):
            super().__init__()
            self.n = self.n+10
            print('A Inner')            
    
    def __init__(self):
        super().__init__()
        self.inner = self.Inner()

class B(Base):
    class Inner(Base.Inner):
        def __init__(self):
            super().__init__()
            self.n = self.n +1000
            print('B Inner') 
    
    def __init__(self):
        super().__init__()
        self.inner = self.Inner()

class C(A, B):
    def __init__(self):
        super().__init__()
        print("C initialized")

# Instantiate C
c = C()
c.inner.n #  i wnat this to be 1011





class Base:
    class Inner:
        def __init__(self):
            self.n = 1
            print('Base Inner')
    
    def __init__(self):
        self.inner = self.Inner()

class A(Base):
    class Inner(Base.Inner):
        def __init__(self):
            super().__init__()
            self.n = self.n + 10
            print('A Inner')            
    
    def __init__(self):
        super().__init__()
        self.inner = self.Inner()

class B(Base):
    class Inner(Base.Inner):
        def __init__(self):
            super().__init__()
            self.n = self.n + 1000
            print('B Inner') 
    
    def __init__(self):
        super().__init__()
        self.inner = self.Inner()

class C(A, B):
    class Inner(A.Inner, B.Inner):
        def __init__(self):
            super().__init__()
            print('C Inner')
    
    def __init__(self):
        super().__init__()
        self.inner = self.Inner()
        print("C initialized")

# Instantiate C
c = C()
print(c.inner.n) # Should print 1011





def get_inner_class_names(cls):
    import inspect
    inner_classes = []
    for name, obj in inspect.getmembers(cls):
        if inspect.isclass(obj) and obj.__module__ == cls.__module__:
            inner_classes.append(name)
    return inner_classes

def get_base_class_names(cls):
    base_names = set()
    def _get_base_names(cls):
        for base in cls.__bases__:
            if base.__name__ not in base_names:
                base_names.add(base.__name__)
                _get_base_names(base)
    _get_base_names(cls)
    return base_names


class C(A, B):
    class Inner(A.Inner, B.Inner):
        def __init__(self):
            super().__init__()
            print('C Inner')
    
    def __init__(self):
        inner_classes = get_inner_class_names(C)
        for inner_class in inner_classes:
            foo_classes = (getattr(c, inner_classes) for c in get_base_class_names(C))
            class foo(*foo_classes):
                def __init__(self):
                    super().__init__()
            setattr(self, inner_class, foo)
        super().__init__()
        self.inner = self.Inner()
        print("C initialized")


c = C()
print(c.inner.n) # Should print 1011




#------------------------------------------------------------------------------


def print_rgb(text, rgb=(255,0,0)):
    rgb0 = ';'+(';'.join([str(e) for e in rgb]))+'m'
    rgb_foreground = '38;2' 
    text2 = ''.join(['\033[', rgb_foreground,rgb0, text,'\033[0m'])
    print(text2)

print_rgb('blue',(135,135,255))











class Base:
    class Inner:
        def __init__(self):
            self.n = 1
            self.base = True
            print('Base Inner')
    
    def __init__(self):
        print('-Base init')
        self.inner = self.Inner()

class A(Base):
    class Inner(Base.Inner):
        def __init__(self):
            super().__init__()
            self.base = False
            self.n = self.n + 10
            print('A Inner')            
    
    def __init__(self):
        print('-A init')        
        super().__init__()
        self.inner = self.Inner()

class B(Base):
    class Inner(Base.Inner):
        def __init__(self):
            super().__init__()
            self.base = False
            self.n = self.n + 1000
            print('B Inner') 
    
    def __init__(self):
        print('-B init')   
        super().__init__()
        self.inner = self.Inner()


import inspect
def get_inner_class_names(cls):
    inner_classes = []
    for name, obj in inspect.getmembers(cls):
        if inspect.isclass(obj) and obj.__module__ == cls.__module__:
            inner_classes.append(name)
    return inner_classes

def get_direct_base_classes(cls):
    return list(cls.__bases__)


if False:
    class C(A, B):
        class Inner(A.Inner, B.Inner):
            def __init__(self):
                super().__init__()
                print('C Inner')
        
        def __init__(self):
            super().__init__()
else:
    class C(A, B):
        def __init__(self):
            inner_class_names = get_inner_class_names(C)
            bases0 = get_direct_base_classes(C)
            for inner_class_name in inner_class_names:
                bases = [b for b in bases0 if hasattr(b, inner_class_name)]
                inner_classes_inherit = [getattr(e, inner_class_name) for e in bases ]
                class temp(*inner_classes_inherit):
                    def __init__(self):
                        super().__init__()
                        print('C Inner')          
                setattr(self, inner_class_name, temp)
            super().__init__()           
            
c = C()
print(c.inner.n)  # Should print 1011

# maybe the base clas








