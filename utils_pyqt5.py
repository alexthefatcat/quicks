# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 16:32:04 2024

@author: Alexm

Future:-
QPicture
QText with Search
QTable with advanced features


Current Classes and Functions
QVBox
QHBox
visibility_manager_dec
QPushButton_switch
"""



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

#------------------------------------------------------------------------------
# class VisibilityManagerMeta(type):
#     def __new__(cls, name, bases, attrs):
#         original_init = attrs.get('__init__', lambda self: None)

#         def __init__(self, *args, **kwargs):
#             self.is_visible = True
#             self.hide_jobs_stack = []
#             self.visible_jobs_stack = []
#             self.add_hide_job = lambda job: self.hide_jobs_stack.append(job)
#             self.add_visible_job = lambda job: self.visible_jobs_stack.append(job)
#             self.run_hide_jobs = lambda: [job() for job in self.hide_jobs_stack]
#             self.run_visible_jobs = lambda: [job() for job in self.visible_jobs_stack]

#             def hide():
#                 self.is_visible = False
#                 self.run_hide_jobs()
#                 super(self.__class__, self).hide()
#             self.hide = hide

#             def show():
#                 self.is_visible = True
#                 self.run_visible_jobs()
#                 super(self.__class__, self).show()
#             self.show = show

#             def toggle_visibility():
#                 if self.is_visible:
#                     self.hide()
#                 else:
#                     self.show()
#             self.toggle_visibility = toggle_visibility

#             original_init(self, *args, **kwargs)

#         attrs['__init__'] = __init__
#         return super().__new__(cls, name, bases, attrs)

def visibility_manager(cls):
    class Wrapped(cls):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.is_visible = True
            self.hide_jobs_stack = []
            self.visible_jobs_stack = []

        def hide(self):
            self.is_visible = False
            self.run_hide_jobs()
            super().hide()

        def show(self):
            self.is_visible = True
            self.run_visible_jobs()
            super().show()

        def toggle_visibility(self):
            if self.is_visible:
                self.hide()
            else:
                self.show()

        def run_hide_jobs(self):
            for job in self.hide_jobs_stack:
                job()

        def run_visible_jobs(self):
            for job in self.visible_jobs_stack:
                job()

        def add_hide_job(self, job):
            self.hide_jobs_stack.append(job)

        def add_visible_job(self, job):
            self.visible_jobs_stack.append(job)

    Wrapped.__name__ = cls.__name__
    Wrapped.__doc__ = cls.__doc__
    return
#------------------------------------------------------------------------------


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




