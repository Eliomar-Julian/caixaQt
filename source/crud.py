import sqlite3

# // criação das tabelas

con = sqlite3.connect('./data/database.db')
cur = con.cursor()
pro = 'CREATE TABLE IF NOT EXISTS produtos(cod TEXT, desc TEXT, pre FLOAT)'
adm = '''CREATE TABLE iF NOT EXISTS admin (
    adm TEXT NOT NULL UNIQUE,
    pas   TEXT NOT NULL,
    id    INTEGER UNIQUE,
    PRIMARY KEY("id" AUTOINCREMENT))'''
cur.execute(pro)
cur.execute(adm)


def insertData(codi: str, desc: str, prec: float) -> None:
    command = 'INSERT INTO produtos(cod, desc, pre) VALUES (?,?,?)'
    cur.execute(command, [codi, desc, prec])
    con.commit()


def queryCod(search) -> list:
    list_ = cur.execute(f'SELECT * FROM produtos WHERE cod=?', [search])
    return list_.fetchall()


def queryCodDynamic(search) -> list:
    command = f'SELECT * FROM produtos WHERE desc LIKE ? ORDER BY cod'
    list_ = cur.execute(command, ('%' + search + '%',))
    return list_.fetchall()


def queryAdmin(search) -> list:
    list_ = cur.execute(f'SELECT * FROM admin WHERE adm=?', [search])
    return list_.fetchall()


def queryAll() -> list:
    list_ = cur.execute('SELECT * FROM produtos ORDER BY desc')
    return list_.fetchall()


def queryAndDelete(search) -> bool:
    try:
        cur.execute('DELETE FROM produtos WHERE desc = ?', [search])
        con.commit()
        return True
    except Exception:
        return False


def insert_user(user: str, password: str) -> None:
    try:
        cur.execute('INSERT INTO admin(adm, pas) VALUES (?,?)', [user, password])
        con.commit()
        return True
    except:
        return False


def load_null_users()-> bool:
   list_ =  cur.execute('SELECT * FROM admin WHERE adm = adm')
   verify = list_.fetchall() 
   if len(verify) != 0:
       return True
   return False


def load_admins() -> None:
    list_ = cur.execute('SELECT * FROM admin ORDER BY adm')
    return list_.fetchall()


def delete_admins(adm: str) -> None:
    cur.execute('DELETE FROM admin WHERE adm = ?', [adm])
    con.commit()
