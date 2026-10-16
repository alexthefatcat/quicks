# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 16:20:12 2026

@author: alexm
"""



from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSizePolicy



from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QSize



class ImageWidget(QWidget):

    def __init__(self, img_fp=None, parent=None, size=(1000, 700)):
        super().__init__(parent)

        # Store target size and calculate fixed aspect ratio (width / height)
        self._target_size = QSize(*size)
        self._aspect_ratio = (
            size[0] / size[1] if size[1] > 0 else 1.0
        )

        # Allow vertical expansion while keeping horizontal policy constrained
        self.setSizePolicy(
            QSizePolicy.Preferred, QSizePolicy.Expanding
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("background-color: white;")

        # Ignore pixmap size hints to prevent new images from triggering layout resizes
        self.label.setSizePolicy(
            QSizePolicy.Ignored, QSizePolicy.Ignored
        )

        layout.addWidget(self.label)

        self._original_pixmap = None
        self.set_image(img_fp)

    def sizeHint(self):
        return self._target_size

    def set_image(self, img_fp):
        """Loads image or clears display without triggering a widget resize."""
        if img_fp:
            pixmap = QPixmap(img_fp)
            self._original_pixmap = (
                pixmap if not pixmap.isNull() else None
            )
        else:
            self._original_pixmap = None

        self._update_display()

    def _update_display(self):
        """Scales image to current label bounds while preserving aspect ratio."""
        if (
            self._original_pixmap
            and not self.label.size().isEmpty()
        ):
            scaled_pixmap = self._original_pixmap.scaled(
                self.label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation,
            )
            self.label.setPixmap(scaled_pixmap)
        else:
            self.label.clear()

    def resizeEvent(self, event):
        """Recalculates fixed width from current height to lock aspect ratio on vertical resizes."""
        super().resizeEvent(event)

        current_height = self.height()
        if current_height > 0:
            target_width = int(
                current_height * self._aspect_ratio
            )
            # Only update width if it differs from aspect-ratio target to avoid layout loops
            if self.width() != target_width:
                self.setFixedWidth(target_width)

        self._update_display()







