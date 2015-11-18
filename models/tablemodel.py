# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets

class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, model, manager, parent = None):
        super(TableModel, self).__init__(parent)
        self._model = model
        self._manager = manager
    
    def columnCount(self, index = None):
       return self._model.numCurrencies()
    
    def rowCount(self, index = QtCore.QModelIndex()):
       return self._model.numCurrencies()
    
    def data(self, index, role = QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            cur1 = self._model.getCurrency(index.row())
            cur2 = self._model.getCurrency(index.column())
            return "{:.4f}".format(self._model.getRatio(cur1, cur2))
    
    def headerData(self, col, orientation, role = QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            return self._model.getCurrency(col)
    
    def setData(self, index, value, role = QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole and value.strip():
            try:
                ratio = float(value)
            except ValueError:
                QtWidgets.QMessageBox.warning(self._manager._window, "Некорректный ввод",
                    "Соотношение должно быть дробным числом.")
                return False
            if ratio <= 0:
                QtWidgets.QMessageBox.warning(self._manager._window, "Некорректный ввод",
                    "Соотношение должно быть положительно.")
                return False
            cur1 = self._model.getCurrency(index.row())
            cur2 = self._model.getCurrency(index.column())
            return self._manager.setRatio(cur1, cur2, ratio)
        return False

    def flags(self, index):
        if index.isValid():
            flags = QtCore.Qt.ItemIsEnabled \
                | QtCore.Qt.ItemIsSelectable
            if index.row() != index.column():
                flags |= QtCore.Qt.ItemIsEditable
            return flags