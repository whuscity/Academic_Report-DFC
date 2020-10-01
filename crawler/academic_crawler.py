#学术报告爬虫主程序
import re
import urllib
import urllib.request
import time
import ssl

import pymysql
import random
from bs4 import BeautifulSoup
from urllib import parse
from fnmatch import fnmatch,fnmatchcase #通配符匹配

#引入正文提取函数
from Html2Article import get_article
#引入存储数据库的方法
from save_to_mysql import save_to_database
save = save_to_database()
startid =1
dup_flag = False #如果某个学校存在重复爬取则置True，以防非动态页面插入dynamic表



#以下connect以及save_to_mysql都需要更改数据库参数
def get_enterURL_from_mysql():
    conn = pymysql.connect(host='47.100.78.223', port=3306, user='PM', passwd='888888', db='AcademicReport',charset='utf8')
    cursor = conn.cursor()
    #sql = 'select * from enter_urls where id >= '+str(startid) #从这里设定开始ID
    sql='select * from enter_urls where enter_urls.id > 1000'
    # sql = 'select enter_urls.id,enter_urls.university,enter_urls.school,enter_urls.first_page,enter_urls.second_page,enter_urls.detail_model,enter_urls.signal_rank,enter_urls.signal_var,enter_urls.signal_max from enter_urls,refused_enter_urls where enter_urls.id = refused_enter_urls.id and enter_urls.id > 1236'
    #sql = 'select * from enter_urls where id =5'dd
    cursor.execute(sql)
    data=cursor.fetchall()
    return data


#判断是否为动态页面
def is_dynamic_page(url,signal_var):
    if signal_var is not None:return False
    elif url is not None:
        if url.find('jsp?') >= 0:
            return True
        # elif url.find('php?') >= 0:
        #     return True
        elif url.find('aspx?') >= 0:
            return True
        # elif url.find('asp?') >= 0:
        #     return True
        elif url.find('html?') >= 0:
            return True
        elif url.find('list?') >= 0:
            return True

