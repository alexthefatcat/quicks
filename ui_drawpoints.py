# -*- coding: utf-8 -*-
"""Created on Fri Apr 29 22:18:53 2022@author: Alexm


tidy it up code
   points shouldnt really be related to the size of the image
   points9 ? change name
   lb change this name
   change main window name
   - + to change size of image
   f - change folder ui select folder
   change it so I can have differnt points files for differnt folders
   
   
"""

from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen#, QGuiApplication

import cv2, sys, os
from get_filepath_versions import get_filepath_versions

#maybe filled red circle

def grouped(lis,n):
    return [a for a in zip( *[lis[e::n] for e in range(n)] )] 

def save_text(filename, data):   
    if type(data) is list:
       data = "\n".join(data)
    with open(filename, "w",encoding="utf-8") as fileobj:
       fileobj.write(data)
  
def load_text(filename):    
    with open(filename, "r",encoding="utf-8") as fileobj:
        print('Read in file:', filename)
        return [line.rstrip("\n") for line in fileobj.readlines()]







if True:
    fp_basic = r"C:\Users\Alexm\Desktop\PROJECTS\GUI_DRAW_POINTS\points.txt"
    #fp_basic = r"C:\Users\Alexm\Desktop\PROJECTS\GUI_DRAW_POINTS\FaceDetection_points.txt"    
    info = get_filepath_versions(fp_basic)
    fp_read = info.get('last_version', False)
    fp_save = info['next_version']
    text_filepath = fp_save
    text_filepath0 = fp_read
    del fp_read, fp_save
    
#------------------------------------------------------------------------------
folder = r"C:\Users\Alexm\Desktop\Organized Images\_FacesWomen"
#folder = r"C:\Users\Alexm\Desktop\FaceDetection"


bad_files = []#('MartinaGarcia.jpg',)
READ_POINTS_IN = True
IMAGE_HIEGHT = 1300

tooltip = '''
Contols:
    < - move left 1 image
    > - move right 1 image
    s - save points
    n - next image without points
    d - delete last point
    c - change color of points
    
Points To Label:
    Left Eye
    Right Eye
    Nose
    Middle of Lips
    Bottom of Chin
    '''.lstrip('\n')
# q red marks, coloured marks, dissapear
# d delete last point

#------------------------------------------------------------------------------ 

 
def convert_to_variabes(lis):
    txt4 = []
    for e in lis:
        e = list(e)
        e[1] = eval(e[1])
        txt4.append( tuple(e))
    return txt4  

def load_points(text_filepath0, img_files):
    txt = load_text(text_filepath0) 
    txt2 = grouped(txt,2)
    txt3 = convert_to_variabes(txt2)
    _tmp_dic = {k:v for k,v in txt3}
    if len(img_files)>0 and isinstance(img_files[0],(list, tuple)):
        img_files0 = [e[0] for e in img_files]
        points9 = [ _tmp_dic.get(f1, []) for f1 in img_files0]
    else:     
        points9 = [ _tmp_dic.get(f1, []) for f1 in img_files]
    return points9

#------------------------------------------------------------------------------ 

# red circle filled with red
ordered_colors = {0:'red',    1:'green', 2:'blue',
                  3:'magenta',4:'yellow',5:'cyan',
                  -1:'darkRed'}    


