#!/usr/bin/python3

from interface import Interface
from PySide2 import QtWidgets, QtGui, QtCore
from crud import queryCod, queryCodDynamic
from reimplemented import ListWidget, Buttons, HOVER, DEFAULT
import sys


class MyApp(Interface):

    TOTAL = float()

    def __init__(self):
        super(MyApp, self).__init__()
        self.btSearch.function = self.searchItens
        self.entryCod.textEdited.connect(self.entryText)
        self.entryCod.returnPressed.connect(self.enterPress)
        self.entryCod.setFocus()
        self.btSearch.clicked.connect(self.searchItens)

    def entryText(self, e):
        self.qtd = '1'
        self.lista = []
        if '*' in e:
            indice = e.index('*')
            self.qtd = e[indice + 1:]
            self.lista = queryCod(e[:indice])
        else:
            self.lista = queryCod(e)

    def enterPress(self):
        if self.lista:
            self.item = QtWidgets.QTreeWidgetItem()
            valor = int(self.qtd) * self.lista[0][2]
            self.TOTAL += valor
            val = f'{valor:.2f}'
            formatado = str('R$ %.2f' % (self.TOTAL)).replace('.', ',')
            it = 'R$ ' + str(self.lista[0][2]).replace('.', ',')
            self.item.setText(0, self.lista[0][1])
            self.item.setText(1, self.qtd + 'x')
            self.item.setText(2, it)
            self.tree.addTopLevelItem(self.item)
            self.item.setText(3, 'R$ ' + str(val).replace('.', ','))
            self.lbPriceCurrent.setText(f'R$ {valor:.2f}'.replace('.', ','))
            self.lbPriceTotal.setText(formatado)

    def searchItens(self):
        self.search = QtWidgets.QDialog(self)
        grid = QtWidgets.QGridLayout(self.search)
        self.searchLine = QtWidgets.QLineEdit()
        btSearch = Buttons('Feito', HOVER, DEFAULT)
        self.listItems = ListWidget()
        btSearch.clicked.connect(self.concluded)
        self.searchLine.textEdited.connect(self.searching)
        self.search.resize(500, 350)
        grid.addWidget(self.searchLine, 0, 0)
        grid.addWidget(btSearch, 0, 1)
        grid.addWidget(self.listItems, 1, 0, 1, 2)
        self.search.setTabOrder(self.searchLine, self.listItems)
        self.search.exec_()

    def searching(self, e):
        prods = queryCodDynamic(e)
        self.listItems.clear()
        for itens in prods:
            self.listItems.addItems(itens[1:2])
        self.listItems.currentItemChanged.connect(self.listItemsGet)
        self.listItems.itemClicked.connect(self.listItemsGet)

    def listItemsGet(self):
        item = self.listItems.currentItem()
        prods = queryCodDynamic(item.text())
        self.entryCod.clear()
        self.entryCod.insert(prods[0][0])

    def concluded(self):
        self.search.close()
        self.entryCod.setFocus()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    form = MyApp()
    form.show()
    sys.exit(app.exec_())
