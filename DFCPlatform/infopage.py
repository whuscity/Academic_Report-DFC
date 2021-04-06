from config.config_param import RDS_Chengdu as DBConfig
import pymysql

class item:
    def __init__(self):
        self.title = None
        self.schName = None
        self.schTitle = None
        self.schSchool = None
        self.date = None
        self.hostSchool = None
        self.hostName = None
        self.hostTitle = None
        self.inviteName = None
        self.inviteTitle = None
        self.abstract = None
        self.schBiography = None
        self.id_source = None
        self.url = None
        self.prevTitle = None
        self.prevId = None
        self.nextTitle = None
        self.nextId = None

def getinfo(id):
    hostD, portD, userD, passwdD, dbD = DBConfig()
    conn = pymysql.connect(host=hostD, port=portD, user=userD, passwd=passwdD, db=dbD)
    cursor = conn.cursor()
    sql = '''
         select id_source,date,topic,reporter_name,reporter_title,reporter_school,host_name,host_title,university,school,inviter_name,inviter_title,academic_url,id
         from
            (SELECT id_source,date,topic,reporter_name,reporter_title,reporter_school,host_name,host_title,enter_urls.university,enter_urls.school,inviter_name,inviter_title,academic_info.academic_url,report.id
                FROM report,enter_urls,academic_info
				where report.id_school = enter_urls.id and report.id_source = academic_info.id) it
				where id_source = %s
    ''' % id
    # print(sql)
    cursor.execute(sql)
    data = cursor.fetchall()
    sql2 = '''
        SELECT id_source,topic
        FROM report 
        WHERE id in 
        (SELECT max(id) 
        FROM report
        WHERE id < %s)
    ''' % data[0][13]
    sql3 = '''
    SELECT id_source,topic
    FROM report 
    WHERE id in 
        (SELECT min(id) 
        FROM report
        WHERE id > %s)
    ''' % data[0][13]
    cursor.execute(sql2)
    data2 = cursor.fetchall()
    cursor.execute(sql3)
    data3 = cursor.fetchall()
    items = []
    for row in data:
        listitem = item()
        listitem.id_source = row[0]
        listitem.date = row[1]
        listitem.title = row[2]
        listitem.schName = row[3]
        listitem.schTitle = row[4]
        listitem.schSchool = row[5]
        listitem.hostName = row[6]
        listitem.hostTitle = row[7]
        listitem.hostSchool = row[8] + row[9]
        listitem.inviteName = row[10]
        listitem.inviteTitle = row[11]
        listitem.url = row[12]
        if data2:
            listitem.prevTitle = data2[0][1]
            listitem.prevId = data2[0][0]
        if data3:
            listitem.nextTitle = data3[0][1]
            listitem.nextId = data3[0][0]
        items.append(listitem)


    cursor.close()
    conn.close()
    return items