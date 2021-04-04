from PySide2 import QtWidgets, QtGui, QtCore
from crud import insertData, queryCod, queryAll, queryAndDelete
from reimplemented import DEFAULT


class Message:
    def sucess(parent, title, message) -> QtWidgets.QMessageBox:
        msg = QtWidgets.QMessageBox(parent)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setStandardButtons(msg.StandardButton.Ok)
        msg.setIcon(msg.Icon.Information)
        msg.exec_()

    def error(parent, title, message) -> QtWidgets.QMessageBox:
        msg = QtWidgets.QMessageBox(parent)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setStandardButtons(msg.StandardButton.Ok)
        msg.setIcon(msg.Icon.Warning)
        msg.exec_()


class MyMenu:
    def __init__(self, parent: QtWidgets.QWidget = None) -> None:
        self.parent = parent
        self.menuBar = QtWidgets.QMenuBar(self.parent)
        self.menuAdm = QtWidgets.QMenu('Administrar', self.menuBar)
        self.cadProd = self.menuAdm.addAction('Cadastrar e remover produtos')
        self.cadUser = self.menuAdm.addAction('Administrar usuários')
        self.overCashieAct = QtWidgets.QAction('Encerrar')
        self.menuAdm.addSeparator()
        self.changeLogo = self.menuAdm.addAction('Mudar logotipo')
        self.changeText = self.menuAdm.addAction('Editar Letreiro')
        self.menuBar.addMenu(self.menuAdm)
        self.menuBar.addAction(self.overCashieAct)
        self.menuBar.setStyleSheet(self.parent.STYLE)
        self.menuBar.setMinimumWidth(300)
        self.shortCuts()

    def shortCuts(self) -> None:
        keys = QtGui.QKeySequence
        qt = QtCore.Qt
        self.cadProd.setShortcut(keys(qt.CTRL + qt.Key_P))
        self.cadUser.setShortcut(keys(qt.CTRL + qt.Key_N))


class CadProd:
    def __init__(self, parent: QtWidgets.QWidget) -> None:
        self.parent = parent
        self.topLev = QtWidgets.QDialog(self.parent)
        self.lbCode = QtWidgets.QLabel('Código')
        self.lbDesc = QtWidgets.QLabel('Descrição')
        self.lbPric = QtWidgets.QLabel('Preço')
        self.layout = QtWidgets.QGridLayout(self.topLev)
        self.entCod = QtWidgets.QLineEdit()
        self.entDes = QtWidgets.QLineEdit()
        self.entPri = QtWidgets.QLineEdit()
        self.treeLi = QtWidgets.QTreeWidget()
        self.btAdct = QtWidgets.QPushButton('Adicionar')
        self.btRemo = QtWidgets.QPushButton('Remover')
        self.btExit = QtWidgets.QPushButton('Sair')
        self.btAdct.clicked.connect(self.get_data)
        self.topLev.setWindowTitle("Cadastro e remoção de produtos")
        self.btExit.clicked.connect(lambda: self.topLev.close())
        self.btRemo.clicked.connect(self.itemRemove)
        self.treeLi.setHeaderLabels(('Codigo', 'Produto', 'Preço'))
        self.treeLi.setColumnWidth(1, 400)
        self.layout.addWidget(self.lbCode, 0, 0)
        self.layout.addWidget(self.lbDesc, 0, 1)
        self.layout.addWidget(self.lbPric, 0, 2)
        self.layout.addWidget(self.entCod, 1, 0)
        self.layout.addWidget(self.entDes, 1, 1)
        self.layout.addWidget(self.entPri, 1, 2)
        self.layout.addWidget(self.treeLi, 2, 0, 1, 3)
        self.layout.addWidget(self.btAdct, 3, 0)
        self.layout.addWidget(self.btRemo, 3, 1)
        self.layout.addWidget(self.btExit, 3, 2)
        self.topLev.resize(600, 400)
        self.lbCode.setFocus()
        self.topLev.exec_()

    def get_data(self) -> insertData:
        def treeAdd(co: str, de: str, pr: float) -> None:
            item = QtWidgets.QTreeWidgetItem()
            prF = f'R$ {pr:.2f}'.replace('.', ',')
            item.setText(0, co)
            item.setText(1, de)
            item.setText(2, prF)
            self.treeLi.insertTopLevelItem(0, item)

        notValid = str('')
        cod = self.entCod.text().strip()
        des = self.entDes.text().strip()
        noRepeatCod = None
        try:
            noRepeatCod = queryCod(cod)[0][0]
        except IndexError:
            pass

        if noRepeatCod:
            msg = f'O Código já está em uso por:\n{queryCod(cod)[0][1]}'
            Message.error(self.parent, 'Codigo ja está em uso', msg)
            return

        if cod != notValid and des != notValid:
            try:
                pre = self.entPri.text().strip()
                pre = float(pre.replace(',', '.'))
                msg = f'{des.upper()} cadastrado com sucesso'
                insertData(cod, des, pre)
                treeAdd(cod, des, pre)
                self.entCod.clear()
                self.entDes.clear()
                self.entPri.clear()
                self.entCod.setFocus()
                Message.sucess(self.parent, 'cadastrado', msg)
            except ValueError:
                msg = 'Somente valor numerico no campo Preço.'
                Message.error(self.parent, 'Erro de Preço', msg)
        else:
            msg = 'Código/Descrição devem conter valores!'
            Message.error(self.parent, 'Valores não especificados', msg)

    def itemRemove(self) -> queryAndDelete:
        def remove():
            item = lista.currentItem()
            valid = queryAndDelete(item.text())
            msg = 'item removido dos registros'
            if valid:
                listed = queryAll()
                btCancel.setText('Concluído')
                lista.clear()
                for x in range(len(listed)):
                    lista.insertItem(x, listed[x][1])
                Message.sucess(self.topLev, 'removido', msg)

        frame = QtWidgets.QFrame(self.topLev)
        label = QtWidgets.QLabel('Todos os itens:')
        layout = QtWidgets.QGridLayout(frame)
        lista = QtWidgets.QListWidget()
        btRemove = QtWidgets.QPushButton('Remover')
        btCancel = QtWidgets.QPushButton('Cancelar')
        listed = queryAll()
        btRemove.clicked.connect(remove)
        btCancel.clicked.connect(lambda: frame.close())
        frame.setStyleSheet(DEFAULT)
        frame.setStyleSheet('background: #000;')
        layout.setContentsMargins(QtCore.QMargins(0, 0, 0, 0))
        layout.addWidget(label, 0, 0, 1, 2)
        layout.addWidget(lista, 1, 0, 1, 2)
        layout.addWidget(btRemove, 2, 0)
        layout.addWidget(btCancel, 2, 1)
        frame.resize(600, 400)
        for x in range(len(listed)):
            lista.insertItem(x, listed[x][1])
        frame.show()
