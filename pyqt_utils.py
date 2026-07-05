
'''
Maybe add one where you can add multiple widgets easilt

'''



import sys
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QWidget, QComboBox, QLabel, QPushButton
from PyQt5.QtWidgets import  QGroupBox, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt, QEvent



class QMainWindow_Debug(QMainWindow):
    """
    if press the key d and hover over the tooltip set by self.tooltip_debug is shown
    its not dynamic yet
    if you set a self.tooltip_debug
    
    """
    def __init__(self):
        self.debug_mode_state = False
        super().__init__()
        self.tooltip_debug = None

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_D and self.isActiveWindow():
            self.debug_mode()
        super().keyPressEvent(event)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key.Key_D:
            self.debug_mode()  # Call debug_mode from base class
        if event.type() == QEvent.ToolTip:
            pass
            #print(f"hxfhfxhgf")            
        return super().eventFilter(obj, event)

    def debug_mode(self):
        self.debug_mode_state = not self.debug_mode_state
        if not self.tooltip_debug is None:
            if self.debug_mode_state:
                self.tooltip_original = self.toolTip()
                tooltip = self.tooltip_debug
            else:
                tooltip = self.tooltip_original
            self.setToolTip(tooltip) 
                
            print('D_> Pressed', self.debug_mode_state)
            





if True:
    #older
    class QMainWindowScreenCorrected(QMainWindow):
        def __init__(self,*args,**kwargs):
            super().__init__(*args,**kwargs)
            self._get_screen_size()
            self.prepare_for_screen()
            
        def _get_screen_size(self):
            from win32api import GetSystemMetrics
            self.screen_info = (GetSystemMetrics(0), GetSystemMetrics(1))        
            self.screen_width = GetSystemMetrics(0)
            self.screen_hieght = GetSystemMetrics(1)        
            moniter_types = {(3440, 1440):'ultrawide', (3840, 2400):'XPS-13inchScreen'}
            self.screen_type = moniter_types.get(self.screen_info, 'unknown')
            
        def prepare_for_screen(self):
            # Handle high resolution displays:
            # if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
            #     app.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
                
            # if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
            #     app.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
            if self.screen_type=='ultrawide':
                self.setStyleSheet("QWidget{font-size:12px;}")
            else:
                self.setStyleSheet("QWidget{font-size:31px;}")    
    
    #newer
    class QMainWindow_FontCorrection(QMainWindow):
        def __init__(self, font_px = 12, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self._get_screen_size()
            self.prepare_for_screen(font_px=font_px)
    
        def _get_screen_size(self):
            screen = QGuiApplication.primaryScreen()
            geometry = screen.geometry()
            self.screen_width = geometry.width()
            self.screen_height = geometry.height()
            self.screen_info = (self.screen_width, self.screen_height)
            self.screen_dpi = round(screen.physicalDotsPerInch(),1)
    
        def prepare_for_screen(self, font_px = 12):
            dpi = self.screen_dpi
            mm_in_inch = 25.4
            size_mm = (font_px/dpi)*mm_in_inch
            size_mm_corrected = max(size_mm, 2.8)
            font_px_corrected = int(size_mm_corrected*(dpi/mm_in_inch))
            self.setStyleSheet(f"QWidget {{ font-size:{font_px_corrected}px; }}")
    
    
    
    








#import sys
#from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QComboBox, QLabel
class QSelectorWidget(QWidget):
    def __init__(self, data, funcConstructWidget=None):
        super().__init__()
        self.data = data
        self.funcConstructWidget = self.default_funcConstructWidget if funcConstructWidget is None else funcConstructWidget
        self.layout = QVBoxLayout(self)
        self.combo = self.createOptions() 
        self.view = QWidget()
        self.view.setLayout(QVBoxLayout())
        self.layout.addWidget(self.combo)
        self.layout.addWidget(self.view)  
        self.updateView()
        
    def createOptions(self, options=None):
        if options is None:
            options = self.data
        if isinstance(options, dict):
            options = list(options.keys())
        self.options = options            
        combo = QComboBox()
        for option in options:
            combo.addItem(option)
        combo.currentIndexChanged.connect(self.updateView)
        return combo        

    def updateView(self, text=None): 
        layout = self.view.layout()
        if layout.count()>0:
            widget = layout.itemAt(0).widget()
            layout.removeWidget(widget)
            widget.deleteLater() 
        newWidget = self.createSwapableWidget(text)
        layout.insertWidget(0, newWidget)
        self.update()

    def createSwapableWidget(self, text=None):
        key = self.combo.currentText()
        text = self.data[key]
        return self.funcConstructWidget(key, text)
    
    @staticmethod
    def default_funcConstructWidget(key, value):
        return  QLabel(str(key)+':-\n\n\t'+str(value))




class MainWindow(QMainWindow_FontCorrection):
    def __init__(self, centralwidget, icon=None, title=None, size=None):
        super().__init__()
        if title is not None:
            self.setWindowTitle(title)
        if icon is not None:
            self.setWindowIcon(icon)
        if size is not None:
            current_size = self.size()
            width = size[0] if size[0] is not None else current_size.width()
            height = size[1] if size[1] is not None else current_size.height()
            self.resize(width, height)
        self.setCentralWidget(centralwidget)


class QVBoxWidgets(QWidget):
    def __init__(self, widgets=None, vertical=True, spacing=6, margins=9):
        super().__init__()
        self.widgets = widgets
        self.vertical = vertical
        self.spacing = spacing
        self.margins = margins
        
        if vertical:
            self.layout = QVBoxLayout()
        else:
            self.layout = QHBoxLayout()
        if widgets is not None:
            if isinstance(widgets,dict):
                widgets_new = []
                for k,v in widgets.items():
                    group_box = QGroupBox(k)
                    group_box.setContentsMargins(margins,margins,margins,margins)
                    group_layout = QVBoxLayout()
                    group_layout.addWidget(v)
                    group_box.setLayout(group_layout)
                    widgets_new.append(group_box)
                widgets = widgets_new
                    
            for i,widget in enumerate(widgets):
                self.layout.addWidget(widget)
        self.layout.setContentsMargins(margins,margins,margins,margins)
        self.layout.setSpacing(spacing)
        self.setLayout(self.layout)
        
    def addWidget(self, widget):
        self.layout.addWidget(widget)
    # def __call__(self, obj):
    #     if isinstance(obj, QVBoxWidgets):
    #         self.setLayout(obj.layout)





if False:
   data = {"Option 1":'11111111', "Option 2":'2222222', "Option 3":'33333333333'}



   if __name__ == '__main__':
       app = QApplication(sys.argv)
       centralwidget = QSelectorWidget(data, None)
       window = MainWindow(centralwidget, title='Combobox example')
       window.show()
       sys.exit(app.exec_())

if False:
    
    

    

    if __name__ == "__main__":
        app = QApplication(sys.argv)
        centralwidget = QVBoxWidgets([QPushButton(f"Button {i}") for i in range(1, 6)])
        window = MainWindow(centralwidget, title='Buttons')
        window.show()
        sys.exit(app.exec_())
        
