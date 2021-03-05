import sqlite3

# // criação das tabelas

con = sqlite3.connect('./data/database.db')
cur = con.cursor()
cur.execute(
    'CREATE TABLE IF NOT EXISTS produtos(cod TEXT, desc TEXT, pre FLOAT)'
)
cur.execute(
    '''CREATE TABLE IF NOT EXISTS admin (
    adm TEXT NOT NULL,
    pas   TEXT NOT NULL,
    id    INTEGER UNIQUE,
    PRIMARY KEY("id" AUTOINCREMENT)
)'''
)

# // insere os dados nas colunas


def insertData(codi, desc, prec):
    cur.execute(
        'INSERT INTO produtos(cod, desc, pre) VALUES (?,?,?)',
        [codi, desc, prec]
    )
    con.commit()

# // retorna a lista de produtos de acordo com o codigo


def queryCod(search):
    list_ = cur.execute(f'SELECT * FROM produtos WHERE cod=?', [search])
    return list_.fetchall()

# // retorna a lista de produtos da busca dinamica...


def queryCodDynamic(search):
    list_ = cur.execute(
        f'SELECT * FROM produtos WHERE desc LIKE ? ORDER BY cod',
        ('%' + search + '%',)
    )
    return list_.fetchall()

# // busca a senha e adm do caixa


def queryAdmin(search):
    list_ = cur.execute(
        f'SELECT * FROM admin WHERE adm=?', [search])
    return list_.fetchall()
