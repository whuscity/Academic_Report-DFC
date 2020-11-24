import pymysql,os,sys,re
sys.path.append("..")
import db_operation.getdata as d

# 连接数据库并取出信息
def get_data(step):
    sql = 'select id,url_id,detail_text from academic_info where model_predict = 1 LIMIT ' + str(step) + ', 1000'
    data = d.get_data(sql);
    return data

def save_as_txt(data):
    from ltp import LTP
    import random
    ltp = LTP()
    for row in data:
        id = row[0]
        school_id = ("000"+str(row[1]))[-4:]
        texts = row[2]
        textlines = texts.split('\n')
        shortened_textlines = []
        for line in textlines:
            line_len = len(line)
            if line_len > 100:
                for i in range(line_len // 100):
                    shortened_textlines.append(line[i*100:(i+1)*100])
            else: shortened_textlines.append(line)
        text = ' '.join(shortened_textlines)
        path = './data/' + str(school_id)
        if os.path.exists(path):pass
        else:os.makedirs(path)
        with open((path + '/' + str(school_id) + "-" + str(id)+".txt"),'w',encoding='UTF-8') as file:
            file.write(text)
            file.close()
            print("\r已保存 "+str(school_id)+"-"+str(id)+".txt",end="")
            # T2	报告人 68 71	曹进德
            # R2 报告人_单位 Arg1: T2 Arg2: T1
        seg,hidden = ltp.seg([text])
        ner = ltp.ner(hidden)
        ner_info = []
        entities_nh = []
        entities_ni = []
        print(type(text))
        print()
        for i in ner[0]:
            if (i[0] == 'Nh'):
                start = i[1]
                end = i[2]
                entity = "".join(seg[0][start:end + 1])
                if(len(entity)>1):
                    entities_nh.append(entity)

            elif (i[0] == 'Ni'):
                start = i[1]
                end = i[2]
                entity = "".join(seg[0][start:end + 1])
                if entity in schoolnames:
                    entities_ni.append(entity)

        for entity in set(entities_nh):
            pattern = re.compile(entity)
            iter = pattern.finditer(text)
            count = 0
            for record in iter:
                ner_info.append("T" + str(300+count) + "\t姓名 " + str(record.span()[0]) + " " + str(
                    record.span()[1]) + "\t" + str(record.group()) + "\n")
                count += 1

        for entity in set(entities_ni):
            pattern = re.compile(entity)
            iter = pattern.finditer(text)
            count = 0
            for record in iter:
                ner_info.append("T" + str(400+count) + "\t单位 " + str(record.span()[0]) + " " + str(
                    record.span()[1]) + "\t" + str(record.group()) + "\n")
                count += 1

        pattern = re.compile('教授|副教授|讲师|研究员|副研究员|助理教授|助理研究员')
        iter = pattern.finditer(text)
        count = 0
        for record in iter:
            ner_info.append("T" + str(500 + count) + "\t职称 " + str(record.span()[0]) + " " + str(
                record.span()[1]) + "\t" + str(record.group()) + "\n")
            count += 1

        date_1 = r"([0-9]+年[0-9]+月[0-9]+日)"  # |([0-9]+月[0-9]+日)
        date_2 = r"([零〇一二三四五六七八九]年[十]?[一二三四五六七八九]月[一二三]?[十]?[一二三四五六七八九十]日)"
        date_3 = r"([0-9]+月[0-9]+日)"
        flag = False
        count = 0
        ## 方式1
        pattern = re.compile(date_1)
        iter = pattern.finditer(text)
        for record in iter:
            ner_info.append("T" + str(600 + count) + "\t日期 " + str(record.span()[0]) + " " + str(
                record.span()[1]) + "\t" + str(record.group()) + "\n")
            count += 1
            flag = True

        if (flag is False):
            pattern = re.compile(date_3)
            iter = pattern.finditer(text)
            for record in iter:
                ner_info.append("T" + str(600 + count) + "\t日期 " + str(record.span()[0]) + " " + str(
                    record.span()[1]) + "\t" + str(record.group()) + "\n")
                count += 1

        ## 方式2
        pattern = re.compile(date_2)
        iter = pattern.finditer(text)
        for record in iter:
            ner_info.append("T" + str(600 + count) + "\t日期 " + str(record.span()[0]) + " " + str(
                record.span()[1]) + "\t" + str(record.group()) + "\n")
            count += 1

        with open((path + '/' + str(school_id) + "-" + str(id)+".ann"),'w',encoding='UTF-8') as file:
            print([text])
            print(ner_info)
            file.writelines(ner_info)
            file.close()
            print("\r已保存 "+str(school_id)+"-"+str(id)+".ann",end="")




txt = open("schoolnames.txt",mode='r',encoding='UTF-8').readlines()
schoolnames = []
for line in txt:
    schoolnames.append(line.replace("\n",""))
print(schoolnames)

for i in range(1):
    data = get_data(i*1000)
    save_as_txt(data)
