import pymysql
from db_operation.getdb import get_db

def exesql(sql):
    hostD, portD, userD, passwdD, dbD, charsetD = get_db()
    conn = pymysql.connect(host=hostD, port=portD, user=userD, passwd=passwdD, db=dbD, charset=charsetD)
    cursor = conn.cursor()
    cursor.execute(sql)
    cursor.close()
    conn.commit()
    conn.close()

def insert_data(sql,data):
    hostD, portD, userD, passwdD, dbD, charsetD = get_db()
    conn = pymysql.connect(host=hostD, port=portD, user=userD, passwd=passwdD, db=dbD, charset=charsetD)
    cursor = conn.cursor()
    cursor.executemany(sql,data)
    cursor.close()
    conn.commit()
    conn.close()