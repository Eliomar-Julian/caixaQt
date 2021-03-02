import sqlite3

con = sqlite3.connect('./data/database.db')
cur = con.cursor()
cur.execute(
	'CREATE TABLE IF NOT EXISTS produtos(cod TEXT, desc TEXT, pre FLOAT)'
)


def insertData(codi, prod, prec):
    cur.execute('INSERT INTO produtos(cod, desc, pre) VALUES (?,?,?)',
    	[codi, prod, prec]
    )
    con.commit()


def queryCod(search):
	list_ = cur.execute(F'SELECT * FROM produtos WHERE cod=?', [search])
	return list_.fetchall()