#生成全部的列表页url，并获取学术详情页的链接和文本内容
def get_listURLs(data):
    for i in range(len(data)):
        list_urls = []
        academic_urls=[]
        academic_info=[]
        error_info=[]

        id = data[i][0]                       #学校和学院对应的id
        university = data[i][1].strip()
        school = data[i][2].strip()
        first_page = data[i][3]              #第一页
        second_page = data[i][4]            #第二页
        detail_model = data[i][5]           # 详情页模式，采用通配符
        signal_rank = data[i][6]            # 列表页url变化规律，0为升序，1为降序 ，2为其他
        signal_var = data[i][7]             # 列表页url如有绑定字段，在此处记录
        signal_max = data[i][8]             # 列表页在最初采集时的规模（列表页页数）

        print('*正在爬取：', university, school, '的学术报告信息')

        #从数据库读取的当前一条信息
        tmp_info = [id, first_page, second_page, detail_model]

        if first_page is None:
            print('入口网址信息为空')
            save.save_emptyURL(tmp_info)
            print('')

        elif is_dynamic_page(first_page,signal_var):
            print('动态加载页面，需要单独处理:', first_page)
            print('')
            save.save_dynamicURL(tmp_info)
        else:
            #列表页第一页的链接
            first_page_info=[id,first_page,detail_model]
            list_urls.append(first_page_info)
            try:
                header = {"User-Agent": "Baiduspider"}
                request = urllib.request.Request(first_page, headers=header)
                response = urllib.request.urlopen(request, timeout=10)
                soup = BeautifulSoup(response, 'html.parser')
                academic_urls_first_page = get_academic_urls(first_page, detail_model, soup)
                academic_urls.extend(academic_urls_first_page)

                #根据列表页第二页中的数字生成全部列表页
                if(signal_var is None or signal_var == ""):
                    r = re.compile('[0-9]+(?=[^0-9]*$)')
                else:r = re.compile(signal_var+'=?[0-9]*')
                if second_page is not None:
                    # #单独检查替换后数字为1的链接是否有效
                    # # 后两行的只能匹配链接最末尾的数字
                    new_url = r.sub('1', second_page)

                    try:
                        header = {"User-Agent": "Baiduspider"}
                        request = urllib.request.Request(new_url, headers=header)
                        response = urllib.request.urlopen(request, timeout=10)
                        soup = BeautifulSoup(response, 'html.parser')
                        academic_urls_one_page = get_academic_urls(new_url, detail_model, soup)
                        academic_urls.extend(academic_urls_one_page)

                        list_urls.append([id,new_url,detail_model])
                    except:
                        print('替换末位数字为1的列表页链接无效')

                    #通过循环生成非首页列表页
                    second_num = r.findall(second_page)
                    if signal_rank == 0:
                        j = signal_max  #升序：（时间顺序）“反爬”，从最后一页开始
                    elif signal_rank == 1:
                        j = 1           #降序：（时间顺序）“反爬”，从最后一页开始
                    else:
                        j=-1  #特殊情况不报错直接跳过
                        print("特殊情况：" + university, school)
                        save.save_dynamicURL(tmp_info)
                    while j <= signal_max and j > 0:
                        tmp_url = r.sub(str(j), second_page)

                        try:
                            header = {"User-Agent": "Baiduspider"}
                            print(j,end=" ")
                            request = urllib.request.Request(tmp_url, headers=header)
                            response = urllib.request.urlopen(request, timeout=10)
                            soup = BeautifulSoup(response, 'html.parser')
                            academic_urls_one_page = get_academic_urls(tmp_url, detail_model, soup)
                            academic_urls.extend(academic_urls_one_page)
                            list_urls.append([id, tmp_url, detail_model])
                            if signal_rank == 0:
                                j -= 1
                            elif signal_rank == 1:  j += 1

                        except:
                            if signal_rank == 0:
                                j -= 1
                            elif signal_rank == 1:  j += 1
                            continue

                print("\r状态：学术报告详情页url获取成功。",end="")
                dup_flag = False
                academic_urls = list(set(academic_urls)) #去重
                academic_info ,error_info = get_academic_text(id,academic_urls)

                print("\r状态：爬取完成。存储中", end="")
                if len(academic_info)==0 and not dup_flag:
                    print('\r该学院未能获取到任何内容，该网页可能为动态加载')
                    save.save_dynamicURL(tmp_info)
                    print('')
                else:
                    #逐学院存储全部列表页链接信息、学术报告信息、错误信息（循环执行一次存一次）
                    save.save_academic_info(academic_info)
                    save.save_listURLs(list_urls)
                    save.save_error_info(error_info)
                    save.delete_from_error(id)

            except Exception as e:  # 抛出异常
                tmp_info.append(str(e))
                save.save_refusedURLS(tmp_info)
                print('\r列表页错误:', str(e))
                print('')



#获取某一列表页的所有学术url
def get_academic_urls(page_url,detail_model,soup):
    links = soup.find_all('a')
    #列表页的所有链接
    all_links=[]
    #所有的学术链接
    academic_urls=[]

    for link in links:
        new_url = link.get('href')
        new_full_url = urllib.parse.urljoin(page_url, new_url)
        #print(new_full_url)
        all_links.append(new_full_url)
    #列表去重
    all_links=list(set(all_links))
    for current_url in all_links:
        if fnmatch(current_url,detail_model+'*'):
            academic_urls.append(current_url)
    academic_urls = list(set(academic_urls))
    return academic_urls

def get_academic_text(id,academic_urls):
    academic_info=[]
    error_info=[]
    count=0
    for url in academic_urls:
        count += 1
        if not save.upload(url):continue #没有保存过，则继续
        else: dup_flag = True
        try:
            academic_text = get_article(url)
            print("\r状态：该学院已爬取{}/{}学术报告。".format(count,len(academic_urls)),end="")
            academic_info.append([id,url,academic_text])
        except:
            print('\r获取学术报告文本失败',end="")
            error_info.append([id,url])
    return (academic_info, error_info)

if __name__ == '__main__':
    a=get_enterURL_from_mysql()
    ssl._create_default_https_context = ssl._create_unverified_context
    get_listURLs(a)
