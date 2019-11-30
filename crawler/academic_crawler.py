#学术报告爬虫主程序
import re
import urllib
import urllib.request
import pymysql
import random
from bs4 import BeautifulSoup
from urllib import parse
from fnmatch import fnmatch,fnmatchcase #通配符匹配

#引入正文提取函数
from crawler.Html2Article import get_article
#引入存储数据库的方法
from crawler.save_to_mysql import save_to_database
save = save_to_database()
startid =1

#以下connect以及save_to_mysql都需要更改数据库参数
def get_enterURL_from_mysql():
    conn = pymysql.connect(host='localhost', port=3306, user='user', passwd='password', db='dbname',charset='utf8mb4')
    cursor = conn.cursor()
    #sql = 'select * from enter_urls where id >= '+str(startid) #从这里设定开始ID
    sql='select * from enter_urls where id BETWEEN 69 and 92'
    #sql = 'select * from enter_urls where id =5'
    cursor.execute(sql)
    data=cursor.fetchall()
    return data

#随机选择一个User-Agent
def get_headers():
    '''
    随机获取一个headers
    '''
    user_agents =  ["Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
                    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
                    "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
                    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
                    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
                    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
                    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
                    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
                    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
                    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
                    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5"
                    ]

    headers = {'User-Agent':random.choice(user_agents)}
    return headers

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
    #headers = {'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"}
    #代理IP池
    # proxy_list = [
    #     {"http": "111.177.188.246"},
    #
    #     {"http": "110.52.235.239"},
    #
    #     {"http": "125.126.194.11"},
    #
    #     {"http": "110.52.235.15"},
    #
    #     {"http": "111.177.182.136"},
    #
    #     {"http": "222.223.115.30"}
    # ]

    #需要单独处理的动态页面

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

        print('正在爬取：', university, school, '的学术报告信息')

        #从数据库读取的当前一条信息
        tmp_info = [id, first_page, second_page, detail_model]

        if first_page == '':
            print('入口网址信息为空')
            save.save_emptyURL(tmp_info)
            print('')

        elif is_dynamic_page(first_page,signal_var):
            print('动态加载页面，需要单独处理:', first_page)
            #dynamic_urls = tmp_info[:]
            print('')
            save.save_dynamicURL(tmp_info)
        else:
            #列表页第一页的链接
            first_page_info=[id,first_page,detail_model]
            list_urls.append(first_page_info)
            try:
                header = {"User-Agent": "Mozilla5.0 (Windows NT 6.1; WOW64; rv:59.0) Gecko/20100101 Firefox/59.0"}
                request = urllib.request.Request(first_page, headers=header)
                response = urllib.request.urlopen(request, timeout=10)
                soup = BeautifulSoup(response, 'html.parser')
                academic_urls_first_page = get_academic_urls(first_page, detail_model, soup)
                academic_urls.extend(academic_urls_first_page)

                #根据列表页第二页中的数字生成全部列表页
                r = re.compile('[0-9]+(?=[^0-9]*$)')
                if second_page is not None:
                    # #单独检查替换后数字为1的链接是否有效
                    # # 后两行的只能匹配链接最末尾的数字
                    new_url = r.sub('1', second_page)
                    #
                    # # #先匹配全部数字，返回列表，再自己选择位置替换
                    # # r = re.findall('[0-9]+', second_page)
                    # # new_url = second_page.replace(str(r[-2]),'1', 1)
                    try:
                        #     # # 随机选择一个代理
                        #     # proxy = random.choice(proxy_list)
                        #     #
                        #     # # 使用选择的代理构建代理处理器对象
                        #     # httpproxy_handler = urllib.request.ProxyHandler(proxy)
                        #     # opener = urllib.request.build_opener(httpproxy_handler)
                        #     # request = urllib.request.Request(new_url, headers=get_headers())
                        #     # response = opener.open(request)
                        header = {"User-Agent": "Mozilla5.0 (Windows NT 6.1; WOW64; rv:59.0) Gecko/20100101 Firefox/59.0"}
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
                        j=0  #特殊情况不报错直接跳过
                        print("特殊情况：" + university, school)
                    while j < signal_max and j > 0:
                        tmp_url = r.sub(str(j), second_page)
                        # r = re.findall('[0-9]+', second_page)
                        # tmp_url = second_page.replace(str(r[-2]), str(j), 1)
                        # tmp_url=second_page.strip().replace(a[-1],str(j))
                        # time.sleep(0.5)
                        try:
                            # # 随机选择一个代理
                            # proxy = random.choice(proxy_list)
                            #
                            # # 使用选择的代理构建代理处理器对象
                            # httpproxy_handler = urllib.request.ProxyHandler(proxy)
                            # opener = urllib.request.build_opener(httpproxy_handler)
                            # #request = urllib.request.Request(tmp_url, headers=get_headers())
                            # request = urllib.request.Request(tmp_url)
                            # #response=urllib.request.urlopen(request,timeout=3)
                            # response = opener.open(request)
                            header = {"User-Agent": "Mozilla5.0 (Windows NT 6.1; WOW64; rv:59.0) Gecko/20100101 Firefox/59.0"}
                            request = urllib.request.Request(tmp_url, headers=header)
                            response = urllib.request.urlopen(request, timeout=10)
                            soup = BeautifulSoup(response, 'html.parser')
                            academic_urls_one_page = get_academic_urls(tmp_url, detail_model, soup)
                            academic_urls.extend(academic_urls_one_page)
                            list_urls.append([university, school, tmp_url, detail_model])
                            if signal_rank == 0:
                                j -= 1
                                if j==1:break
                            elif signal_rank == 1:  j += 1

                        except:
                            continue
                #去重
                academic_urls = list(set(academic_urls))
                academic_info ,error_info = get_academic_text(id,academic_urls)
                # print(list_urls)
                # print(academic_urls)
                # print(len(academic_urls))
                # print(academic_info)
                # print(first_page,len(academic_info),'条')


                if len(academic_info)==0:
                    print('未能获取到任何内容，该网页可能为动态加载')
                    save.save_dynamicURL(tmp_info)
                    print('')
                else:
                    #逐学院存储全部列表页链接信息、学术报告信息、错误信息（循环执行一次存一次）
                    save.save_academic_info(academic_info)
                    save.save_listURLs(list_urls)
                    save.save_error_info(error_info)

            except Exception as e:  # 抛出异常
                save.save_refusedURLS(tmp_info)
                print('列表页错误:', str(e))
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
    # i=0
    for url in academic_urls:
        if not save.upload(url):continue
        # time.sleep(0.5)
        # print("进度:{0}%".format(round((i + 1) * 100 / len(academic_urls))), end="\r")
        # i+=1
        try:
            academic_text = get_article(url)
            # print(academic_text)
            academic_info.append([id,url,academic_text])
        except:
            print('获取学术报告文本失败')
            error_info.append([id,url])
    return (academic_info, error_info)

if __name__ == '__main__':
    a=get_enterURL_from_mysql()
    get_listURLs(a)
