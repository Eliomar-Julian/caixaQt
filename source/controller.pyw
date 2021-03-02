#!/usr/bin/python3

from interface import Interface
from PySide2 import QtWidgets
from crud import queryCod
import sys


class MyApp(Interface):

	TOTAL = float()

	def __init__(self):
		super(MyApp, self).__init__()
		self.entryCod.textEdited.connect(self.entryText)
		self.entryCod.returnPressed.connect(self.enterPress)
		self.btSearch.clicked.connect(self.searchItens)

	def entryText(self, e):
		self.qtd = '1'
		self.lista = []
		if '*' in e:
			indice = e.index('*')
			self.qtd = e[indice + 1:]
			self.lista = queryCod(e[:indice])
		else:
			self.lista = queryCod(e)

	def enterPress(self):
		if self.lista:
			item = QtWidgets.QTreeWidgetItem()
			item.setText(0, self.lista[0][1])
			item.setText(1, self.qtd + 'x')
			item.setText(2, 'R$ ' + str(self.lista[0][2]).replace('.', ','))
			self.tree.addTopLevelItem(item)
			valor = int(self.qtd) * self.lista[0][2]
			self.TOTAL += valor
			val = f'{valor:.2f}'
			item.setText(3, 'R$ ' + str(val).replace('.', ','))
			self.lbPriceCurrent.setText('R$ ' + str(valor).replace('.', ','))
			self.lbPriceTotal.setText(
				str('R$ %.2f' %(self.TOTAL)).replace('.', ',')
			)

	def searchItens(self):
		print('clicado')


if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	form = MyApp()
	form.show()
	sys.exit(app.exec_())