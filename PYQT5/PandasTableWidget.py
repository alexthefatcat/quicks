
'''





QPandasTableWidget(QAbstractTableModel)

QPandasTableWidget







+-------------------------------------------------------+
|                       THE DATA                        |
|   (Your raw Python lists, dictionaries, database,     |
|             or a Pandas DataFrame)                    |
+-------------------------------------------------------+
                           ^
                           | Read / Write
                           v
+-------------------------------------------------------+
|                      THE MODEL                        |
|   (The Translator / Brain: QAbstractTableModel)      |
|  - Knows the total row and column counts              |
|  - Fetches data points dynamically when asked         |
+-------------------------------------------------------+
                           ^
                           | "Hey, what goes in Row 2, Col 1?"
                           v
+-------------------------------------------------------+
|                      THE VIEW                         |
|             (The Window: QTableView)                  |
|  - A dumb grid layout on the screen                   |
|  - Only renders what is visible to the user           |
+-------------------------------------------------------+



So Im attempg to create a class called  QPandasTableWidget
I want it to adventually have filtering so it should go this route
I want it to have a subclass QPandasTableModel which is the default model
the class should have two properties .df and .df_view

so dont creat


pandaswidget = QPandasTableWidget(df)

so dont write any code yet what do you think of this


'''





#==============================================================================
# 


import sys
import contextlib
import pandas as pd
from PyQt5.QtCore import QAbstractTableModel, QModelIndex, QVariant, Qt, QEvent, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView, QAbstractButton, QLineEdit, QVBoxLayout, QWidget

DEBUG = True

