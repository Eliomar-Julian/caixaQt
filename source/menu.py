from PySide2 import QtWidgets, QtGui, QtCore


class MyMenu:
    def __init__(self, parent=None):
        self.parent = parent
        self.menuBar = QtWidgets.QMenuBar(self.parent)
        self.menuAdm = QtWidgets.QMenu('Administrar', self.menuBar)
        self.cadProd = self.menuAdm.addAction('Cadastrar Produtos')
        self.cadUser = self.menuAdm.addAction('Administrar Usuários')
        self.menuStyle = QtWidgets.QMenu('Aparência', self.menuBar)
        self.styl = self.menuStyle.addAction('Mudar Cores')
        self.icon = self.menuStyle.addAction('Trocar logo')
        self.menuBar.addMenu(self.menuAdm)
        self.menuBar.addMenu(self.menuStyle)
        self.menuBar.setStyleSheet(self.parent.STYLE)
        self.menuBar.setMinimumWidth(200)
        self.shortCuts()

    def shortCuts(self):
        keys = QtGui.QKeySequence
        qt = QtCore.Qt
        self.cadProd.setShortcut(keys(qt.CTRL + qt.Key_P))
        self.cadUser.setShortcut(keys(qt.CTRL + qt.Key_N))
        self.styl.setShortcut(keys(qt.CTRL + qt.Key_S))
        self.icon.setShortcut(keys(qt.CTRL + qt.Key_I))
