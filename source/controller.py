#!/usr/bin/python3

from interface import Interface
from PySide2 import QtWidgets, QtGui, QtCore
from crud import queryCod, queryCodDynamic
from toplevels import SearchItems, FinallyPurchasing
from reimplemented import ListWidget, Buttons, HOVER, DEFAULT
import sys


class MyApp(Interface):

    TOTAL = float()

    def __init__(self):
        super(MyApp, self).__init__()
        self.btSearch.function = self.searchItens
        self.btFinish.function = self.finished
        self.entryCod.textEdited.connect(self.entryText)
        self.entryCod.returnPressed.connect(self.enterPress)
        self.entryCod.setFocus()
        self.btSearch.clicked.connect(self.searchItens)
        self.btFinish.clicked.connect(self.finished)

    def entryText(self, e):
        '''
        filtra a entrada de texto para ver se tem algum 
        multiplicador
        '''
        self.qtd = '1'
        self.lista = []
        if '*' in e:
            indice = e.index('*')
            self.qtd = e[indice + 1:]
            self.lista = queryCod(e[:indice])
        else:
            self.lista = queryCod(e)

    def enterPress(self):
        '''
        espera enter ser apertado para atualizar os Widgets 
        na tela principal.
        '''
        if self.lista:
            self.item = QtWidgets.QTreeWidgetItem()
            self.valor = int(self.qtd) * self.lista[0][2]
            self.TOTAL += self.valor
            self.valActual = f'{self.valor:.2f}'
            self.formatado = str('R$ %.2f' % (self.TOTAL)).replace('.', ',')
            self.vaUni = f'R$ {self.lista[0][2]:.2f}'.replace('.', ',')
            self.currentPrice = f'R$ {self.valor:.2f}'.replace('.', ',')
            self.showCurrent = 'R$ ' + str(self.valActual).replace('.', ',')
            if self.valor > 0:
                self.item.setText(0, self.lista[0][1])
                self.item.setText(1, self.qtd + ' x')
                self.item.setText(2, self.vaUni)
                self.tree.insertTopLevelItem(0, self.item)
                self.item.setText(3, self.showCurrent)
                self.lbPriceCurrent.setText(self.currentPrice)
                self.lbPriceTotal.setText(self.formatado)

    def searchItens(self):
        SearchItems(self)

    def finished(self):
        FinallyPurchasing(self)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    form = MyApp()
    form.show()
    sys.exit(app.exec_())
