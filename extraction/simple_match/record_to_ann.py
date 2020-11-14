import pymysql,os,sys
sys.path.append("..")
import db_operation.getdata as getdata

# 连接数据库并取出信息
def get_data(step):
    sql = 'select id,url_id,time_str,start_index,end_index from time_regex LIMIT ' + str(step) + ', 1000'
    data = getdata.get_data(sql);
    return data

def save_as_ann(data):
    n = 1
    for row in data:
        n += 1
        n = n % 8
        n = n + 1000
        id = row[0]
        school_id = ("000"+str(row[1]))[-4:]
        text = row[2]
        start_index = row[3]
        end_index = row[4]
        text = "T"+str(n)+"\t时间 " + str(start_index) + " " +str(end_index) + "\t" + text+"\n"
        path = './data/' + str(school_id)
        if os.path.exists(path):pass
        else:os.makedirs(path)
        with open((path + '/' + str(school_id) + "-" + str(id)+".ann"),'a+',encoding='UTF-8') as file:
            file.write(text)
            file.close()
            print("\r已保存 "+str(school_id)+"-"+str(id)+".ann",end="")

for i in range(1):
    data = get_data(i*1000)
    save_as_ann(data)