def getStyle():
	with open(file='./source/style.qss', mode='r', encoding='UTF-8') as style:
		return style.read()