if True:
    
    def image_read(img_filepath, mode='pil', return_original=False):
        mode = mode.lower().replace(' ','')
        assert mode in ('cv2','pil')
        if   mode == 'cv2':    
            import cv2
            image_original = cv2.imread(img_filepath, 1)
            img = cv2.cvtColor(image_original, cv2.COLOR_BGR2RGB)
        elif mode == 'pil':
            from PIL import Image
            import numpy as np
            image_original = Image.open(img_filepath).convert("RGB")
            img = np.array(image_original)
        if return_original:
            return image_original
        return img  
    
    def image_resize_by_ratio(img, *, ratio=None, new_height=None, new_width=None, return_ratio=False):
        old_height, old_width, *bytesPerComponent = img.shape
        
        if ratio is not None:
            assert (new_height is None) and (new_width is None)
            new_width = round(old_width * ratio)
            new_height = round(old_height * ratio)
        else:
            assert not ((new_height is None) and (new_width is None))
            if new_height is None:
                ratio = new_width/old_width 
                new_height = round(old_height * ratio)                  
            if new_width is None:
                ratio = new_height/old_height 
                new_width = round(old_width * ratio)                  
        img = cv2.resize(img, (new_width, new_height))
        if return_ratio:
            return img, ratio
        return img       
        
    
          


def read_image(fp, hieght0=IMAGE_HIEGHT):
      '''
      function that returns an image
      '''
      img = image_read(fp)
      height_orig, width_orig, bytesPerComponent = img.shape
      ratio = 1
      if hieght0 is not None:
          img, ratio = image_resize_by_ratio(img, new_height=hieght0, return_ratio=True)
          height_new, width_new, bytesPerComponent = img.shape


      bytesPerLine = bytesPerComponent * width_new

      QImg = QImage(img.data, width_new, height_new, bytesPerLine, QImage.Format_RGB888)
      QImg.image_orig_size = (height_orig, width_orig)
      QImg.ratio = ratio
      return QImg






class DrawDots(QLabel):
    '''
    class that draws dots
    '''
    def __init__(self, points=None, orig_size=None, *args):
        super().__init__(*args)
        if points is None:
            points = []
        self.points = points
        self.dot_colors = ordered_colors
        self.RED_DOTS = True
        
    def convert_point(self, point, image_ratio=None, inverse=False):
        if image_ratio is None:
            image_ratio = self.image_ratio
        x0,y0 = point
        if not inverse:
            return (round(x0/image_ratio), round(y0/image_ratio))
        return (round(x0*image_ratio), round(y0*image_ratio))

    def mousePressEvent(self, event):
        x0 = event.x()
        y0 = event.y()
        point0 = (x0, y0)
        point = self.convert_point(point0)        
        self.points.append(point)
    
    def mouseReleaseEvent(self, event):
        x0 = event.x()
        y0 = event.y()
        point0 = (x0, y0)
        print('Released', point0)   
        
    def mouseDoubleClickEvent(self, event):
        x0 = event.x()
        y0 = event.y()
        point0 = (x0, y0)
        print('Doubleclick', point0)           
    
    def draw_colored_dot(self, point, qcolor):
        x0,y0 = point
        painter = QPainter(self)
        painter.setPen(QPen(Qt.white, 4, Qt.SolidLine))   
        painter.drawPoint(x0, y0)               
        painter.setPen(QPen(qcolor, 2, Qt.SolidLine))
        painter.drawEllipse(x0-3, y0-3, 5, 5)

    def paintEvent(self, event):
        super().paintEvent(event)
        for i,point0 in enumerate(self.points):
            if self.RED_DOTS:
                color = 'red'
            else:
                color_default = self.dot_colors[-1]
                color = self.dot_colors.get(i, color_default)
            qcolor = getattr(Qt, color)
            point = self.convert_point(point0, inverse=True)
            self.draw_colored_dot(point, qcolor)   
        self.update()

class imager(DrawDots):
   def __init__(self,*args,**kwargs):
       super().__init__(*args,**kwargs)
       
   def draw_image(self,fp, points=None):
      if points is not None:
          self.points = points     
        
      if isinstance(fp,(list,tuple)):
          fp = os.path.join(fp[1], fp[0])
      QImg = read_image(fp)
      pixmap = QPixmap.fromImage(QImg)
      self.image_ratio = QImg.ratio
      self.setPixmap(pixmap)
      self.setCursor(Qt.CrossCursor)
  
    
