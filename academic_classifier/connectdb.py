import pymysql
from sklearn import model_selection
import numpy as np
def prepare_datasets():
    conn = pymysql.connect(host='localhost', port = 3306, user = "root",password = "root",database = "test",charset= "utf8" )
    cursor = conn.cursor()
    sql1 = """select detail_text,academic_signal from academic_info_copy where (44090000<= id and id<=44091175 )"""  # 44250470 91页开头
    cursor.execute(sql1)
    data1 = cursor.fetchall()
    sql2 = """select content_text,text_signal from predict_table_dsy where (1520<= id and id<=6519)"""  # 44250470 91页开头
    cursor.execute(sql2)
    data2 = cursor.fetchall()
    sql4 = """select content_text,text_signal from predict_table_wbh where (31535<= id and id<=44522)"""  # 44250470 91页开头
    cursor.execute(sql4)
    data4 = cursor.fetchall()
    sql3 = """select content_text,text_signal from predict_table_xx where (31522<= id and id<=32521)"""  # 44250470 91页开头
    cursor.execute(sql3)
    # sql = """select detail_text,academic_signal from academic_info_copy where (44090000<= id and id<=44091175 )"""#那个academic搞成byte了不对44091175太大了
    data3 = cursor.fetchall()
    conn2 = pymysql.connect(host='localhost', port=3306, user="root", password="root", database="clear", charset="utf8")
    cursor2 = conn2.cursor()
    sql5 = """select content_text,text_signal from predict_table_med where text_signal = 0"""  # 44250470 91页开头
    cursor2.execute(sql5)
    data5 = cursor2.fetchall()
    data = data1+data2+data3+data4+data5
    X_train, X_test = model_selection.train_test_split(data,test_size=0.33,random_state=42)
    x_train,x_test = np.array(X_train),np.array(X_test)
    X_train,X_test = x_train[:,0],x_test[:,0]
    Y_train,Y_test = x_train[:,1],x_test[:,1]
    cursor.close()
    cursor2.close()
    conn.close()
    conn2.close()
    return X_train,Y_train,X_test,Y_test




