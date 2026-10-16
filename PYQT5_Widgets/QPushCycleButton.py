# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 16:18:24 2026

@author: alexm
"""


from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QPushButton


class QPushCycleButton(QPushButton):
    valueChanged = pyqtSignal(object)
    stateChanged = pyqtSignal(int, str)

    def __init__(self, states, initial_index=0, parent=None):
        """states: List of labels ["A", "B"] or ("Label", value) tuples [("Hide", True), ("Show", False)].
        
        self.btn_image_visable = QPushCycleButton([("Show Image", False),("Hide Image", True)])
        self.btn_image_visable.valueChanged.connect(lambda state: self.img_widget.setVisible(state))        
        
        self.btn_image_visable.refresh() 
        self.btn_image_visable.index = 0
        
        """
        super().__init__(parent)
        self._states = [s if isinstance(s, tuple) else (str(s), s) for s in states ]
        self._index = initial_index % len(self._states)
        self.clicked.connect(self._cycle)
        self._update_display()
        
    def refresh(self):
        self._update_display()
        self.valueChanged.emit(self.value)
        self.stateChanged.emit(self._index, self.label)

    def _cycle(self):
        self._index = (self._index + 1) % len(self._states)
        self.refresh()

    def _update_display(self):
        self.setText(self.label)

    @property
    def label(self):
        return self._states[self._index][0]

    @property
    def value(self):
        return self._states[self._index][1]

    @property
    def index(self):
        return self._index
    
    @index.setter
    def index(self, value):
        """Sets the active state index, updates button text, and emits signals."""
        if not isinstance(value, int):
            raise TypeError("Index must be an integer")
        new_index = value % len(self._states)
    
        if self._index != new_index:
            self._index = new_index
            self.refresh()