# -*- coding: utf-8 -*-
"""Created on Wed Sep 18 15:18:19 2024@author: Alexm"""

#from video_player__temp_qpicture import QPictureBase2 as QPicture

import numpy as np
import sys, os

from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QLabel, QPushButton, QProgressBar
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, Qt, QEvent
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtGui import QFont, QIntValidator
from PyQt5.QtWidgets import QLineEdit, QLabel, QHBoxLayout, QVBoxLayout, QPushButton


def changed():
    if False:
        print('changed')

'''


Works Well 
Future Additions
   1)  create a ui exe one?
     **QPicture
   2)  get QPicture to deal with black and white images and floats
    **Extra Info
   5)  titles?
   6)  can but second argument in with same length as images and the info will be displyed over image
   7)  if list contains two images so both images side by side 
   9)  name of variable in the name of the title    
    **Others
   3)  mseconds best what happens if i want to pause an exact amount over iteration
   4)  3d volumes it can deal with 
   8)  show stats of the variable
   11) when hovering value of pixel as well as max min in image as well as image volume
   12) prograss bar differnt from 100 
   13) I think it will try to resize it image is differnt size ie has been stretchced
    
video_play(images)  
    
'''



import sys
import numpy as np

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtWidgets import QPushButton, QLineEdit, QHBoxLayout, QVBoxLayout,  QScrollArea, QLabel, QMenu
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QPixmap, QPainter, QBrush, QPen, QImage, QColor, QResizeEvent
from PyQt5.QtCore import Qt, QSize, QPoint, QSize, QEvent, QTimer


def save_images(frames, filename='output.mp4', framerate=20.0, color_correction_cv = True):
    import cv2
    import numpy as np
    assert isinstance(frames, (list, tuple))
    for i,frame in enumerate(frames):
        if i==0:
            screen_size = frame.shape[1::-1]
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for MP4
            out = cv2.VideoWriter(filename, fourcc, framerate, screen_size)
        if color_correction_cv:
            frame = frame[:,:,(2,1,0)]
        assert frame.dtype == np.uint8
        out.write(frame)
    out.release()
    print('Saved images as:- '+filename)

                




