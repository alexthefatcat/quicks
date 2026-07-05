# -*- coding: utf-8 -*-
from PyQt5 import *
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import regex as re

SET_FOCUS = False


class VisableLineEdit(QLineEdit):
   def __init__(self):
      super().__init__()
      self.hidden = False
      self.flip_visability()
      
   def flip_visability(self):
       self.hidden = not self.hidden       
       if self.hidden:
           self.hide()
       else:
           self.show()
           self.setFocus() 


class MyHighlighter(QTextEdit):
    def __init__(self, text, parent=None):
        super(MyHighlighter, self).__init__(parent)
        self.setText(text)
        self.cursor = self.textCursor()
        self.location = None 
        self.pattern = None
    
    def find_and_highlight(self, pattern, text):
        self.locs = []
        self.pattern = pattern

        for m in re.finditer(pattern, text):
            self.locs.append((m.start(0), m.end(0)))

        for loc in self.locs:        
            line_st, line_en = self.given_a_point_find_begining_and_end_of_line(text, loc[0])
            self.highlight_red(line_st, line_en, QColor(220,220,255))   
            
        for loc in self.locs:
            self.highlight_red(loc[0], loc[1], QColor(130,130,255))
            
    def given_a_point_find_begining_and_end_of_line(self, text, loc):
        texta, textb = text[:loc], text[loc:]
        v = len(texta.rsplit('\n',1)[-1])
        vv = len(texta) -v
        vvv = len(textb.split('\n',1)[0])
        vvvv = len(texta) +vvv
        return vv, vvvv
            
    def highlight_red(self, ind_start, inde_end, color='red'):
        red_format = QTextCharFormat()
        if isinstance(color,str):
            red_format.setBackground(QBrush(QColor(color)))
        else:
            red_format.setBackground(QBrush(color))            
        
        self.cursor.setPosition(ind_start)
        self.cursor.setPosition(inde_end, self.cursor.KeepAnchor)            
        self.cursor.mergeCharFormat(red_format)
    
    
    def highlight_all_white(self, color='white'):
        len_text = len(self.toPlainText())
        self.highlight_red(0, len_text, color='white')


class MainWindow(QWidget):
   def __init__(self,text):
      super().__init__()
      self.text_ui = MyHighlighter(text, pattern)
      layout = QVBoxLayout()
      self.find_bar = VisableLineEdit()
      layout.addWidget(self.text_ui)
      layout.addWidget(self.find_bar)      
      self.setLayout(layout)
      
      self.setWindowTitle("Search Bar Demo")
      self.make_connections()
      self.setGeometry(200,600,1500,900)
      self.show()

   def pressed_find(self):
       self.text_ui.highlight_all_white()
       pattern = self.find_bar.text()
       if pattern!=self.text_ui.pattern:
           self.text_ui.location = -1
       text = self.text_ui.toPlainText()
       self.text_ui.find_and_highlight(pattern, text)
       if SET_FOCUS:
           if len(self.text_ui.locs)>0:
               pos = self.text_ui.locs[0][0]
               self.text_ui.setFocus()        
               new_cursor = self.text_ui.textCursor()
               new_cursor.setPosition(pos)
               self.text_ui.setTextCursor(new_cursor)
               
       else:
            if self.text_ui.location is None:
                if len(self.text_ui.locs)>0:
                    ind_start, inde_end = self.text_ui.locs[0]
                    self.text_ui.location = 0
                    self.text_ui.highlight_red(ind_start, inde_end)
            else:
                self.text_ui.location = (self.text_ui.location+1)%(len(self.text_ui.locs))
                if len(self.text_ui.locs)>0:
                    ind_start, inde_end = self.text_ui.locs[self.text_ui.location]
                    self.text_ui.highlight_red(ind_start, inde_end)
                    self.text_ui.ensureCursorVisible()
                    
                    new_cursor = self.text_ui.textCursor()
                    new_cursor.setPosition(ind_start)
                    self.text_ui.setTextCursor(new_cursor)                    
                    self.text_ui.ensureCursorVisible()

                       
                    
                    
                    
   # def eventFilter(self, source, event):
   #      print(event.key(), event.text())
   #      if event.type() == QEvent.KeyPress:
   #              print('>>>')
   #      if source is self.find_bar:
   #              print('<<<')                
   #      if (event.type() == QEvent.KeyPress and source is self.find_bar):
   #          print('key press:', (event.key(), event.text()))
   #      return super(MainWindow, self).eventFilter(source, event)        
      
   def keyPressEvent(self, event):
        if event.key() == Qt.Key_F and event.modifiers() == Qt.ControlModifier:
            self.find_bar.flip_visability()
            self.text_ui.highlight_all_white()

   def make_connections(self):
       self.find_bar.returnPressed.connect(self.pressed_find)



text = """In this text I want to highlight this word and only this word.\n""" +\
"""Any other word shouldn't be highlighted
To search Ctrl+F


who wants to eat a ham sandwhich

thought
vader was lukes father

never never
"""*5

pattern = "word"

if __name__ == "__main__":
    import sys
    a = QApplication(sys.argv)
    a.setStyleSheet("QWidget{font-size: 10pt;}")
    window = MainWindow(text)
    sys.exit(a.exec_())    
    
    
import regex as re
[(m.start(0), m.end(0)) for m in re.finditer(pattern, text)]






		





















