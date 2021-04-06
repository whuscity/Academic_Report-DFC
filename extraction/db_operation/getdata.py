import pymysql
from db_operation.config_param import get_db

def get_data(sql):
    hostD, portD, userD, passwdD, dbD, charsetD = get_db()
    conn = pymysql.connect(host=hostD, port=portD, user=userD, passwd=passwdD, db=dbD, charset=charsetD)
    cursor = conn.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    return data
