import pymysql,os,sys
sys.path.append("..")
import db_operation.getdata as d

# 连接数据库并取出信息
def get_data(step):
    sql = 'select id,url_id,detail_text from academic_info LIMIT ' + str(step) + ', 1000'
    data = d.get_data(sql);
    return data

def save_as_txt(data):
    for row in data:
        id = row[0]
        school_id = ("000"+str(row[1]))[-4:]
        text = row[2]
        path = './data/' + str(school_id)
        if os.path.exists(path):pass
        else:os.makedirs(path)
        with open((path + '/' + str(school_id) + "-" + str(id)+".txt"),'w',encoding='UTF-8') as file:
            file.write(text)
            file.close()
            print("\r已保存 "+str(school_id)+"-"+str(id)+".txt",end="")

for i in range(324):
    data = get_data(i*1000)
    save_as_txt(data)