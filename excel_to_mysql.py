#将一个excel文件中的入口url等信息存入数据库，每次处理一个文件
import pymysql
import xlrd

#读取excel文件并返回list
def get_data_from_excel():
    data = xlrd.open_workbook(r'C:\Users\OnePiece\PycharmProjects\academic_crawler\0129\张霁.xlsx')

    #data.sheets()[0]代表第1个工作表
    data_sheet = data.sheets()[0]
    rowNum = data_sheet.nrows  # sheet行数
    colNum = data_sheet.ncols  # sheet列数

    #获取所有单元格的内容,不包括表头
    list=[]
    for i in range(1,rowNum):
        rowlist = []
        for j in range(colNum):
            rowlist.append(data_sheet.cell(i,j).value)
        list.append(rowlist)
    print(list)
    return list

def save_to_database(data_list):
    conn = pymysql.connect(host = 'localhost', port = 3306, user = 'root', passwd = '123456', db = 'test',charset = 'utf8')  # 基本的本机MYSQL配置
    cursor = conn.cursor()
    sql = "insert into enter_urls VALUES (%s,%s,%s,%s,%s)"
    cursor.executemany(sql, data_list)
    conn.commit()
    conn.close()

if __name__=='__main__':
    a = get_data_from_excel()
    save_to_database(a)