#!/usr/bin/python3

from interface import Interface
from PySide2 import QtWidgets, QtGui, QtCore
from crud import queryCod, queryCodDynamic
from toplevels import SearchItems, FinallyPurchasing
from reimplemented import ListWidget, Buttons, HOVER, DEFAULT
from loadconfigs import saveTotal
import sys


class MyApp(Interface):
    '''
    classe de controle de interface...
    '''
    TOTAL = float()

    def __init__(self):
        super(MyApp, self).__init__()
        self.btSearch.function = self.searchItens
        self.btThing.function = self.finished
        self.btFinish.function = self.finishVars
        self.entryCod.textEdited.connect(self.entryText)
        self.entryCod.returnPressed.connect(self.enterPress)
        self.entryCod.setFocus()
        self.btSearch.clicked.connect(self.searchItens)
        self.btThing.clicked.connect(self.finished)
        self.btFinish.clicked.connect(self.finishVars)


    # // filtra a entrada de texto para ver se tem algum 
    # multiplicador
    
    def entryText(self, e):
        self.qtd = '1'
        self.lista = []
        if '*' in e:
            indice = e.index('*')
            self.qtd = e[indice + 1:]
            self.lista = queryCod(e[:indice])
        else:
            self.lista = queryCod(e)
    
    # // espera enter ser apertado para atualizar os Widgets 
    # na tela principal.
    
    def enterPress(self):
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

    # // finaliza a venda atual e zera variaveis...

    def finishVars(self):
        ok = QtWidgets.QMessageBox.StandardButton.Ok
        cancel = QtWidgets.QMessageBox.StandardButton.Cancel
        message = 'Realmnte deseja finalizar essa compra?'
        title = 'Finalizar'
        resp = QtWidgets.QMessageBox.warning(
            self, title, message, ok | cancel
        )
        if resp == ok:
            saveTotal(self.TOTAL)
            self.TOTAL = 0
            self.lbPriceCurrent.setText('R$ 0,00')
            self.lbPriceTotal.setText('R$ 0,00')
            self.tree.clear()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    form = MyApp()
    form.show()
    sys.exit(app.exec_())
