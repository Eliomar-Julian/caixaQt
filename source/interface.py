#!/usr/bin/python3

from PySide2 import QtCore, QtGui, QtWidgets
from loadconfigs import getStyle
from reimplemented import Buttons, HOVER, DEFAULT
from menu import MyMenu


class Interface(QtWidgets.QWidget):

    STYLE: str = getStyle()

    def __init__(self) -> None:
        super(Interface, self).__init__()
        self.places = QtWidgets.QGridLayout(self)
        self.places.setContentsMargins(0, 0, 0, 0)
        self.startMethods()

    def startMethods(self) -> None:
        self.startLogo()
        self.buttons()
        self.purchasingView()
        self.pricesShow()
        self.setWidgetName()
        self.pushStyle()
        self.menu()

    def menu(self) -> None:
        self.menuBar = MyMenu(self)

    def startLogo(self) -> None:
        image = QtGui.QPixmap('images/cart.png')
        self.frameLogo = QtWidgets.QFrame()
        conteiner = QtWidgets.QGridLayout(self.frameLogo)
        self.logo = QtWidgets.QLabel()
        self.frameLogo.setFixedSize(300, 300)
        self.logo.setPixmap(image)
        self.logo.setScaledContents(True)
        conteiner.addWidget(self.logo)
        self.places.addWidget(self.frameLogo, 0, 0)

    def buttons(self) -> None:
        self.frameButtons = QtWidgets.QFrame()
        self.btSearch = Buttons('Buscar', HOVER, DEFAULT)
        self.btThing = Buttons('Troco', HOVER, DEFAULT)
        self.btFinish = Buttons('Finalizar', HOVER, DEFAULT)
        self.btRemove = Buttons('Remover', HOVER, DEFAULT)
        conteiner = QtWidgets.QGridLayout(self.frameButtons)
        widget = [
            self.btSearch, self.btThing,
            self.btFinish, self.btRemove
        ]
        for wid in widget:
            conteiner.addWidget(wid)
            wid.setCursor(QtCore.Qt.PointingHandCursor)
        self.places.addWidget(self.frameButtons, 1, 0)

    def purchasingView(self) -> None:
        self.framePurchase = QtWidgets.QFrame()
        conteiner = QtWidgets.QGridLayout(self.framePurchase)
        label = QtWidgets.QLabel('Código do Produto: ')
        self.entryCod = QtWidgets.QLineEdit()
        self.tree = QtWidgets.QTreeWidget()
        not_scroll = QtCore.Qt.ScrollBarAlwaysOff
        self.tree.setWordWrap(False)
        self.tree.setHeaderLabels(('Produto', 'Qunt.', 'Preço', 'Total'))
        self.tree.setColumnWidth(0, 400)
        self.tree.setHorizontalScrollBarPolicy(not_scroll)
        self.tree.setVerticalScrollBarPolicy(not_scroll)
        conteiner.addWidget(label)
        conteiner.addWidget(self.entryCod)
        conteiner.addWidget(self.tree)
        self.places.addWidget(self.framePurchase, 0, 1)

    #=> preco total e corrente...

    def pricesShow(self) -> None:
        self.framePrices = QtWidgets.QFrame()
        conteiner = QtWidgets.QGridLayout(self.framePrices)
        self.lbPriceText = QtWidgets.QLabel('Preço do Item')
        self.lbPriceCurrent = QtWidgets.QLabel('R$ 0,00')
        self.lbPriceTextTotal = QtWidgets.QLabel('Total da Compra')
        self.lbPriceTotal = QtWidgets.QLabel('R$ 0,00')
        widgets = [
            self.lbPriceText,
            self.lbPriceCurrent,
            self.lbPriceTextTotal,
            self.lbPriceTotal
        ]
        for wid in widgets:
            conteiner.addWidget(wid)
            wid.setObjectName(str(wid))
        self.places.addWidget(self.framePrices, 0, 2)

    def setWidgetName(self) -> QtWidgets.QWidget.objectName:
        self.setObjectName('mainWindow')
        self.lbPriceText.setObjectName('showLabelPrice')
        self.lbPriceCurrent.setObjectName('priceCurrentItem')
        self.lbPriceTextTotal.setObjectName('labelTextPriceTotal')
        self.lbPriceTotal.setObjectName('labelPriceTotal')

    def pushStyle(self):
        self.setStyleSheet(self.STYLE)
