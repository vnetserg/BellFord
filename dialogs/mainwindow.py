# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets
from ui.ui_mainwindow import Ui_MainWindow

from modelmanager import ModelManager

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.connectAll()
        self._manager = ModelManager(self)

    def connectAll(self):
        self.ui.addButton.pressed.connect(self.addButtonPressed)
        self.ui.deleteButton.pressed.connect(self.deleteButtonPressed)
        self.ui.calcButton.pressed.connect(self.calcButtonPressed)

    def addButtonPressed(self):
        cur, flag = QtWidgets.QInputDialog.getText(self, "Ввод названия", "Введите название валюты:")
        if not flag: return
        self._manager.addCurrency(cur.strip())

    def deleteButtonPressed(self):
        index = self.ui.listView.currentIndex()
        if not index.isValid():
            QtWidgets.QMessageBox.warning(self, "Не выбрана валюта",
                "Вы не выбрали валюту для удаления.")
        else:
            self._manager.deleteCurrencyNum(index.row())

    def calcButtonPressed(self):
        spec = self._manager.speculation()
        if spec.exists:
            self.ui.pathEdit.setText(" -> ".join(spec.path + spec.path[0:1]))
            self.ui.ratioEdit.setText(str(spec.ratio))
        else:
            self.ui.pathEdit.clear()
            self.ui.ratioEdit.clear()
            QtWidgets.QMessageBox.information(self, "Решения нет",
                "В данных условиях спекуляция невозможна.")
