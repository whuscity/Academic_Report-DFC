import pymysql,os,sys
sys.path.append("..")
import db_operation.getdata as getdata

# 连接数据库并取出信息
def get_data():
    sql = 'select DISTINCT university, school from enter_urls'
    data = getdata.get_data(sql);
    return data


def save_as_txt(data):
    fullnamelist = []
    univlist = []
    for row in data:
        fullnamelist.append(row[0] + row[1]+"\n")
        univlist.append(row[0]+"\n")
    with open("schoolnames.txt",mode='w',encoding='utf-8') as f:
        # for row in fullnamelist:
        f.writelines(fullnamelist+list(tuple(univlist)))
        f.close()

save_as_txt(get_data())