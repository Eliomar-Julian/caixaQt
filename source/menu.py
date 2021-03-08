from PySide2 import QtWidgets, QtGui, QtCore
from crud import *
from reimplemented import DEFAULT


# // Classe que exibe uma messageBox


class Message:
    def sucess(parent, title, message):
        parent = parent
        title = title
        message = message
        msg = QtWidgets.QMessageBox(parent)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setStandardButtons(msg.StandardButton.Ok)
        msg.setIcon(msg.Icon.Information)
        msg.exec_()

    def error(parent, title, message):
        parent = parent
        title = title
        message = message
        msg = QtWidgets.QMessageBox(parent)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setStandardButtons(msg.StandardButton.Ok)
        msg.setIcon(msg.Icon.Information)
        msg.exec_()


# // classe que define a barra de menu...


class MyMenu:
    def __init__(self, parent=None):
        self.parent = parent
        self.menuBar = QtWidgets.QMenuBar(self.parent)
        self.menuAdm = QtWidgets.QMenu('Administrar', self.menuBar)
        self.cadProd = self.menuAdm.addAction('Cadastrar e remover produtos')
        self.cadUser = self.menuAdm.addAction('Administrar usuários')
        self.menuStyle = QtWidgets.QMenu('Aparência', self.menuBar)
        self.styl = self.menuStyle.addAction('Mudar cores')
        self.icon = self.menuStyle.addAction('Trocar logo')
        self.overCashieAct = QtWidgets.QAction('Encerrar')
        self.menuBar.addMenu(self.menuAdm)
        self.menuBar.addMenu(self.menuStyle)
        self.menuBar.addAction(self.overCashieAct)
        self.menuBar.setStyleSheet(self.parent.STYLE)
        self.menuBar.setMinimumWidth(300)
        self.shortCuts()

    def shortCuts(self):
        keys = QtGui.QKeySequence
        qt = QtCore.Qt
        self.cadProd.setShortcut(keys(qt.CTRL + qt.Key_P))
        self.cadUser.setShortcut(keys(qt.CTRL + qt.Key_N))
        self.styl.setShortcut(keys(qt.CTRL + qt.Key_S))
        self.icon.setShortcut(keys(qt.CTRL + qt.Key_I))


# // cadastra e remove itens do banco de dados


class CadProd:
    def __init__(self, parent):
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
        self.btAdct.clicked.connect(self.getData)
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

    # // metodo que valida dados ante de serem inseridos no banco...

    def getData(self):
        def treeAdd(co, de, pr):
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

    # // metodo responsavel por eliminar um item do banco

    def itemRemove(self):
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
