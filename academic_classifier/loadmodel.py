import pickle
import pymysql
import numpy as np
from train_model import normalize_corpus

def prepare_datasets():
    conn = pymysql.connect(host='localhost', port = 3306, user = "root",password = "root",database = "clear",charset= "utf8" )
    cursor = conn.cursor()
    sql = """select id,detail_text from economic"""#1-5页末尾 10-15末页 20-25末  100-105末 125-130末
    cursor.execute(sql)
    data = cursor.fetchall()
    conn.close()
    return data
def load_predict_result(predict_result,data):
    # list1 = predict_result.tolist()
    # list2 = list(data)
    # listid = [i[0] for i in list2]
    # listcontent = [i[1] for i in list2]
    # list_insert = list(zip(listcontent,list1))
    # conn = pymysql.connect(host='localhost', port=3306, user="root", password="root", database="test", charset="utf8")
    # cursor = conn.cursor()
    # sql = """insert into predict_table(text,signal)VALUES (%s,%s)"""  # 那个academic搞成byte了不对44091175太大了
    # cursor.executemany(sql,list_insert)
    # conn.commit()
    # conn.close()
    list1 = predict_result.tolist()
    list2 = list(i[1] for i in data)
    listid = list(i[0] for i in data)
    list_insert = list(zip(listid,list2, list1))
    conn = pymysql.connect(host='localhost', port=3306, user="root", password="root", database="clear", charset="utf8")
    cursor = conn.cursor()
    sql = """insert into predict_table_economic(content_id,content_text,text_signal) VALUES (%s,%s,%s)"""  # 那个academic搞成byte了不对44091175太大了
    cursor.executemany(sql, list_insert)
    conn.commit()
    conn.close()

tfidf_svm = open("model.pkl", "rb")
classifier = pickle.load(tfidf_svm)
data = prepare_datasets()
data0 = np.array(data)[:,0]
data1 = np.array(data)[:,1]
######################################
#需要先对读入的文本进行处理提取出feature#
######################################
normalize_corpus_data = normalize_corpus(data1)  #之前训练没有用normalize
# vector = CountVectorizer(min_df=1, ngram_ra   nge=(1,1))
vector = pickle.load(open("vect.pkl",   'rb'))
# print(vector.vocabulary_)
predict_features = vector.transform(normalize_corpus_data)
predict_result = classifier.predict(predict_features)
load_predict_result(predict_result,data)
tfidf_svm.close()
