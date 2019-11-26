import pymysql
#将需要单独处理的动态页面信息存入数据库
hostD = 'localhost'
portD = 3306
userD = 'crawler001'
passwdD = '123456'
dbD = 'acarep_crawler'
charsetD = 'utf8mb4'

class save_to_database(object):
    def save_dynamicURL(self,data_list):
        conn = pymysql.connect(host=hostD, port=portD, user=userD, passwd=passwdD, db=dbD, charset=charsetD)  # 基本的本机MYSQL配置
        cursor = conn.cursor()
        sql = "insert into dynamic_urls (university,school,first_page,second_page,detail_model) VALUES (%s,%s,%s,%s,%s)"
        cursor.execute(sql, data_list)
        conn.commit()
        conn.close()

    #将入口网址为空的院校存入数据库
    def save_emptyURL(self,data_list):
        conn = pymysql.connect(host=hostD, port=portD, user=userD, passwd=passwdD, db=dbD, charset=charsetD)  # 基本的本机MYSQL配置
        cursor = conn.cursor()
        sql = "insert into empty_urls (university,school,first_page,second_page,detail_model) VALUES (%s,%s,%s,%s,%s)"
        cursor.execute(sql, data_list)
        conn.commit()
        conn.close()

    #将无法打开的入口链接信息存入数据库
    def save_refusedURLS(self,data_list):
        conn = pymysql.connect(host=hostD, port=portD, user=userD, passwd=passwdD, db=dbD, charset=charsetD)  # 基本的本机MYSQL配置
        cursor = conn.cursor()
        sql = "insert into refused_enter_urls (university,school,first_page,second_page,detail_model) VALUES (%s,%s,%s,%s,%s)"
        cursor.execute(sql, data_list)
        conn.commit()
        conn.close()

    #将列表页的信息存入数据库
    def save_listURLs(self,data_list):
        conn = pymysql.connect(host=hostD, port=portD, user=userD, passwd=passwdD, db=dbD, charset=charsetD)  # 基本的本机MYSQL配置
        cursor = conn.cursor()
        sql = "insert into list_urls (university,school,list_url,detail_model) VALUES (%s,%s,%s,%s)"
        cursor.executemany(sql, data_list)
        conn.commit()
        conn.close()

    def save_error_info(self,data_list):
        conn = pymysql.connect(host=hostD, port=portD, user=userD, passwd=passwdD, db=dbD, charset=charsetD)  # 基本的本机MYSQL配置
        cursor = conn.cursor()
        sql = "insert into error_info VALUES (%s,%s,%s)"
        cursor.executemany(sql, data_list)
        conn.commit()
        conn.close()

    #将详情页的信息存入数据库
    def save_academic_info(self,data_list):
        conn = pymysql.connect(host=hostD, port=portD, user=userD, passwd=passwdD, db=dbD, charset=charsetD)  # 基本的本机MYSQL配置
        cursor = conn.cursor()
        sql = "insert into academic_info VALUES (%s,%s,%s,%s)"
        cursor.executemany(sql, data_list)
        conn.commit()
        conn.close()