
import sys
from PyQt5.QtWidgets import QApplication, QStyle, QWidget, QHBoxLayout, QTextEdit, QScrollBar, QFrame, QStyleOptionSlider
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QColor

text = ''.join([f"{i:03d} | This is some initial text in the QTextEdit.\n" for i in range(166)])
lines = [0,20,110,165]


class CustomQFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.maximum = 162
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
    
    



class CustomTextEdit(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.layout = QHBoxLayout()
        self.layout.setSpacing(0)

        self.textEdit = QTextEdit()
        self.textEdit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textEdit.setPlainText(text)  # Add initial text
        self.textEdit.verticalScrollBar().valueChanged.connect(self.updateExternalScroll)
        self.textEdit.textChanged.connect(self.updateScrollBarHeight)  # Connect textChanged signal

        # Create a frame for the grey bar
        self.greyBar = CustomQFrame()
        self.greyBar.setStyleSheet("background-color: lightgrey; min-width: 15px;")

        # Create the vertical scrollbar
        self.scrollBar = QScrollBar()
        self.scrollBar.setOrientation(Qt.Vertical)
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

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("Custom QTextEdit with Grey Bar")
        
        # Update the scrollbar height based on the total number of lines
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CustomTextEdit()
    window.show()
    sys.exit(app.exec_())



if False: 

    
    import random
    
    def random_bin(n):
        out = random.randint(1, n) == 1
        return out
    
    # Example usage:
    print(random_bin(6))
    
    for n in range(100_000):
        assert not random_bin(234), f'Random crash {n}'
 




 







 