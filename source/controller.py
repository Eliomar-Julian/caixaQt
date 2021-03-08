#!/usr/bin/python3

from interface import Interface
from PySide2 import QtWidgets
from toplevels import SearchItems, FinallyPurchasing, Login
from loadconfigs import saveTotal
from crud import queryCod
from menu import CadProd, Message


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
        self.btRemove.function = self.removeItem
        self.entryCod.textEdited.connect(self.entryText)
        self.entryCod.returnPressed.connect(self.enterPress)
        self.btSearch.clicked.connect(self.searchItens)
        self.btFinish.clicked.connect(self.finishVars)
        self.btRemove.clicked.connect(self.removeItem)
        self.menuBar.cadProd.triggered.connect(self.cadProdFunc)
        self.menuBar.cadUser.triggered.connect(self.cadUserFunc)
        self.menuBar.styl.triggered.connect(self.stylFunc)
        self.menuBar.icon.triggered.connect(self.iconFunc)
        self.menuBar.overCashieAct.triggered.connect(self.overCashieFunc)
        self.entryCod.setFocus()

    # // filtra a entrada de texto para ver se tem algum
    # multiplicador

    def entryText(self, eventText):
        self.quantify = str(' 1')
        self.lista = list()
        if str('*') in eventText:
            self.indice_ = eventText.index('*')
            self.quantify = eventText[self.indice_ + 1:]
            self.lista = queryCod(eventText[:self.indice_])
        else:
            self.lista = queryCod(eventText)

    # // espera enter ser apertado para atualizar os Widgets
    # na tela principal.

    def enterPress(self):
        if self.lista:
            self.item = QtWidgets.QTreeWidgetItem()
            self.valor = int(self.quantify) * self.lista[0][2]
            self.TOTAL += self.valor
            self.valActual = f'{self.valor:.2f}'
            self.formatado = str('R$ %.2f' % (self.TOTAL)).replace('.', ',')
            self.vaUni = f'R$ {self.lista[0][2]:.2f}'.replace('.', ',')
            self.currentPrice = f'R$ {self.valor:.2f}'.replace('.', ',')
            self.showCurrent = 'R$ ' + str(self.valActual).replace('.', ',')
            self.btThing.clicked.connect(self.finished)
            if self.valor > 0:
                self.item.setText(0, self.lista[0][1])
                self.item.setText(1, self.quantify + ' x')
                self.item.setText(2, self.vaUni)
                self.item.setText(3, self.showCurrent)
                self.tree.insertTopLevelItem(0, self.item)
                self.lbPriceCurrent.setText(self.currentPrice)
                self.lbPriceTotal.setText(self.formatado)

    # // remove os itens selecionados na lista de compras

    def removeItem(self):
        login = Login(self)
        if login.queryUser():
            item = self.tree.currentItem()
            indexItem = self.tree.indexOfTopLevelItem(item)
            totalPrice = float(item.text(3)[2:].replace(',', '.'))
            self.tree.takeTopLevelItem(indexItem)
            self.TOTAL -= totalPrice
            self.labelUpdate(item)

    # // chama a função de finalizar a compra atual

    def finished(self):
        FinallyPurchasing(self, valor=self.TOTAL)
        return

    # // atualiza as amostras de preços da tela...

    def labelUpdate(self, i):
        try:
            self.lbPriceCurrent.setText(i.text(3))
        except AttributeError:
            self.lbPriceCurrent.setText('R$ 0,00')
        self.lbPriceTotal.setText(f'R$ {self.TOTAL:.2f}'.replace('.', ','))

    # // finaliza a venda atual e zera variaveis...

    def finishVars(self):
        ok = QtWidgets.QMessageBox.StandardButton.Ok
        cancel = QtWidgets.QMessageBox.StandardButton.Cancel
        message = 'Realmnte deseja finalizar essa compra?'
        title = 'Finalizar'
        resp = QtWidgets.QMessageBox.warning(
            self, title, message, ok | cancel)
        if resp == ok:
            saveTotal(self.TOTAL)
            self.TOTAL = 0
            self.lbPriceCurrent.setText('R$ 0,00')
            self.lbPriceTotal.setText('R$ 0,00')
            self.tree.clear()

    # // abre janela de cadastro de produtos...

    def cadProdFunc(self):
        validate = Login(self)
        title = 'Erro de autenticação'
        if validate.queryUser() == (True):
            CadProd(self)
        elif validate.queryUser() == (False):
            Message.error(self, title, 'Desculpe tente novamente')

    # // abre janela de cadastro de usuarios

    def cadUserFunc(self):
        print('cadUserFunc')

    # muda a cor de fundo e de frente da aplicação

    def stylFunc(self):
        print('stylFunc')

    # // muda o logo do estabelecimento

    def iconFunc(self):
        print('iconFunc')

    # // chama a função de busca de produtos no banco de dados...

    def searchItens(self):
        SearchItems(self)

    # // encerra as operações do dia de caixa ....

    def overCashieFunc(self):
        login = Login(self)
        print(login.queryUser())