class QPictureBase2(QWidget):
    def __init__(self, image_data):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.scroll_area = self.QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setContentsMargins(0, 0, 0, 0)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Hide horizontal scrollbar
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)    # Hide vertical scrollbar
        self.layout.addWidget(self.scroll_area)      
        self.update(image_data)

    def resizeEvent(self, event):
        size = (event.size().width()-2, event.size().height()-2)  
        self.scaled_pixmap = self.pixmap.scaled(*size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.label.setPixmap(self.scaled_pixmap)
        changed()
        self.current_size = size
        
    #        self.widget_image.update(image, update_label=True,reset_widget_size=False) 
    def update(self, image_data=None, reset_widget_size=True, update_label=False):
        if image_data is not None:
            self.image_data = image_data
        qimage = QImage(self.image_data.astype(np.uint8), self.image_data.shape[1], self.image_data.shape[0], QImage.Format_RGB888)
        self.pixmap = QPixmap.fromImage(qimage)
        if not update_label:
            self.label = self.QLabel(self)         
            self.label.setPixmap(self.pixmap)
        else:
            changed()
            if hasattr(self, 'current_size'):
                self.scaled_pixmap = self.pixmap.scaled(*self.current_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.label.setPixmap(self.scaled_pixmap)
            else:              
                self.label.setPixmap(self.pixmap)                
            
        if not update_label:
            self.label.setAlignment(Qt.AlignCenter)
            self.scroll_area.setWidget(self.label)
        if reset_widget_size:
            size_image = self.size_image    
            self.setFixedSize(size_image[0]+2, size_image[1]+2)
            def reset_to_minimum():
                self.setMinimumSize(1,1)
                self.setMaximumSize(10_000,10_000)            
            QTimer.singleShot(10, reset_to_minimum)

    @property
    def size_image(self):
        height, width, *clr = self.image_data.shape
        return width, height   

    class QScrollArea(QScrollArea):
        def __init__(self, parent=None):
            super().__init__()
            self.parent = parent
    class QLabel(QLabel):
        def __init__(self, parent=None):
            super().__init__()
            self.parent = parent
    
    #make prettier
    def position_to_pixel(self, x, y):
        label_width = self.label.width()
        label_height = self.label.height()
        pixmap_width = self.label.pixmap().width()
        pixmap_height = self.label.pixmap().height()
        x_offset = (label_width - pixmap_width) // 2
        y_offset = (label_height - pixmap_height) // 2  
        scale_width = self.size_image[0]/pixmap_width
        scale_hieght = self.size_image[1]/pixmap_height
        pixel_x = int(scale_width*(x-x_offset))
        pixel_y = int(scale_hieght*(y-y_offset))
        inside_image = (-1<pixel_x<self.size_image[0]) and (-1<pixel_y<self.size_image[1])
        return pixel_x, pixel_y, inside_image

    def pixel_to_position(self, pixel_x, pixel_y):
        label_width = self.label.width()
        label_height = self.label.height()
        pixmap_width = self.label.pixmap().width()
        pixmap_height = self.label.pixmap().height()
        x_offset = (label_width - pixmap_width) // 2
        y_offset = (label_height - pixmap_height) // 2  
        scale_width = pixmap_width / self.size_image[0]
        scale_height = pixmap_height / self.size_image[1]
        x = pixel_x * scale_width + x_offset
        y = pixel_y *scale_height + y_offset
        return int(x), int(y)

QPicture = QPictureBase2



class QVBox(QWidget):
    def __init__(self, *args):
        super().__init__()
        vbox = QVBoxLayout()
        for arg in args:
            vbox.addWidget(arg)
        self.setLayout(vbox)
        
class QHBox(QWidget):
    def __init__(self, *args):
        super().__init__()
        hbox = QHBoxLayout()
        for arg in args:
            hbox.addWidget(arg)
        self.setLayout(hbox)

class Worker(QThread):
    update = pyqtSignal(int)

    def __init__(self, parent):
        super().__init__()
        self._is_running = True 

    def run(self):
        count = 0
        while self._is_running:
            self.msleep(100)
            count += 1
            self.update.emit(count)

    def stop(self):
        self._is_running = False


class QPushButton_switch(QtWidgets.QPushButton):
    def __init__(self, modes=None, index=0):
        super().__init__()        
        if modes is None:
            standardIcons = [ QtWidgets.QStyle.SP_MediaPlay,
                              QtWidgets.QStyle.SP_MediaPause,]  
            icons = [ self.style().standardIcon(standardIcon) for standardIcon in standardIcons ]   
            modes = icons

        self.modes = modes
        self.nmodes = len(modes)
        self.index = index
        self.refresh_button()
        self.clicked.connect(self.on_click)
        
    def change(self, value=1):
        self.index = (self.index +value) % self.nmodes
            
    def refresh_button(self):
        self.setIcon(self.modes[self.index])
            
    def on_click(self):
        self.change()
        self.refresh_button()         




def read_images_in_folder(folder, size = (300, 400), filelimit=300):
    import numpy as np
    import os
    
    def imshow(image, title=''):
        import matplotlib.pyplot as plt
        plt.imshow(image, cmap='gray')
        plt.title(title)
        plt.axis('off')  # Hide axes
        plt.show()
        
    def resize_with_padding(image_path, target_width, target_height):
        from PIL import Image, ImageOps
        image = Image.open(image_path)
        image.thumbnail((target_width, target_height), Image.LANCZOS)
        new_image = Image.new("RGB", (target_width, target_height), (0, 0, 0))
        paste_position = ((target_width - image.width) // 2, (target_height - image.height) // 2)
        new_image.paste(image, paste_position)
        image_array = np.array(new_image)
        return image_array    
        
    filepaths = os.listdir(folder)
    filepaths = [os.path.join(folder, f) for f in filepaths]
    filepaths = [f for f in filepaths if ('.jpg' in f) or ('.png' in f)]   
    if filelimit is not None:
        filepaths = filepaths[:filelimit]
    images0 = [resize_with_padding(filepath,  size[0], size[1]) for filepath in filepaths]
    images0 = np.stack(images0, -1)
    return images0
    

# Most of the above should be imported
#------------------------------------------------------------------------------

class QSliceToolbar(QWidget):
    def __init__(self, nslices=100):
        super().__init__()
        button_width = 32
        font = QFont('Arial', 14) 
        
        self.prev_btn = QtWidgets.QPushButton('<')#◀<
        self.play_btn = QPushButton_switch()
        self.next_btn = QtWidgets.QPushButton('>')#▶>

        self.prev_btn.setFixedWidth(button_width)
        self.play_btn.setFixedWidth(button_width)
        self.next_btn.setFixedWidth(button_width)
        self.prev_btn.setFixedHeight(button_width)
        self.play_btn.setFixedHeight(button_width)
        self.next_btn.setFixedHeight(button_width)            
        play_buttons = QHBox(self.prev_btn, self.play_btn, self.next_btn)

        self.textbox = QLineEdit()
        self.textbox.setValidator(QIntValidator(0, nslices))
        self.label = QLabel(' '.join(['/', str(nslices)]))
        self.textbox.setFixedHeight(button_width-2)
        self.label.setFixedHeight(button_width-2)
        label_width = int(1.5*self.label.sizeHint().width())
        self.textbox.setFixedWidth(label_width)
        self.textbox.setFont(font)
        self.label.setFont(font)         
        
        
        self.save_btn = QPushButton('Save') 
        self.save_btn.setFont(font)
        self.save_btn.adjustSize()  
        self.save_btn.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)        
        
        self.loop_btn = QPushButton('Loop')
        self.loop_btn.setCheckable(True)  
        self.loop_btn.setFont(font)
        self.loop_btn.adjustSize()
        self.loop_btn.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        
        slice_info = QHBox(self.textbox, self.label, self.save_btn, self.loop_btn)

        self.progress = QProgressBar(self)
        self.progress.setFixedHeight(17)        
        #self.progress.setGeometry(50, 50, 500, 4)
        
        self.progress.setStyleSheet("QProgressBar::chunk { background-color: lightblue; }")
        
        self.prev_btn.setFocusPolicy(Qt.ClickFocus)
        self.next_btn.setFocusPolicy(Qt.ClickFocus)
        self.play_btn.setFocusPolicy(Qt.ClickFocus)       
        self.save_btn.setFocusPolicy(Qt.ClickFocus)        
        self.loop_btn.setFocusPolicy(Qt.ClickFocus)       
        
        row2 = QHBox(play_buttons, slice_info)
        layout = QVBoxLayout()
        layout.addWidget(self.progress)
        layout.addWidget(row2)            
        self.setLayout(layout)                  
        
   

    


class MainWindow_PlayVideo(QMainWindow):
    update = pyqtSignal(int)
    def __init__(self, data, index=0):
        super().__init__()
        self.setWindowTitle("QuickImage PlayVideo")
        self.index = index
        self.images = self.read_data(data)
        self.nimages = len(self.images)
        #.setFocus() .setFocus() 
        self.widget_image =  QPicture(self.current_image())
        self.toolbar = QSliceToolbar(self.nimages)
        
        self.central_widget = QtWidgets.QWidget()          
        lay = QtWidgets.QVBoxLayout(self.central_widget)
        lay.addWidget(self.widget_image)

        lay.addWidget(self.toolbar)        
        self.setCentralWidget(self.central_widget)       
  
        self.toolbar.textbox.returnPressed.connect(self.validate_input)
  
        self.toolbar.prev_btn.clicked.connect(self.dec_focus_label(self.on_click1))
        self.toolbar.play_btn.clicked.connect(self.dec_focus_label(self.on_click2))
        self.toolbar.next_btn.clicked.connect(self.dec_focus_label(self.on_click3))
        self.toolbar.save_btn.clicked.connect(self.dec_focus_label(self.on_click_save))        
        
        self.toolbar.progress.mousePressEvent = self.jump_slice
        
        self.worker = Worker(self)
        self.worker.update.connect(self.update_label)
        self.index_changed()
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.StrongFocus)
        self.widget_image.setFocus()
        self.installEventFilter(self)
    
    def dec_focus_label(self, method):
        def wrapper():
            out = method()
            self.widget_image.setFocus()    
            return out
        return wrapper

    def index_changed(self, new_index=None, add=0):
        if new_index is None:
            new_index = self.index
        new_index = new_index + add     
        if new_index<0:
            if self.looping:
                new_index = new_index%self.nimages
            else:
                if add==-1:
                    new_index = self.index
        if new_index>=(self.nimages):
            if self.looping:
                new_index = new_index%self.nimages
            else:            
                if add==+1:
                    new_index = self.index 
                    if self.worker._is_running:
                        self.toolbar.play_btn.click()
             
        self.index = new_index
        image = self.current_image()
        self.widget_image.update(image, update_label=True, reset_widget_size=False) 
        self.toolbar.textbox.setText(str(new_index))
        pvalue = int(100*self.index/self.nimages)
        self.toolbar.progress.setValue(pvalue)

    @property
    def looping(self):
        return self.toolbar.loop_btn.isChecked()        
        
    def current_image(self):
        image = self.images[self.index]
        if len(image.shape) ==2:
            iamge3 = np.stack([image,image,image],2)*255
        else:
            iamge3 = image           
        iamge4 = np.array(iamge3, dtype='uint8')
        return iamge4 
    
    @pyqtSlot(int)
    def update_label(self, value):
        self.index_changed(add=+1)        

    def on_click3(self):
        self.index_changed(add=+1)
        
    def on_click1(self):
        self.index_changed(add=-1)     

    def on_click2(self):
        if self.toolbar.play_btn.index==1:
            if not self.worker.isRunning():
                self.worker = Worker(self)
                self.worker.update.connect(self.update_label)
                self.worker.start()    
        else:
            self.worker.stop()    
    
    def on_click_save(self):
        options = QFileDialog.Options()
        #options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "Save File", "untitled.mp4", "MP4 Files (*.mp4)", options=options)       
        try:
            save_images(self.images, filename=fileName)
        except ModuleNotFoundError:
            print('Please install the cv2 module to save')
            
    def validate_input(self):
        text = self.toolbar.textbox.text()
        if text.isdigit() and 0 <= int(text) <= self.nimages:
            self.index_changed(int(text))
        else:
            self.textbox.undo()

    def jump_slice(self, event):
        if event.button() == Qt.LeftButton:
            pos = event.pos().x()
            value = int((pos / self.toolbar.progress.width()) * 100)
            index = int((pos / self.toolbar.progress.width()) * self.nimages)                
            self.index_changed(index)
              
    def eventFilter(self, source, event):    
        if event.type() == QEvent.KeyPress:# and self.underMouse():
            if event.key() == Qt.Key_Left:
                self.index_changed(add=-1)     
            if event.key() == Qt.Key_Right:
                self.index_changed(add=+1)  
            if event.key() == Qt.Key_Space:
               self.toolbar.play_btn.click()
        return super().eventFilter(source, event)
    
    def closeEvent(self, event):
        self.worker.terminate()  # Stop the thread
        self.worker.wait()       # Wait for the thread to finish
        event.accept()           # Accept the close event


    def read_data(self, data):
        def anyin(cont1, cont2):
            return any([e in cont2 for e in cont1])
        
        if   isinstance(data, (list, tuple, dict)):
            data0 = data
        elif isinstance(data, np.ndarray):
            shape = data.shape
            assert len(shape) in (3,4)
            if len(shape) == 4:
                data0 = list(np.moveaxis(data,-1,0))
            else:
                for dim in (2,3):
                    if shape[dim] in (3,4):
                        break
                else:
                    assert False
                if dim==2:
                    data0 = list(np.moveaxis(data,-1,0))
                else:
                    data0 = list(np.moveaxis(data,-2,0))
        elif isinstance(data, str):
            if os.path.isdir(data):
                data0 = self.read_data(read_images_in_folder(data))
        else:
            assert False
            
            
        assert data0[0].dtype == 'uint8'
        return data0
    
    
    
    




def videoplayer(images0, return_frames=False):
    app = QApplication(sys.argv)
    window = MainWindow_PlayVideo(images0)
    frames1 = window.images
    window.show()  
    sys.exit(app.exec_())
    if return_frames:
        return frames1













if __name__ == '__main__':
    def find_first_working_filepath(filepaths):
        for filepath in filepaths:
            if os.path.exists(filepath):
                return filepath    
    
    filepaths = (r'C:\Users\Alexm\Desktop\Organized Images\_FacesWomen\_New',)   
    filepath = find_first_working_filepath(filepaths)
    if filepath is not None:
        app = QApplication(sys.argv)
        window = MainWindow_PlayVideo(filepath)
        frames = window.images
        window.show()  
        sys.exit(app.exec_())
    else:
        def create_some_images_to_play():
            import numpy as np
            images = [np.zeros([500,500]) for n in range(135)]
            for i in range(len(images)):
                img = images[i]
                ii = i*3
                img[(0+ii):(10+ii),0:10] = 1
                img[(460-ii):(490-ii),400:420] = 1 
                inds = list(range((460-ii),(490-ii),2))
                for ind in inds:
                    img[400:420, ind] = 1 
                img[240:260,:] = 1
                img[:,248:252,] = 1    
                images[i] = img
                
            images[0][::5,] = 1
            images[-1][::8,] = 1    
            return images  
        
        images0 = create_some_images_to_play()
        videoplayer(images0)    
    



if False:
    #Below is an attempt to only load fist image and neiboring images so
    # its quickere to work at first
    thread_1 = False

    
    
    
    class Cache(dict):
        def __init__(self, *args, limit, **kwargs):
            super().__init__(*args, **kwargs)
            self.limit = limit
            self.keys_order = []
        def __setitem__(self, key, value):
            if key in self.keys_order:          
                self.refresh(key)
            else:
                if len(self)>self.limit:
                    first_key = self.keys_order.pop(0)
                    self.pop(first_key)
                self.keys_order.append(key)        
            super().__setitem__(key, value)
            
        def refresh(self, key):
            self.keys_order.remove(key)
            self.keys_order.append(key)  
            
        def __contains__(self, key):
            out = super().__contains__(key)  
            if out:
                self.refresh(key)
            return out
        
        def __getitem__(self, key, *args):
            self.refresh(key)
            return super().__getitem__(key, *args)
    
    
    
    
    folder= 'folder_boom'
        
    def get_filepaths(folder):
        return [f'filename_bob_{i+1}' for i in range(345)]
    
    
    def dynamic_load(filename):
        print(filename)
        return filename+'data'
    
    class DynamicLoader:
        def __init__(self, folder=folder, i=0):
            self.filepaths = get_filepaths(folder)
            self.length = len(self.filepaths)
            self.cache = Cache(13)
    
        def neigbouring_indexs(self, index, nfiles, nniegbours=8):
            out = []
            for n in range(0, (nniegbours//2)):
                out.append((index+n)%nfiles)
                out.append((index-n)%nfiles)
            out = out[1:] 
            return out
    
        def new_slice(self, ii):
            if ii not in self.cache:
                filename = self.filepaths[ii]
                data = dynamic_load(filename)
                self.cache[filename] = data
            
    
        
        def __getitem__(self, index):
            neigbouring_indexs = self.neigbouring_indexs(index, self.length, nniegbours=8)#[0,1,-1,2,-1]
            for nindex in neigbouring_indexs:
                self.new_slice(nindex) # loads data in the cache sp background after first thread        
                if nindex == index:
                    if thread_1:
                        return self.cache[index] # you want it to do this first
            for nindex in neigbouring_indexs[::-1]:
                self.cache.refresh(nindex)      
            
        
        
        
        
        
            
    ind= 45
    
    dynamicLoader = DynamicLoader()  
    
    
    list(dynamicLoader.cache.keys())
    dynamicLoader[8]
    
    
    
    dynamicLoader.cache
    
    
        
    











