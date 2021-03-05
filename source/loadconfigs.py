def getStyle():
    with open(file='./config/style.qss', mode='r', encoding='UTF-8') as style:
        return style.read()


def getDefaultStyle():
    ...


def saveTotal(val):
    from datetime import datetime
    date_ = datetime.now().strftime('%H:%M')
    record = f'{date_} = {val}\n'
    print(date_)
    with open('./data/saldo.sd', 'a+', encoding='utf-8') as saldo:
        saldo.write(record)
