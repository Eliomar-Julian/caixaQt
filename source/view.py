from controller import MyApp, QtWidgets
import sys


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    form = MyApp()
    form.show()
    sys.exit(app.exec_())
