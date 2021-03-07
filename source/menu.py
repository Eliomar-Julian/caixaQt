from PySide2 import QtWidgets, QtGui, QtCore
from crud import insertData, queryCod


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
        msg.setStandardButtons(msg.StandardButton.Critical)
        msg.setIcon(msg.Icon.Information)
        msg.exec_()


class MyMenu:
    def __init__(self, parent=None):
        self.parent = parent
        self.menuBar = QtWidgets.QMenuBar(self.parent)
        self.menuAdm = QtWidgets.QMenu('Administrar', self.menuBar)
        self.cadProd = self.menuAdm.addAction('Cadastrar Produtos')
        self.cadUser = self.menuAdm.addAction('Administrar Usuários')
        self.menuStyle = QtWidgets.QMenu('Aparência', self.menuBar)
        self.styl = self.menuStyle.addAction('Mudar Cores')
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

    def getData(self):
        def messageError(message):
            msg = QtWidgets.QMessageBox(self.parent)
            msg.setWindowTitle('Erro de entrada de dados')
            msg.setText(message)
            msg.setStandardButtons(msg.StandardButton.Ok)
            msg.setIcon(msg.Icon.Critical)
            msg.exec_()

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
            Message.error(
                self.parent,
                'Codigo ja está em uso',
                f'O Código já está em uso por:\n{queryCod(cod)[0][1]}'
            )
            return
        if cod != notValid and des != notValid:
            try:
                pre = self.entPri.text().strip()
                pre = float(pre.replace(',', '.'))
                insertData(cod, des, pre)
                treeAdd(cod, des, pre)
                Message.sucess(
                    self.parent,
                    'cadastrado',
                    f'{des.upper()} cadastrado com sucesso'
                )
            except ValueError:
                Message.error(
                    self.parent, 
                    'Erro de Preço',
                    'Somente valor numerico no campo Preço.'
                )
        else:
            messageError('Código/Descrição devem conter valores!')
