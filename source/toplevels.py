from reimplemented import *
from crud import *
from PySide2 import QtWidgets
from PySide2 import QtGui
from menu import *


class SearchItems:
    def __init__(self, parent) -> None:
        self.parent = parent
        self.searchItemsFunction()

    def searchItemsFunction(self) -> None:
        self.search = QtWidgets.QDialog(self.parent)
        self.grid = QtWidgets.QGridLayout(self.search)
        self.searchLine = QtWidgets.QLineEdit()
        self.btSearch = Buttons('Feito', HOVER, DEFAULT)
        self.listItems = ListWidget()
        self.fraseInit = f'TAB:selecionar{" "*5}'
        self.fraseCmpl = f'ENTER:confirmar{" "*5}ESPAÇO:listar'
        self.frase = self.fraseInit + self.fraseCmpl
        self.infos = QtWidgets.QLabel(self.frase)
        self.search.setWindowTitle("Faca uma busca")
        self.infos.setStyleSheet('font-size: 15px;')
        self.btSearch.clicked.connect(self.concluded)
        self.searchLine.textEdited.connect(self.searching)
        self.search.resize(500, 350)
        self.grid.addWidget(self.searchLine, 0, 0)
        self.grid.addWidget(self.btSearch, 0, 1)
        self.grid.addWidget(self.listItems, 1, 0, 1, 2)
        self.grid.addWidget(self.infos, 2, 0)
        self.search.setTabOrder(self.searchLine, self.listItems)
        self.search.exec_()

    # => varre o banco...

    def searching(self, e) -> None:
        prods = queryCodDynamic(e)
        self.listItems.clear()
        for itens in prods:
            self.listItems.addItems(itens[1:2])
        self.listItems.currentItemChanged.connect(self.list_items_get)
        self.listItems.itemClicked.connect(self.list_items_get)

    # => lista todos os produtos

    def list_items_get(self) -> None:
        self.item = self.listItems.currentItem()
        self.prods = queryCodDynamic(self.item.text())
        self.parent.entryCod.clear()
        self.parent.entryCod.insert(self.prods[0][0])

    def concluded(self) -> None:
        self.search.close()
        self.parent.entryCod.setFocus()


class FinallyPurchasing:
    def __init__(self, parent) -> None:
        self.parent = parent
        self.tot = self.parent.TOTAL
        self.root_ = QtWidgets.QDialog(self.parent)
        self.grid = QtWidgets.QVBoxLayout(self.root_)
        self.labelInfoTotal = QtWidgets.QLabel('total da compra')
        total_formatted = self.parent.replace_(f'R$ {self.parent.TOTAL:.2f}')
        self.labelTotal = QtWidgets.QLabel(total_formatted)
        self.especialStyle = 'background: #fff; color: red; font-size: 50pt;'
        self.labelInfoMoney = QtWidgets.QLabel('Dinheiro')
        self.entMoney = QtWidgets.QLineEdit()
        self.labelThingMoneyInfo = QtWidgets.QLabel('Troco')
        self.labelThingMoney = QtWidgets.QLabel('R$ 0,00')
        self.buttonConteiner = QtWidgets.QFrame()
        grid = QtWidgets.QGridLayout(self.buttonConteiner)
        self.lb_finished_ = QtWidgets.QLabel('ESC: Sair.')
        self.btCupom_ = QtWidgets.QPushButton('Imprimir cupom')
        self.root_.setWindowTitle("Dialogo de Troco")
        self.btCupom_.clicked.connect(self.print_cupom)
        self.entMoney.returnPressed.connect(self.thingMoney)
        self.entMoney.setFocus()
        self.labelTotal.setStyleSheet(self.especialStyle)
        self.entMoney.setStyleSheet(self.especialStyle)
        self.labelThingMoney.setStyleSheet(self.especialStyle)
        self.root_.resize(400, 600)
        self.grid.addWidget(self.labelInfoTotal)
        self.grid.addWidget(self.labelTotal)
        self.grid.addWidget(self.labelInfoMoney)
        self.grid.addWidget(self.entMoney)
        self.grid.addWidget(self.labelThingMoneyInfo)
        self.grid.addWidget(self.labelThingMoney)
        self.grid.addWidget(self.buttonConteiner)
        grid.addWidget(self.lb_finished_, 0, 0)
        grid.addWidget(self.btCupom_, 0, 1)
        self.root_.exec_()

    # => mostra o valor do troco na tela.

    def thingMoney(self) -> None:
        val = float(self.entMoney.text().replace(',', '.'))
        show = val - self.tot
        self.labelThingMoney.setText(f'R$ {show:.2f}'.replace('.', ','))

    def print_cupom(self) -> None:
        print('Falta configurar impressora')


class Login:
    def __init__(self, parent: QtWidgets.QWidget) -> None:
        self.parent = parent
        self.root = QtWidgets.QDialog(self.parent)
        label1 = QtWidgets.QLabel('Usuário: ')
        label2 = QtWidgets.QLabel('Senha: ')
        self.entName = QtWidgets.QLineEdit()
        self.enPassw = QtWidgets.QLineEdit()
        self.btOk = QtWidgets.QPushButton('Ok')
        grid = QtWidgets.QGridLayout(self.root)
        self.root.setWindowTitle("Janela de login")
        self.enPassw.setEchoMode(QtWidgets.QLineEdit.Password)
        self.btOk.clicked.connect(self.queryUser)
        grid.addWidget(label1, 0, 0)
        grid.addWidget(self.entName, 0, 1)
        grid.addWidget(label2, 1, 0)
        grid.addWidget(self.enPassw, 1, 1)
        grid.addWidget(self.btOk, 2, 0, 1, 2)
        self.root.resize(400, 200)
        self.root.exec_()

    def queryUser(self) -> bool:
        user = self.entName.text()
        passw = self.enPassw.text()
        data = queryAdmin(user)
        try:
            teste1 = (user == data[0][0])
            teste2 = (passw == data[0][1])
            if teste1 and teste2:
                self.root.close()
                return True
        except IndexError:
            self.root.close()
            return False
