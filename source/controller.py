#!/usr/bin/python3
# clean code concept..

from toplevels import Login
from PySide2 import QtCore
from PySide2.QtCore import Qt
from interface import Interface
from PySide2 import QtWidgets
from toplevels import FinallyPurchasing, SearchItems, Login
from loadconfigs import saveTotal
from crud import queryCod, insert_user, load_admins, delete_admins
from menu import CadProd, Message


class MyApp(Interface):
    TOTAL: float = float()
    ZERO: str = 'R$ 0, 00'

    def __init__(self: Interface) -> None:
        super(MyApp, self).__init__()
        self.btSearch.function = self.searchItens
        self.btThing.function = self.finished_thing
        self.btFinish.function = self.finishVars
        self.entryCod.textEdited.connect(self.entryText)
        self.entryCod.returnPressed.connect(self.enterPress)
        self.btSearch.clicked.connect(self.searchItens)
        self.btFinish.clicked.connect(self.finishVars)
        self.btRemove.clicked.connect(self.removeItem)
        self.entryCod.textEdited.connect(self.entryText)
        self.menuBar.cadProd.triggered.connect(self.cadProdFunc)
        self.menuBar.cadUser.triggered.connect(self.cadUserFunc)
        self.menuBar.changeLogo.triggered.connect(self.changeLogo)
        self.menuBar.changeText.triggered.connect(self.changeText)
        self.menuBar.overCashieAct.triggered.connect(self.overCashieFunc)
        self.btThing.clicked.connect(self.finished_thing)
        self.entryCod.setFocus()

    def entryText(self, event_text: QtCore.QEvent) -> None:
        self.quantify: str = ' 1'
        self.lista: list = []
        self.multiple_index: str = '*'
        if self.multiple_index in event_text:
            self.indice_ = event_text.index(self.multiple_index)
            self.quantify = event_text[:self.indice_]
            self.lista = queryCod(event_text[self.indice_ + 1:])
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
                self.entryCod.clear()

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
            if passw == nul or rpass == nul:
                msg = 'As senhas não podem estar vazias'
                Message.error(self, 'Senha em branco', msg)
                return
            my_return = insert_user(name, passw)
            if not my_return:
                Message.error(self, 'erro', 'Nome ja existe')
            else:
                dial.close()

        def remove() -> None:
            def listing():
                adms = load_admins()
                for ad in adms:
                    listar.addItem(ad[0])

            def finally_remove():
                item = listar.currentItem()
                delete_admins(item.text())
                listar.clear()
                btC.setText('Sair')
                remove()

            frame = QtWidgets.QFrame(dial)
            grid = QtWidgets.QVBoxLayout(frame)
            listar = QtWidgets.QListWidget()
            btR = QtWidgets.QPushButton('Remover')
            btC = QtWidgets.QPushButton('Cancelar')
            grid.addWidget(listar)
            btR.clicked.connect(finally_remove)
            btC.clicked.connect(lambda: frame.close())
            grid.addWidget(btR)
            grid.addWidget(btC)
            grid.setContentsMargins(0, 0, 0, 0)
            listing()
            frame.resize(400, 300)
            frame.setStyleSheet('background: black;')
            frame.show()

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
        dial.setWindowTitle("Cadastro e remoção de usuários")
        dial.resize(400, 300)
        ent_pass.setEchoMode(QtWidgets.QLineEdit.Password)
        ent_rpas.setEchoMode(QtWidgets.QLineEdit.Password)
        bt_adc.clicked.connect(insert)
        bt_rem.clicked.connect(remove)
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

    def overCashieFunc(self) -> None:
        login = Login(self)
        if not login.queryUser():
            Message.error(self, 'erro', 'tente novamente!')
            return

        def read_(file_, mode) -> None:
            with open(file_, mode) as saldo:
                lista = saldo.read()
                return lista

        def listing() -> None:
            dados = read_('data/saldo.sd', 'r')
            wraps = dados.split('\n')
            value = float()
            first_time = str()
            last_time = str()
            for x in wraps:
                lista = x.split(' ')
                try:
                    value += float(lista[2])
                    if first_time == '':
                        first_time = lista[0]
                    last_time = lista[0]
                except:
                    ...
            if first_time == '' and last_time == '':
                first_time = last_time = '0:00'
            text.setText(dados)
            label_total.setText(f'<h1>R$ {value:.2f}</h1>'.replace('.', ','))
            color = 'style="color: red;"'
            frase = f'<h1 {color}>De {first_time} às {last_time}</h1>'
            label_info_total.setText(frase)

        def clear_cashie():
            text.clear()
            label_total.setText('<h1> R$ 0,00 </h1>')
            read_('data/saldo.sd', 'w')

        dialog = QtWidgets.QDialog(self)
        layout = QtWidgets.QGridLayout(dialog)
        label_info = QtWidgets.QLabel()
        text = QtWidgets.QTextEdit()
        label_info_total = QtWidgets.QLabel()
        label_total = QtWidgets.QLabel('R$ 0,00')
        button_clear = QtWidgets.QPushButton('limpar caixa')
        dialog.setWindowTitle("Limpando o caixa")
        layout.addWidget(label_info)

        layout.addWidget(text)
        layout.addWidget(label_info_total)
        layout.addWidget(label_total)
        layout.addWidget(button_clear)
        listing()
        button_clear.clicked.connect(clear_cashie)
        dialog.exec_()

    def changeLogo(self):
        file_ = QtWidgets.QFileDialog.getOpenFileName(
            self, 'abrir imagem', '~', 'Tipos de imagem(*.png *.jpg *.bmp)')
        self.logo.setPixmap(file_[0])

    def changeText(self):
        def change():
            frase = entry.text()
            self.timer.timeout.disconnect()
            self.label_latters.clear()
            self.nameMarket(frase)

        frame = QtWidgets.QDialog(self)
        layout = QtWidgets.QVBoxLayout(frame)
        label1 = QtWidgets.QLabel('escreva um letreiro')
        entry = QtWidgets.QLineEdit()
        label2 = QtWidgets.QLabel('ESC: sair   ENTER: confirmar')
        frame.setWindowTitle("Mudar letreiro")
        layout.addWidget(label1)
        layout.addWidget(entry)
        layout.addWidget(label2)
        frame.show()
        entry.setPlaceholderText('letreiro...')
        entry.returnPressed.connect(change)
        frame.resize(300, 300)
        frame.exec_()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Delete:
            self.removeItem()

