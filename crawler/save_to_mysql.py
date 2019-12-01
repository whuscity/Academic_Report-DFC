import pymysql
#将需要单独处理的动态页面信息存入数据库
hostD = 'localhost'
portD = 3306
userD = 'crawler001'
passwdD = '123456'
dbD = 'acarep_crawler'
charsetD = 'utf8mb4'

class save_to_database(object):
    #将动态页面的院校信息存入数据库
    def save_dynamicURL(self, data_list):
        conn = pymysql.connect(host=hostD, port=portD, user=userD, passwd=passwdD, db=dbD,
                               charset=charsetD)  # 基本的本机MYSQL配置
        cursor = conn.cursor()
        sql = "insert into dynamic_urls (id,first_page,second_page,detail_model) VALUES (%s,%s,%s,%s)"
        cursor.execute(sql, data_list)
        conn.commit()
        print('动态页面信息插入成功！')
        conn.close()

    # 将入口网址为空的院校存入数据库
    def save_emptyURL(self, data_list):
        conn = pymysql.connect(host=hostD, port=portD, user=userD, passwd=passwdD, db=dbD,
                               charset=charsetD)  # 基本的本机MYSQL配置
        cursor = conn.cursor()
        sql = "insert into empty_urls (id,first_page,second_page,detail_model) VALUES (%s,%s,%s,%s)"
        cursor.execute(sql, data_list)
        conn.commit()
        print('入口为空页面信息插入成功！')
        conn.close()

    # 将无法打开的入口链接信息存入数据库
    def save_refusedURLS(self, data_list):
        conn = pymysql.connect(host=hostD, port=portD, user=userD, passwd=passwdD, db=dbD,
                               charset=charsetD)  # 基本的本机MYSQL配置
        cursor = conn.cursor()
        sql = "insert into refused_enter_urls (id,first_page,second_page,detail_model) VALUES (%s,%s,%s,%s)"
        cursor.execute(sql, data_list)
        conn.commit()
        print('无法打开页面信息插入成功！')
        conn.close()

    # 将列表页的信息存入数据库
    def save_listURLs(self, data_list):
        conn = pymysql.connect(host=hostD, port=portD, user=userD, passwd=passwdD, db=dbD,
                               charset=charsetD)  # 基本的本机MYSQL配置
        cursor = conn.cursor()
        sql = "insert into list_urls (url_id,list_url,detail_model) VALUES (%s,%s,%s)"
        cursor.executemany(sql, data_list)
        conn.commit()
        print('列表页面信息插入成功！')
        conn.close()

    # 将访问错误的页面存入数据库
    def save_error_info(self, data_list):
        conn = pymysql.connect(host=hostD, port=portD, user=userD, passwd=passwdD, db=dbD,
                               charset=charsetD)  # 基本的本机MYSQL配置
        cursor = conn.cursor()
        sql = "insert into error_info(url_id,academic_url) VALUES (%s,%s)"
        cursor.executemany(sql, data_list)
        conn.commit()
        print('访问错误页面信息插入成功！')
        conn.close()

    # 将详情页的信息存入数据库
    def save_academic_info(self, data_list):
        conn = pymysql.connect(host=hostD, port=portD, user=userD, passwd=passwdD, db=dbD,
                               charset=charsetD)  # 基本的本机MYSQL配置
        cursor = conn.cursor()
        sql = "insert into academic_info (url_id,academic_url,detail_text) VALUES (%s,%s,%s)"
        cursor.executemany(sql, data_list)
        conn.commit()
        print('详情页面信息插入成功！')
        conn.close()

    # 判断是否爬取过
    def upload(self, url):
        conn = pymysql.connect(host=hostD, port=portD, user=userD, passwd=passwdD, db=dbD,
                               charset=charsetD)
        cursor = conn.cursor()
        sql = 'select id from academic_info where academic_url="{}"'.format(url)  # url唯一所以可以用作条件进行查询
        cursor.execute(sql)
        data = cursor.fetchall()
        if data:  # 如果存在就证明重复，不进行保存操作，返回False
            print(url, '已经爬取过。。。')
            return False
        else:
            return True
