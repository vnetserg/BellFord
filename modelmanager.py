# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets

from model import Model
from models.listmodel import ListModel
from models.tablemodel import TableModel

from speculation import Speculation

class ModelManager:
    def __init__(self, window):
        self._window = window
        self._model = Model()
        self._listModel = ListModel(self._model, self, parent = window)
        self._tableModel = TableModel(self._model, self, parent = window)
        window.ui.listView.setModel(self._listModel)
        window.ui.tableView.setModel(self._tableModel)

    def addCurrency(self, cur):
        if self._model.hasCurrency(cur):
            return QtWidgets.QMessageBox.warning(self._window, "Некорректный ввод",
                "Данная валюта уже есть в списке.")
        num = self._model.numCurrencies()
        self._listModel.beginInsertRows(QtCore.QModelIndex(), num, num)
        self._tableModel.beginInsertRows(QtCore.QModelIndex(), num, num)
        self._tableModel.beginInsertColumns(QtCore.QModelIndex(), num, num)
        self._model.addCurrency(cur)
        self._tableModel.endInsertRows()
        self._tableModel.endInsertColumns()
        self._listModel.endInsertRows()
        self._window.ui.tableView.resizeColumnsToContents()

    def deleteCurrencyNum(self, num):
        self._listModel.beginRemoveRows(QtCore.QModelIndex(), num, num)
        self._tableModel.beginRemoveRows(QtCore.QModelIndex(), num, num)
        self._tableModel.beginRemoveColumns(QtCore.QModelIndex(), num, num)
        self._model.deleteCurrencyNum(num)
        self._tableModel.endRemoveRows()
        self._tableModel.endRemoveColumns()
        self._listModel.endRemoveRows()

    def renameCurrency(self, old, new):
        if old == new: return
        if self._model.hasCurrency(new):
            QtWidgets.QMessageBox.warning(self._window, "Некорректный ввод",
                "Данная валюта уже есть в списке.")
            return False
        self._model.renameCurrency(old, new)
        num = self._model.currencyIndex(new)
        self._listModel.dataChanged.emit(self._listModel.createIndex(num, 0),
            self._listModel.createIndex(num, 0))
        self._tableModel.headerDataChanged.emit(QtCore.Qt.Vertical, num, num)
        self._tableModel.headerDataChanged.emit(QtCore.Qt.Horizontal, num, num)
        self._window.ui.tableView.resizeColumnsToContents()
        return True

    def setRatio(self, cur1, cur2, ratio):
        num1 = self._model.currencyIndex(cur1)
        num2 = self._model.currencyIndex(cur2)
        self._model.setRatio(cur1, cur2, ratio)
        self._tableModel.dataChanged.emit(self._tableModel.createIndex(num1, num2),
            self._listModel.createIndex(num1, num2))
        self._tableModel.dataChanged.emit(self._tableModel.createIndex(num2, num1),
            self._listModel.createIndex(num2, num1))
        self._window.ui.tableView.resizeColumnsToContents()
        return True

    def speculation(self):
        return Speculation(self._model)