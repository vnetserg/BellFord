# -*- coding: utf-8 -*-

from PyQt5 import QtCore

class ListModel(QtCore.QAbstractListModel):
    def __init__(self, model, manager, parent = None):
        super(ListModel, self).__init__(parent)
        self._model = model
        self._manager = manager
    
    def rowCount(self, index = QtCore.QModelIndex()):
       return self._model.numCurrencies()
    
    def data(self, index, role = QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            return self._model.getCurrency(index.row())
    
    def setData(self, index, value, role = QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole and value.strip():
            return self._manager.renameCurrency(self.data(index), value.strip())
        return False
    
    def flags(self, index):
        if index.isValid():
            flags = QtCore.Qt.ItemIsEnabled \
                | QtCore.Qt.ItemIsEditable \
                | QtCore.Qt.ItemIsSelectable
            #   | QtCore.Qt.ItemIsUserCheckable
            return flags