class DrawPointsOnImageUI(QMainWindow):
    '''
    self.pointss # is the point of everyone
    for points in pointss:
        for point in pints:
            x0,y0 = point
    '''
    def __init__(self, img_files, pointss_to_copy):
      super().__init__()
      
      self.img_files = img_files
      self.file_no = 0
      self.nfiles = len(img_files) 
      
      if len(pointss_to_copy)!=self.nfiles: 
          print('Error mismatch between image files and points')
          self.pointss = [[] for n in range(self.nfiles)]  
      else:
          #Expected
          self.pointss = [ [ee for ee in e] for e in pointss_to_copy] # deep copy

      self.setToolTip(tooltip)  
      self.setToolTipDuration(360_000)
      self.initUI()
      self.show()  
      self.setCentralWidget(self.lb)
            
    def strings_output(self):
        out = []
        img_files2 = self.img_files
        if len(img_files2)>0 and isinstance(img_files2[0], (list, tuple)):
            img_files2 = [e[0] for e in img_files2]
        for file, points in zip(img_files2, self.pointss):
            out.append(str(file)+'\n\t'+str(points))
        return out

    @property
    def get_points(self):
        return self.pointss[self.file_no]
    @property
    def get_image(self):
        return self.img_files[self.file_no]
    @property
    def get_image_ratios(self):
        return self.image_ratios[self.file_no]    
    
    @property    
    def get_title(self):
        return f'Draw Dots img no {self.file_no}/{self.nfiles}, ({self.get_image})'
    
    def draw_image(self):
        self.setWindowTitle(self.get_title)
        self.lb.draw_image(self.get_image, self.get_points)
        self.update()
        
    def initUI(self):
      self.lb = imager()
      self.draw_image()

    def keypress_change_image(self, event_key):
        #move one image left or right
        key_dic = {Qt.Key_Left:-1, Qt.Key_Right:+1, Qt.Key_Space:+1}
        value = key_dic.get(event_key, 0)
        
        #next image without points
        if event_key==Qt.Key_N:
            for i,e in enumerate(range(self.file_no, self.nfiles)):
                points =  self.pointss[e]
                if len(points)==0:
                    value = i
                    break

        # move to differnt image
        if value !=0:
            self.file_no = (self.file_no+value) % self.nfiles
            self.draw_image()         


    def keyPressEvent(self, event):
        event_key = event.key()
        
        # move to differnt image keys arrow space n
        self.keypress_change_image(event_key)

        #delete last point
        if event_key==Qt.Key_D:
            print('Deleted Point')
            if len(self.lb.points)>0:
                _ = self.lb.points.pop(-1)

        #change color of points
        if event_key==Qt.Key_C:
            self.lb.RED_DOTS = not self.lb.RED_DOTS
             
        #save
        if event_key==Qt.Key_S:
            save_text(text_filepath, self.strings_output()) 
            print('saved to:', text_filepath)
            print('Saved!')
            
#------------------------------------------------------------------------------
from PyQt5 import QtWidgets
QProxyStyle = QtWidgets.QProxyStyle
QStyle = QtWidgets.QStyle

class ProxyStyle(QProxyStyle):
    def __init__(self):
        super().__init__()

    def styleHint(self, hint, option, widget, returnData):
        dic = {QStyle.SH_ToolTip_WakeUpDelay: 6_000,
               QStyle.SH_ToolTip_FallAsleepDelay: 10_000,}
        return dic.get(hint, super().styleHint(hint, option, widget, returnData))



img_files = os.listdir(folder)
img_files = [f for f in img_files if f.endswith('.jpg') or f.endswith('.png') ]
img_files = [f for f in img_files if f not in bad_files]
img_files = [(f, folder) for f in img_files]
points9 = []
if READ_POINTS_IN:
    points9 = load_points(text_filepath0, img_files)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle(ProxyStyle())
    window = DrawPointsOnImageUI(img_files, points9)
    new_points = window.pointss
    sys.exit(app.exec_())

print('Finished!')















