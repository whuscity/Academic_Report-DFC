# Academic-Report_Crawler
### 双一流院校学术报告通知信息采集。 

    包含的代码：
    1.handle_error.py
    2.academic_crawler.py
    3.Html2Article.py
    4.save_to_mysql.py
    
1.handle_error.py  
操作步骤：  
A.安装依赖的库：requests#获取网页内容 pymysql#数据库操作 chardet#获取网页编码 urllib.request#打开网页  
B.连接自己的数据库：代码第14行（database函数中）conn = pymysql.connect(host='127.0.0.1', user='username', password='password', db='database_name',charset='utf8') # 连接数据库,username,password,database_name对应自己的数据库信息。  
C.运行主程序

2.academic_crawler.py  
*从数据库中获取待爬取的url的模板和规律，生成要爬取的url，获取有效详情页url并将内容存储至数据库。*  
外部库：re,urllib,pymysql,random,bs4,fnmatch  
操作步骤：  
A.安装依赖的库  
B.修改`get_enterURL_from_mysql()`中`pymysql.connect()`的参数。  
C.确认自己的save_to_mysql.py中的本机MySQL配置已修改。  
D.运行主程序  

3.Html2Article.py  
*基于统计的正文提取，设定长度阈值仅捕获有效文本进行储存。*  

4.save_to_mysql  
*将爬取数据存储至数据库*  
离线操作时请在代码头几行自行更改本机mysql配置，**更新时请不要commit此代码因本机操作带来的改变。**


### 数据库的结构设计，具体见doc


