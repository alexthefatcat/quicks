# -*- coding: utf-8 -*-
"""Created on Fri Oct  2 18:48:28 2026@author: alexm"""


from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QGridLayout


class QBox_Widget:

    @staticmethod
    def _create_box(layout_type, *widgets) -> QWidget:
        container = QWidget()
        layout = layout_type(container)
        for w in widgets:
            if w is not None:
                layout.addWidget(w)
        return container

    @staticmethod
    def H(*widgets) -> QWidget:
        return QBox_Widget._create_box(QHBoxLayout, *[w for w in widgets if w is not None])

    @staticmethod
    def V(*widgets) -> QWidget:
        return QBox_Widget._create_box(QVBoxLayout, *[w for w in widgets if w is not None])

    @staticmethod
    def Grid(matrix: list[list]) -> QWidget:
        """
        Accepts a 2D list of widgets representing rows and columns.
        Use `None` for empty cells.
        Use `(widget, rowSpan, colSpan)` to span across multiple cells.
        """
        container = QWidget()
        layout = QGridLayout(container)

        for row_idx, row in enumerate(matrix):
            for col_idx, item in enumerate(row):
                if item is None:
                    continue

                if isinstance(item, tuple):
                    # Tuple format: (widget, row_span, col_span)
                    widget, row_span, col_span = item
                    layout.addWidget(widget, row_idx, col_idx, row_span, col_span)
                else:
                    layout.addWidget(item, row_idx, col_idx)

        return container