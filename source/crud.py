import sqlite3

con = sqlite3.connect('./data/database.db')
cur = con.cursor()
cur.execute(
    'CREATE TABLE IF NOT EXISTS produtos(cod TEXT, desc TEXT, pre FLOAT)'
)


def insertData(codi, desc, prec):
    cur.execute(
        'INSERT INTO produtos(cod, desc, pre) VALUES (?,?,?)',
        [codi, desc, prec]
    )
    con.commit()


def queryCod(search):
    list_ = cur.execute(f'SELECT * FROM produtos WHERE cod=?', [search])
    return list_.fetchall()


def queryCodDynamic(search):
    list_ = cur.execute(
        f'SELECT * FROM produtos WHERE desc LIKE ? ORDER BY cod',
        ('%' + search + '%',)
    )
    return list_.fetchall()
