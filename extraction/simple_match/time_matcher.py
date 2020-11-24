import re,sys
sys.path.append("..")
import db_operation.getdata as get
import db_operation.insertdata as insert


date_1 = r"([0-9]+年[0-9]+月[0-9]+日)" #|([0-9]+月[0-9]+日)
date_2 = r"([零〇一二三四五六七八九]年[十]?[一二三四五六七八九]月[一二三]?[十]?[一二三四五六七八九十]日)"
date_3 = r"([0-9]+月[0-9]+日)"

date_4 = r"20[0-2][0-9]-[12]?[0-9]-[1-3]?[0-9]"
date_5 = r"20[0-2][0-9]\.[12]?[0-9]\.[1-3]?[0-9]"
date_6 = r"20[0-2][0-9]\/[12]?[0-9]\/[1-3]?[0-9]"

for i in range(119,120):
    step = i*1000
    data = get.get_data("SELECT id, url_id, detail_text FROM academic_info LIMIT "+str(step)+",1000")
    timedata = []
    iterlist = []
    sql = "insert into time_regex(id,url_id,time_str,start_index,end_index) VALUES (%s,%s,%s,%s,%s) "

    for row in data:
        id = row[0]
        url_id = row[1]
        flag = False
        ## 方式1
        pattern = re.compile(date_1)
        iter = pattern.finditer(row[2])
        for record in iter:
            timedata.append(tuple([id,url_id,record.group(),record.span()[0],record.span()[1]]))
            flag = True

        if(flag is False):
            pattern = re.compile(date_3)
            iter = pattern.finditer(row[2])
            for record in iter:
                timedata.append(tuple([id, url_id, record.group(), record.span()[0], record.span()[1]]))

        ## 方式2
        pattern = re.compile(date_2)
        iter = pattern.finditer(row[2])
        for record in iter:
            timedata.append(tuple([id, url_id, record.group(), record.span()[0], record.span()[1]]))

    # print(len(timedata))
    print(timedata)
    insert.insert_data(sql, timedata)
