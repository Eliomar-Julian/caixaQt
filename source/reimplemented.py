from PySide2 import QtWidgets, QtCore

HOVER = 'background-color: qlineargradient(\
spread:pad, x1:0.148492, y1:0.261, x2:0.928,\
y2:0.54, stop:0 rgba(109, 201, 222, 20),\
stop:1 rgba(255, 255, 255, 50));\
color: red;'

DEFAULT = '#0099ff'


class Buttons(QtWidgets.QPushButton):
    '''
    Reeimplemntado os botoes
    '''

    def __init__(self, text, style, defaultColor):
        self.text_ = text
        self.style_ = style
        self.defaultColor_ = defaultColor
        self.function = None
        QtWidgets.QPushButton.__init__(self)
        self.setText(self.text_)

    # // adiciona estilo degrade quando o botão é focalizado atraves de um tab

    def focusInEvent(self, event):
        self.setStyleSheet(self.style_)

    # // traz a cor padrão quando o botão sai de foco...

    def focusOutEvent(self, event):
        self.setStyleSheet(self.defaultColor_)

    # // espera enter se apertado para lhe atribuir um metodo...

    def keyPressEvent(self, event):
        numEnter = QtCore.Qt.Key_Enter
        keyEnter = QtCore.Qt.Key_Return
        evento = event.key()
        if evento == numEnter or evento == keyEnter:
            if self.function:
                self.function()


class ListWidget(QtWidgets.QListWidget):
    def __init__(self):
        self.function = None
        QtWidgets.QListWidget.__init__(self)
