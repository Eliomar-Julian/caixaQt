#!/usr/bin/python3

from PySide2 import QtCore, QtGui, QtWidgets
from load_style import getStyle
from buttons import Buttons, HOVER, DEFAULT
import sys


class Interface(QtWidgets.QWidget):

    STYLE = getStyle()

    def __init__(self):
        super(Interface, self).__init__()
        self.places = QtWidgets.QGridLayout(self)
        self.places.setContentsMargins(0, 0, 0, 0)
        self.startMethods()

    def startMethods(self):
        self.startLogo()
        self.buttons()
        self.purchasingView()
        self.pricesShow()
        self.setWidgetName()
        self.pushStyle()

    def startLogo(self):
        image = QtGui.QPixmap('images/cart.png')
        self.frameLogo = QtWidgets.QFrame()
        conteiner = QtWidgets.QGridLayout(self.frameLogo)
        self.logo = QtWidgets.QLabel()
        self.frameLogo.setFixedSize(300, 300)
        self.logo.setPixmap(image)
        self.logo.setScaledContents(True)
        conteiner.addWidget(self.logo)
        self.places.addWidget(self.frameLogo, 0, 0)

    def buttons(self):
        self.frameButtons = QtWidgets.QFrame()
        self.btSearch = Buttons('Buscar', HOVER, DEFAULT)
        self.btFinish = Buttons('Finalizar', HOVER, DEFAULT)
        self.btCancel = Buttons('Cancelar', HOVER, DEFAULT)
        self.btRemove = Buttons('Remover', HOVER, DEFAULT)
        conteiner = QtWidgets.QGridLayout(self.frameButtons)
        widget = [
            self.btSearch, self.btFinish,
            self.btCancel, self.btRemove
        ]
        for wid in widget:
            conteiner.addWidget(wid)
            wid.setCursor(QtCore.Qt.PointingHandCursor)
        self.places.addWidget(self.frameButtons, 1, 0)

    def purchasingView(self):
        self.framePurchase = QtWidgets.QFrame()
        conteiner = QtWidgets.QGridLayout(self.framePurchase)
        label = QtWidgets.QLabel('Código do Produto: ')
        self.entryCod = QtWidgets.QLineEdit()
        self.tree = QtWidgets.QTreeWidget()
        self.tree.setWordWrap(False)
        self.tree.setHeaderLabels(('Produto', 'Qunt.', 'Preço', 'Total'))
        self.tree.setColumnWidth(0, 320)
        conteiner.addWidget(label)
        conteiner.addWidget(self.entryCod)
        conteiner.addWidget(self.tree)
        self.places.addWidget(self.framePurchase, 0, 1)

    def pricesShow(self):
        self.framePrices = QtWidgets.QFrame()
        conteiner = QtWidgets.QGridLayout(self.framePrices)
        self.lbPriceText = QtWidgets.QLabel('Preço do Item')
        self.lbPriceCurrent = QtWidgets.QLabel('R$ 0,00')
        self.lbPriceTextTotal = QtWidgets.QLabel('Total da Compra')
        self.lbPriceTotal = QtWidgets.QLabel('R$ 0,00')
        widgets = [
            self.lbPriceText, self.lbPriceCurrent,
            self.lbPriceTextTotal, self.lbPriceTotal
        ]
        for wid in widgets:
            conteiner.addWidget(wid)
            wid.setObjectName(str(wid))
        self.places.addWidget(self.framePrices, 0, 2)

    def setWidgetName(self):
        self.setObjectName('mainWindow')
        self.lbPriceText.setObjectName('showLabelPrice')
        self.lbPriceCurrent.setObjectName('priceCurrentItem')
        self.lbPriceTextTotal.setObjectName('labelTextPriceTotal')
        self.lbPriceTotal.setObjectName('labelPriceTotal')

    def pushStyle(self):
        self.setStyleSheet(self.STYLE)
