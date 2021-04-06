from config.config_param import RDS_Chengdu as DBConfig
import pymysql

class item:
    def __init__(self):
        self.title = None
        self.schName = None
        self.schSchool = None
        self.hostSchool = None
        self.date = None
        self.url = None
        self.id_source = None


def get_list():
    hostD, portD, userD, passwdD, dbD = DBConfig()
    conn = pymysql.connect(host=hostD, port=portD, user=userD, passwd=passwdD, db=dbD)
    cursor = conn.cursor()
    sql = '''
        SELECT id_source,date,topic,reporter_name,reporter_school,enter_urls.university,enter_urls.school 
        FROM report, enter_urls
        where report.id_school = enter_urls.id
        and 1=1
        LIMIT 0,10
    '''
    cursor.execute(sql)
    data = cursor.fetchall()
    # print(list(data))
    items = []
    for row in data:
        listitem = item()
        listitem.id_source = row[0]
        listitem.date = row[1]
        listitem.title = row[2]
        listitem.schName = row[3]
        listitem.schSchool = row[4]
        listitem.hostSchool = row[5] + row[6]
        items.append(listitem)
    cursor.close()
    conn.close()
    return items

print(get_list())