class QPandasTableWidget(QTableView):
    """
    A self-contained custom widget that acts like a standard QTableWidget,
    but uses an internal QPandasTableModel to handle Pandas DataFrames natively.
    """
    def __init__(self, df=None, parent=None):
        super().__init__(parent)
        
        # UI Styling Defaults
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(True)
        
        # Track our 3-state index sorting loop (0: Ascending, 1: Descending, 2: Original)
        self._index_sort_state = 0
        
        # Connect horizontal headers for column sorting
        self.horizontalHeader().sortIndicatorChanged.connect(self.handle_sort)
        
        # Install an Event Filter on the corner button to detect clicks
        corner_button = self.findChild(QAbstractButton)
        if corner_button:
            corner_button.installEventFilter(self)
        
        # Initialize internal storage frames
        self._df_source = pd.DataFrame()
        self._df_view = None
        
        # Setup and bind the internal default model subclass
        self._model = self.QPandasTableModel(self)
        self.setModel(self._model)
        
        if df is not None:
            self.df = df

    def set_search_filter(self, text):
        """Filters the view DataFrame by matching the text across any column."""
        if not text:
            # If search is empty, restore the full base DataFrame
            self.df_view = self._df_source.copy()
            return

        search_string = str(text).lower()

        self._model.layoutAboutToBeChanged.emit()
        with self._model.correctPersistentIndex():
            # Check if any cell in the row contains the search substring (case-insensitive)
            # .astype(str) ensures numeric and boolean columns are searchable too
            mask = self._df_source.astype(str).apply(
                lambda row: row.str.lower().str.contains(search_string)
            ).any(axis=1)
            
            self.df_view = self._df_source[mask].copy()
            
        self._model.layoutChanged.emit()

    def eventFilter(self, obj, event):
        """Intercepts specific mouse patterns on the top-left corner button."""
        if isinstance(obj, QAbstractButton):
            # Double-click detected: Select the entire table
            if event.type() == QEvent.MouseButtonDblClick:
                if event.button() == Qt.LeftButton:
                    self.selectAll()
                    return True
                    
            # Single-click release detected: Run our 3-step loop
            elif event.type() == QEvent.MouseButtonRelease:
                if event.button() == Qt.LeftButton:
                    # QTableView native logic intercepts double-clicks as two press/releases.
                    # We use a tiny single-shot timer to let the double click win if it occurs.
                    QTimer.singleShot(100, self.handle_corner_click_loop)
                    return True
                    
        return super().eventFilter(obj, event)

    def handle_corner_click_loop(self):
        """Cycles through: Index Ascending -> Index Descending -> Original Order -> Loop"""
        if self.df_view.empty:
            return

        self._model.layoutAboutToBeChanged.emit()
        with self._model.correctPersistentIndex():
            
            if self._index_sort_state == 0:
                # Click 1: Sort by Index Ascending
                self.df_view = self.df_view.sort_index(ascending=True)
                self._index_sort_state = 1
                print("Corner State 1: Sorted by Index (Ascending)")
                
            elif self._index_sort_state == 1:
                # Click 2: Sort by Index Descending (Inverse)
                self.df_view = self.df_view.sort_index(ascending=False)
                self._index_sort_state = 2
                print("Corner State 2: Sorted by Index (Descending)")
                
            elif self._index_sort_state == 2:
                # Click 3: Restore Original Sort Order
                self.df_view = self.df_view.loc[self.df.index]
                self._index_sort_state = 0
                print("Corner State 3: Restored to Original Data Layout")

        self._model.layoutChanged.emit()
        
        # Clear the visual sort indicators on the column headers
        self.horizontalHeader().setSortIndicator(-1, Qt.AscendingOrder)

    def handle_sort(self, column_index, order):
        """Sorts the underlying DataFrame view dynamically based on header clicks."""
        if column_index == -1 or self.df_view.empty:
            return

        column_name = self.df_view.columns[column_index]
        ascending = (order == Qt.AscendingOrder)

        self._model.layoutAboutToBeChanged.emit()
        with self._model.correctPersistentIndex():
            self.df_view = self.df_view.sort_values(by=column_name, ascending=ascending)
        self._model.layoutChanged.emit()
        
        # Reset the corner loop state if the user chooses to sort by a normal data column instead
        self._index_sort_state = 0

    @property
    def df(self):
        return self._df_source

    @df.setter
    def df(self, new_df):
        if isinstance(new_df, (pd.Series, pd.DataFrame)):
            self._df_source = pd.DataFrame(new_df).copy()
            if DEBUG and not self._df_source.empty:
                if 'counter' not in self._df_source.columns:
                    self._df_source.insert(0, 'counter', list(range(len(self._df_source))))
        else:
            self._df_source = pd.DataFrame()
            
        self._df_view = None
        self._index_sort_state = 0
        self._model.layoutChanged.emit()

    @property
    def df_view(self):
        if self._df_view is not None:
            return self._df_view
        return self._df_source

    @df_view.setter
    def df_view(self, filtered_df):
        self._df_view = filtered_df
        self._model.layoutChanged.emit()

    # =========================================================================
    # THE INNER COMPANION MODEL
    # =========================================================================
    class QPandasTableModel(QAbstractTableModel):
        def __init__(self, table_widget):
            super().__init__(table_widget)
            self.widget = table_widget  
            self.persistentIndexPast = []
            self.show_index = True
            self.show_columns = True

        def rowCount(self, parent=QModelIndex()):
            return 0 if parent.isValid() else self.widget.df_view.shape[0]

        def columnCount(self, parent=QModelIndex()):
            return 0 if parent.isValid() else self.widget.df_view.shape[1]

        def data(self, index, role=Qt.DisplayRole):
            if not index.isValid():
                return QVariant()
            if role == Qt.DisplayRole:
                val = self.widget.df_view.iat[index.row(), index.column()]
                if pd.isna(val):
                    return QVariant("")
                if hasattr(val, 'item'):
                    val = val.item()
                return QVariant(val)
            return QVariant()

        def headerData(self, section, orientation, role=Qt.DisplayRole):
            if role != Qt.DisplayRole:
                return QVariant()
            if orientation == Qt.Horizontal and self.show_columns:
                return QVariant(str(self.widget.df_view.columns[section]))
            if orientation == Qt.Vertical and self.show_index:        
                return QVariant(str(self.widget.df_view.index[section]))
            return QVariant()

        @contextlib.contextmanager
        def correctPersistentIndex(self):
            oldIndexList = self.persistentIndexList()
            oldIds = self.widget.df_view.index.copy()
            yield  
            newIds = self.widget.df_view.index
            newIndexList = []
            persistentIndexPastNew = []
            for index in (oldIndexList + self.persistentIndexPast):
                if index.row() < len(oldIds):
                    row_id = oldIds[index.row()]
                    if row_id in newIds:
                        newRow = newIds.get_indexer([row_id])[0]
                        newIndexList.append(self.index(newRow, index.column(), index.parent()))
                        continue
                persistentIndexPastNew.append(index)
            self.changePersistentIndexList(oldIndexList, newIndexList)
            self.persistentIndexPast = persistentIndexPastNew


