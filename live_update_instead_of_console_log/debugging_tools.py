# -*- coding: utf-8 -*-
"""Created on Thu Jun 26 02:43:24 2025@author: Alexm"""
# debugging_tools.py

# debugging_tools.py

import sys
import threading
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem
from PyQt5.QtCore import QTimer, Qt

_app = QApplication.instance() or QApplication(sys.argv)

class LiveVariableOutput(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Live Variable Output")
        self.setGeometry(550, 100, 400, 300)

        layout = QVBoxLayout()
        self.label = QLabel("Streaming Values")
        self.log = QListWidget()
        layout.addWidget(self.label)
        layout.addWidget(self.log)
        self.setLayout(layout)

        # Refresh window manually to avoid freezing
        self.repaint_timer = QTimer()
        self.repaint_timer.timeout.connect(self.repaint)
        self.repaint_timer.start(100)

    def insert(self, val):
        self.log.addItem(QListWidgetItem(str(val)))
        self.log.scrollToBottom()

def _keep_ui_alive():
    _app.exec_()

def live_variable_outputs():
    if not hasattr(_app, '_loop_thread'):
        thread = threading.Thread(target=_keep_ui_alive, daemon=True)
        _app._loop_thread = thread
        thread.start()

    window = LiveVariableOutput()
    window.show()
    return window