from PySide2 import QtGui, QtCore
from controller import MyApp, QtWidgets
from crud import load_null_users, insert_user
from menu import Message
import sys


def if_not_admin(parent: QtWidgets.QWidget) -> None:
    load = load_null_users()
    if not load:
        def cad()-> None:
            ent1 = ent_name.text().strip()
            ent2 = ent_pass.text().strip()
            if ent1 == '':
                msg = 'O nome não pode estar em branco'
                Message.error(parent, 'erro', msg)
                return
            capture = insert_user(ent1, ent2)
            if not capture:
                msg = 'O nome do administrador já existe, tente outro'
                Message.error(parent, 'erro', msg)
                return
            root.close()
            msg = 'Administrador cadastrado com sucesso!'
            Message.sucess(parent, 'Cadastrado', msg)

        root = QtWidgets.QDialog(parent)
        layout = QtWidgets.QGridLayout(root)
        lb1 = QtWidgets.QLabel('Nome')
        lb2 = QtWidgets.QLabel('Senha')
        ent_name = QtWidgets.QLineEdit()
        ent_pass = QtWidgets.QLineEdit()
        bt = QtWidgets.QPushButton('Cadastrar')
        root.resize(400, 300)
        ent_pass.setEchoMode(QtWidgets.QLineEdit.Password)
        root.setWindowTitle("Cadastre o primeiro administrador")
        bt.clicked.connect(cad)
        layout.addWidget(lb1, 0, 0)
        layout.addWidget(lb2, 1, 0)
        layout.addWidget(ent_name, 0, 1)
        layout.addWidget(ent_pass, 1, 1)
        layout.addWidget(bt)
        root.exec_()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    form = MyApp()
    form.setWindowTitle("CaixaQt | PDV sistema")
    form.setWindowIcon(QtGui.QIcon("images/cart.png"))
    form.showMaximized()
    if_not_admin(form)
    form.show()
    sys.exit(app.exec_())
