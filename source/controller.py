#!/usr/bin/python3
# clean code concept..

from toplevels import Login
from PySide2 import QtCore
from PySide2.QtCore import Qt
from interface import Interface
from PySide2 import QtWidgets
from toplevels import FinallyPurchasing, SearchItems, Login
from loadconfigs import saveTotal
from crud import queryCod, insert_user
from menu import CadProd, Message


class MyApp(Interface):
    TOTAL: float = float()
    ZERO: str = 'R$ 0, 00'

    def __init__(self: Interface) -> None:
        super(MyApp, self).__init__()
        self.btSearch.function = self.searchItens
        self.btThing.function = self.finished_thing
        self.btFinish.function = self.finishVars
        self.btRemove.function = self.removeItem
        self.entryCod.textEdited.connect(self.entryText)
        self.entryCod.returnPressed.connect(self.enterPress)
        self.btSearch.clicked.connect(self.searchItens)
        self.btFinish.clicked.connect(self.finishVars)
        self.btRemove.clicked.connect(self.removeItem)
        self.menuBar.cadProd.triggered.connect(self.cadProdFunc)
        self.menuBar.cadUser.triggered.connect(self.cadUserFunc)
        self.menuBar.overCashieAct.triggered.connect(self.overCashieFunc)
        self.btThing.clicked.connect(self.finished_thing)
        self.entryCod.setFocus()

    def entryText(self, event_text: QtCore.QEvent) -> None:
        self.quantify: str = ' 1'
        self.lista: list = []
        self.multiple_index: str = '*'
        if self.multiple_index in event_text:
            self.indice_ = event_text.index(self.multiple_index)
            self.quantify = event_text[self.indice_ + 1:]
            self.lista = queryCod(event_text[:self.indice_])
        else:
            self.lista = queryCod(event_text)

    # => automatiza replace...

    def replace_(self, string: str, a: str = '.', b: str = ',') -> str.replace:
        return string.replace(a, b)

    def enterPress(self, update_total: str = None) -> None:
        if self.lista:
            self.item = QtWidgets.QTreeWidgetItem()
            self.valor = int(self.quantify) * self.lista[0][2]
            self.TOTAL += self.valor
            self.valActual = self.replace_(f'{self.valor:.2f}')
            self.formatado = self.replace_(str('R$ %.2f' % (self.TOTAL)))
            self.vaUni = self.replace_(f'R$ {self.lista[0][2]:.2f}')
            self.currentPrice = self.replace_(f'R$ {self.valor:.2f}')
            self.showCurrent = self.replace_('R$ ' + str(self.valActual))
            if self.valor > 0:
                self.item.setText(0, self.lista[0][1])
                self.item.setText(1, self.quantify + ' x')
                self.item.setText(2, self.vaUni)
                self.item.setText(3, self.showCurrent)
                self.tree.insertTopLevelItem(0, self.item)
                self.lbPriceCurrent.setText(self.currentPrice)
                self.lbPriceTotal.setText(self.formatado)

    def removeItem(self) -> None:
        login = Login(self)
        if login.queryUser():
            item = self.tree.currentItem()
            index_item = self.tree.indexOfTopLevelItem(item)
            self.totalPrice = float(self.replace_(item.text(3)[2:], ',', '.'))
            self.tree.takeTopLevelItem(index_item)
            self.TOTAL -= self.totalPrice
            self.labelUpdate(item)

    # => finaliza a venda atual...

    def finished_thing(self) -> None:
        FinallyPurchasing(self)

    def labelUpdate(self, item: QtWidgets.QLabel) -> None:
        try:
            self.lbPriceCurrent.setText(item.text(3))
        except AttributeError:
            self.lbPriceCurrent.setText(self.ZERO)
        self.lbPriceTotal.setText(self.replace_(f'R$ {self.TOTAL:.2f}'))

    def finishVars(self) -> None:
        ok = QtWidgets.QMessageBox.StandardButton.Ok
        cancel = QtWidgets.QMessageBox.StandardButton.Cancel
        message = 'Realmnte deseja finalizar essa compra?'
        title = 'Finalizar'
        ms_box = QtWidgets.QMessageBox.warning
        resp = ms_box(self, title, message, ok | cancel)
        if resp is ok:
            saveTotal(self.TOTAL)
            self.TOTAL = 0
            self.lbPriceCurrent.setText(self.ZERO)
            self.lbPriceTotal.setText(self.ZERO)
            self.tree.clear()

    def cadProdFunc(self) -> None:
        validate = Login(self)
        title = 'Erro de autenticação'
        if validate.queryUser() is True:
            CadProd(self)
        elif validate.queryUser() is False:
            Message.error(self, title, 'Desculpe tente novamente')

    def cadUserFunc(self) -> None:
        def insert():
            nul = str('')
            name = ent_name.text().strip()
            passw = ent_pass.text().strip()
            rpass = ent_rpas.text().strip()
            if name == nul:
                msg = 'O nome não pode estar vazio'
                Message.error(self, 'Erro de nome', msg)
                return
            if passw != nul and rpass != nul:
                if passw != rpass:
                    msg = 'As senhas não coincidem'
                    Message.error(self, 'Erro de senha', msg)
                    return
                insert_user(name, passw)
            if passw == nul or rpass == nul:
                msg = 'As senhas não podem estar vazias'
                Message.error(self, 'Senha em branco', msg)

        login = Login(self)
        if not login.queryUser():
            return
        dial = QtWidgets.QDialog(self)
        layout = QtWidgets.QGridLayout(dial)
        labe_name = QtWidgets.QLabel('Nome: ')
        labe_pass = QtWidgets.QLabel('Senha:')
        labe_rpas = QtWidgets.QLabel('Repita a senha:')
        labe_info = QtWidgets.QLabel('ESC: sair.')
        ent_name = QtWidgets.QLineEdit()
        ent_pass = QtWidgets.QLineEdit()
        ent_rpas = QtWidgets.QLineEdit()
        bt_adc = QtWidgets.QPushButton('Cadastrar')
        bt_rem = QtWidgets.QPushButton('Remover')
        dial.resize(400, 300)
        ent_pass.setEchoMode(QtWidgets.QLineEdit.Password)
        ent_rpas.setEchoMode(QtWidgets.QLineEdit.Password)
        bt_adc.clicked.connect(insert)
        layout.addWidget(labe_name, 0, 0)
        layout.addWidget(labe_pass, 1, 0)
        layout.addWidget(labe_rpas, 2, 0)
        layout.addWidget(ent_name, 0, 1)
        layout.addWidget(ent_pass, 1, 1)
        layout.addWidget(ent_rpas, 2, 1)
        layout.addWidget(bt_adc, 3, 0)
        layout.addWidget(bt_rem, 3, 1)
        layout.addWidget(labe_info, 4, 0)
        dial.exec_()

    def searchItens(self):
        SearchItems(self)

    # // encerra as operações do dia de caixa ....

    def overCashieFunc(self):
        login = Login(self)
        print(login.queryUser())
