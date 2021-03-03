from reimplemented import ListWidget, Buttons, HOVER, DEFAULT
from crud import queryCod, queryCodDynamic
from PySide2 import QtCore, QtWidgets


class SearchItems:
    def __init__(self, parent) -> None:
        '''
        classe responsavel por busca os itens no banco
        e listar no treeview.
        '''
        self.parent = parent
        self.searchItemsFunction()
    
    def searchItemsFunction(self):
        '''
        Desenha a janela top level de busca
        '''
        self.search = QtWidgets.QDialog(self.parent)
        self.grid = QtWidgets.QGridLayout(self.search)
        self.searchLine = QtWidgets.QLineEdit()
        self.btSearch = Buttons('Feito', HOVER, DEFAULT)
        self.listItems = ListWidget()
        self.frase = f'TAB:selecionar{" "*5}ENTER:confirmar{" "*5}ESPAÇO:listar'
        self.infos = QtWidgets.QLabel(self.frase)
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

    def searching(self, e):
        '''
        Invocado a cada tecla pressionada e varre
        dinamicamente o banco.
        '''
        prods = queryCodDynamic(e)
        self.listItems.clear()
        for itens in prods:
            self.listItems.addItems(itens[1:2])
        self.listItems.currentItemChanged.connect(self.listItemsGet)
        self.listItems.itemClicked.connect(self.listItemsGet)

    def listItemsGet(self):
        '''
        pega o produto selecionado e adiciona o codigo
        na linha de entrada de codigo da janela principal.
        '''
        self.item = self.listItems.currentItem()
        self.prods = queryCodDynamic(self.item.text())
        self.parent.entryCod.clear()
        self.parent.entryCod.insert(self.prods[0][0])

    def concluded(self):
        '''
        fecha a janela de buscas e direciona o foco
        para a linha de entrda da janela principal.
        '''
        self.search.close()
        self.parent.entryCod.setFocus()


class FinallyPurchasing:
    def __init__(self, parent) -> None:
        '''
        Classe responsavel por finalizar a compra atual
        e zerar os contadores da janela principal
        '''
        self.parent = parent
        self.top()

    def top(self):
        '''
        desenhando a janela de finalização...
        '''
        self.root = QtWidgets.QDialog(self.parent)
        self.grid = QtWidgets.QVBoxLayout(self.root)
        self.labelInfoTotal = QtWidgets.QLabel('total da compra')
        self.labelTotal = QtWidgets.QLabel(self.parent.formatado)
        self.especialStyle = 'background: #fff; color: red; font-size: 50pt;'
        self.labelInfoMoney = QtWidgets.QLabel('Dinheiro')
        self.entMoney = QtWidgets.QLineEdit()
        self.labelThingMoneyInfo = QtWidgets.QLabel('Troco')
        self.labelThingMoney = QtWidgets.QLabel('R$ 0,00')
        self.buttonConteiner = QtWidgets.QFrame()
        grid = QtWidgets.QGridLayout(self.buttonConteiner)
        self.btFinished_ = QtWidgets.QPushButton('Finalizar')
        self.btCupom_ = QtWidgets.QPushButton('Imprimir cupom')
        self.entMoney.returnPressed.connect(self.thingMoney)
        self.entMoney.setFocus()
        self.labelTotal.setStyleSheet(self.especialStyle)
        self.entMoney.setStyleSheet(self.especialStyle)
        self.labelThingMoney.setStyleSheet(self.especialStyle)
        self.root.resize(400, 600)
        self.grid.addWidget(self.labelInfoTotal)
        self.grid.addWidget(self.labelTotal)
        self.grid.addWidget(self.labelInfoMoney)
        self.grid.addWidget(self.entMoney)
        self.grid.addWidget(self.labelThingMoneyInfo)
        self.grid.addWidget(self.labelThingMoney)
        self.grid.addWidget(self.buttonConteiner)
        grid.addWidget(self.btFinished_, 0, 0)
        grid.addWidget(self.btCupom_, 0, 1)
        self.root.exec_()

    def thingMoney(self):
        '''
        mostra o valor do troco na tela.
        '''
        tot = self.parent.TOTAL
        val = float(self.entMoney.text().replace(',', '.'))
        show = val - tot
        self.labelThingMoney.setText(f'R$ {show:.2f}'.replace('.', ','))
