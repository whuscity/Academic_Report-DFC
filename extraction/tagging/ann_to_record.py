import pandas as pd
id = 44166575
id_school = 44
'''文本内容样例：
T300	姓名 5 8	汪寿阳
T301	姓名 41 44	汪寿阳
T303	姓名 233 236	许和连
T400	单位 24 35	湖南大学经济与贸易学院
T401	单位 237 248	湖南大学经济与贸易学院
T501	职称 148 150	教授
T502	职称 251 253	教授
T600	日期 198 203	5月19日
T1	单位 0 5	中国科学院
R1	报告人_单位 Arg1:T300 Arg2:T1	
R2	报告人_职称 Arg1:T300 Arg2:T501	
T2	日期 74 84	2019-05-14
T3	主题 45 59	谈政策研究和政策研究报告撰写
R3	日期_主题 Arg1:T3 Arg2:T2	
R4	报告人_主题 Arg1:T300 Arg2:T3	
R5	主持人_职称 Arg1:T303 Arg2:T502	
T4	报告人简介 123 194	汪寿阳 中国科学院特聘研究员、长江学者奖励计划特聘教授、博士生导师、国家杰出青年科学基金获得者、发展中国家科学院院士，国家系统与控制科学院院士
'''
with open("sampledata/{:0>4d}-{}.ann".format(id_school,id),encoding='utf-8') as f:
    lines = f.readlines()
    print(pd.DataFrame(lines))
    entities = []
    relations = []
    for line in lines:
        if(line[:1]=='T'):
            rec = line[:-1].split('\t')
            rec[1] = rec[1].split(' ')[0]
            entities.append(rec)
        elif(line[:1]=='R'):
            rec = line[:-1].split('\t')
            relation = rec[1].split(' ')
            relation[1] = relation[1].split(':')[1]
            relation[2] = relation[2].split(':')[1]
            relations.append(relation)
    entities_df = pd.DataFrame(entities)
    print(entities_df)
    print(pd.DataFrame(relations))

    for line in relations:
        line[1] = entities_df[entities_df[0] == line[1]][2].values[0]
        line[2] = entities_df[entities_df[0] == line[2]][2].values[0]

    name_topic = [None,None]
    name_title = [None,None]
    name_school = [None,None]
    topic_abstract = [None,None]
    host_title = [None,None]
    inviter_title = [None,None]
    inviter_school = [None,None]
    topic_date = [None,None]

    for relation in relations:
        if relation[0] == '报告人_主题': #报告人_主题	Arg1:姓名, Arg2:主题
            name_topic = [relation[1],relation[2]]
        elif relation[0] == '报告人_职称':#报告人_职称 	Arg1:姓名, Arg2:职称
            name_title = [relation[1], relation[2]]
        elif relation[0] == '报告人_单位':#报告人_单位	Arg1:姓名, Arg2:单位
            name_school = [relation[1], relation[2]]
        elif relation[0] == '摘要_主题':#摘要_主题  	Arg1:主题, Arg2:摘要
            topic_abstract = [relation[1], relation[2]]
        elif relation[0] == '主持人_职称':#主持人_职称	Arg1:姓名, Arg2:职称
            host_title = [relation[1], relation[2]]
        elif relation[0] == '邀请人_职称':#邀请人_职称	Arg1:姓名, Arg2:职称
            inviter_title = [relation[1],relation[2]]
        elif relation[0] == '邀请人_单位':#邀请人_单位	Arg1:姓名, Arg2:单位
            inviter_school = [relation[1],relation[2]]
        elif relation[0] == '日期_主题':#日期_主题		Arg1:主题, Arg2:日期
            topic_date = [relation[1],relation[2]]
            year = relation[2][:4]

    data = [id, id_school, topic_date[1], year, name_topic[1], name_topic[0], name_title[1], name_school[1],
            host_title[0], host_title[1],
            'host_school', inviter_title[0], inviter_title[1], inviter_school[1]]
    # data = [id,id_school,date,year,topic,reporter_name,reporter_title,reporter_school,host_name,host_title,host_school,inviter_name,inviter_title,inviter_school]
#  数据库各字段：
# （id,id_source,id_school,date,year,topic,
#   reporter_name,reporter_title,reporter_school,
#   host_name,host_title,host_school,
#   inviter_name,inviter_title,inviter_school,
#   operation_time)

print(data)
# 提取记录样例：
# [44166575, 44, '2019-05-14', '2019', '谈政策研究和政策研究报告撰写', '汪寿阳', '教授', '中国科学院', '许和连', '教授', 'host_school', None, None, None]