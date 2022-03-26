import mysql.connector
import configparser

# // lendo configurações do banco de dados do usuario

config = configparser.ConfigParser()
config.read('./mysql-server.ini')
connec = [
    config['Server-mysql']['host'],
    config['Server-mysql']['user'],
    config['Server-mysql']['password'],
    config['Server-mysql']['database'],
]

# // criação das tabelas

con = mysql.connector.connect(
    host=connec[0], user=connec[1], 
    password=connec[2], database=connec[3]
)
cur = con.cursor()
cur.execute(
    '''CREATE TABLE IF NOT EXISTS produtos (
    cod VARCHAR(30), des VARCHAR(100), pre FLOAT);'''
)
cur.execute(
    '''CREATE TABLE IF NOT EXISTS admin (
        `adm` VARCHAR(100) NOT NULL UNIQUE, 
        `pas` VARCHAR(20) NOT NULL, 
        `id` INT AUTO_INCREMENT UNIQUE, 
        PRIMARY KEY(`id`));'''
)


def insertData(codi: str, desc: str, prec: float) -> None:
    command = 'INSERT INTO produtos (cod, des, pre) VALUES (%s, %s , %s);'
    cur.execute(command, (codi, desc, prec))
    con.commit()


def queryCod(search) -> list:
    cur.execute(f"SELECT * FROM produtos WHERE cod = '%s';" % (search))
    return cur.fetchall()


def queryCodDynamic(search) -> list:
    command = "SELECT * FROM produtos WHERE des LIKE '%s' ORDER BY `cod`;"
    cur.execute(command %('%'+search+'%'))
    return cur.fetchall()


def queryAdmin(search) -> list:
    cur.execute("SELECT * FROM admin WHERE adm LIKE '%s';" % (search))
    return cur.fetchall()


def queryAll() -> list:
    cur.execute('SELECT * FROM produtos ORDER BY des;')
    return cur.fetchall()


def queryAndDelete(search) -> bool:
    try:
        cur.execute("DELETE FROM produtos WHERE des = '%s';" % (search))
        con.commit()
        return True
    except Exception:
        return False


def insert_user(user: str, password: str) -> None:
    try:
        cur.execute('INSERT INTO admin(adm, pas) VALUES (%s, %s);', 
            (user, password))
        con.commit()
        return True
    except:
        return False


def load_null_users()-> bool:
   cur.execute('SELECT * FROM admin WHERE adm = adm;') 
   verify = cur.fetchall()
   if len(verify) != 0:
       return True
   return False


def load_admins() -> None:
    cur.execute('SELECT * FROM admin ORDER BY adm;')
    return cur.fetchall()


def delete_admins(adm: str) -> None:
    cur.execute("DELETE FROM admin WHERE adm = '%s';" % (adm))
    con.commit()

