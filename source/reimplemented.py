from PySide2 import QtWidgets, QtCore
from time import sleep

HOVER = 'background-color: qlineargradient(\
spread:pad, x1:0.148492, y1:0.261, x2:0.928,\
y2:0.54, stop:0 rgba(109, 201, 222, 20),\
stop:1 rgba(255, 255, 255, 50));\
color: red;'

DEFAULT = '#0099ff'


class Buttons(QtWidgets.QPushButton):
    def __init__(self, text, style, defaultColor)-> None:
        self.text_ = text
        self.style_ = style
        self.defaultColor_ = defaultColor
        self.function = None
        QtWidgets.QPushButton.__init__(self)
        self.setText(self.text_)

    def focusInEvent(self, event: QtCore.QEvent.FocusIn) -> None:
        self.setStyleSheet(self.style_)

    def focusOutEvent(self, event: QtCore.QEvent.FocusOut) -> None:
        self.setStyleSheet(self.defaultColor_)

    def keyPressEvent(self, event: QtCore.QEvent.KeyPress) -> 'function':
        numEnter = QtCore.Qt.Key_Enter
        keyEnter = QtCore.Qt.Key_Return
        evento = event.key()
        if evento == numEnter or evento == keyEnter:
            if self.function:
                self.function()


class ListWidget(QtWidgets.QListWidget):
    def __init__(self)-> None:
        self.function = None
        QtWidgets.QListWidget.__init__(self)
