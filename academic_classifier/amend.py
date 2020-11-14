import pymysql

conn = pymysql.connect(host='localhost', port=3306, user="root", password="root", database="clear", charset="utf8")
cursor = conn.cursor()
sql = """select id,content_text from predict_table_economic where text_signal = 0"""  # 1-5页末尾 10-15末页 20-25末  100-105末 125-130末
cursor.execute(sql)
data = cursor.fetchall()
conn.close()

conn = pymysql.connect(host='localhost', port=3306, user="root", password="root", database="clear", charset="utf8")
cursor = conn.cursor()
for i in data:
    # print(i)
    if "报告" in i[1] or "讲座" in i[1] or "论坛" in i[1] or "主讲" in i[1]:
        sql = "update predict_table_economic set text_signal = 1 where (id ="+str(i[0])+ ")"
        # sql = """select id,content_text from predict_table_med where text_signal = 0"""  # 1-5页末尾 10-15末页 20-25末  100-105末 125-130末
        cursor.execute(sql)
conn.commit()
conn.close()