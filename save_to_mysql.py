import pymysql
#将需要单独处理的动态页面信息存入数据库

class save_to_database(object):
    def save_dynamicURL(data_list):
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='test', charset='utf8')  # 基本的本机MYSQL配置
        cursor = conn.cursor()
        sql = "insert into dynamic_urls VALUES (%s,%s,%s,%s,%s)"
        cursor.execute(sql, data_list)
        conn.commit()
        conn.close()

    #将入口网址为空的院校存入数据库
    def save_emptyURL(data_list):
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='test', charset='utf8')  # 基本的本机MYSQL配置
        cursor = conn.cursor()
        sql = "insert into empty_urls VALUES (%s,%s,%s,%s,%s)"
        cursor.execute(sql, data_list)
        conn.commit()
        conn.close()

    #将无法打开的入口链接信息存入数据库
    def save_refusedURLS(data_list):
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='test', charset='utf8')  # 基本的本机MYSQL配置
        cursor = conn.cursor()
        sql = "insert into refused_enter_urls VALUES (%s,%s,%s,%s,%s)"
        cursor.execute(sql, data_list)
        conn.commit()
        conn.close()

    #将列表页的信息存入数据库
    def save_listURLs(data_list):
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='test', charset='utf8')  # 基本的本机MYSQL配置
        cursor = conn.cursor()
        sql = "insert into list_urls VALUES (%s,%s,%s,%s)"
        cursor.executemany(sql, data_list)
        conn.commit()
        conn.close()

    def save_error_info(data_list):
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='test', charset='utf8')  # 基本的本机MYSQL配置
        cursor = conn.cursor()
        sql = "insert into error_info VALUES (%s,%s,%s)"
        cursor.executemany(sql, data_list)
        conn.commit()
        conn.close()

    #将详情页的信息存入数据库
    def save_academic_info(data_list):
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='test',
                               charset='utf8')  # 基本的本机MYSQL配置
        cursor = conn.cursor()
        sql = "insert into academic_info VALUES (%s,%s,%s,%s)"
        cursor.executemany(sql, data_list)
        conn.commit()
        conn.close()