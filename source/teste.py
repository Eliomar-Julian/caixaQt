import mysql.connector

con = mysql.connector.connect(host='localhost', user='root', password='asd123', database='cadastro')
cur = con.cursor()



cur.execute('CREATE TABLE IF NOT EXISTS produtos (cod VARCHAR(10), des VARCHAR(100), pre FLOAT);')
cur.execute('CREATE TABLE IF NOT EXISTS admin (`adm` VARCHAR(100) NOT NULL UNIQUE, `pas` VARCHAR(20) NOT NULL, `id` INT AUTO_INCREMENT UNIQUE, PRIMARY KEY(`id`));')

print(cur.fetchall())

