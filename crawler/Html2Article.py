# -*- coding: UTF-8 -*-
#Html2Article.py:基于统计的正文提取
import re
import urllib.request
import time
from bs4 import BeautifulSoup
import chardet#获取网页编码


threshold_of_article = 5  #设置的正文长度阈值

def get_html(url):
    try:
        header = {"User-Agent": "Mozilla5.0 (Windows NT 6.1; WOW64; rv:59.0) Gecko/20100101 Firefox/59.0"}
        request = urllib.request.Request(url, headers=header)
        response = urllib.request.urlopen(request, timeout=10)
        html = response.read()
        encode = chardet.detect(html)['encoding']#获取网页编码
        # response = requests.get(url,headers=header)
        # html = response.text
        # return html
        html_file = html.decode(encode)
        return html_file


    except Exception as e:  # 抛出超时异常
        print('\r详情页错误:', str(e),end="")
        time.sleep(3)
        return None

def html2Article(html_file):

    #首先去除可能导致误差的script和css，之后再去标签
    tempResult = re.sub('<script([\s\S]*?)</script>','',html_file)
    tempResult = re.sub('<SCRIPT([\s\S]*?)</SCRIPT>', '', tempResult)
    tempResult = re.sub('<style([\s\S]*?)</style>','',tempResult)

    #去除所有的超链接及链接内容
    # tempResult = re.sub('<[Aa].+?</[Aa]>','',tempResult)
    #可跨行匹配<a></a>
    r=re.compile('<[Aa].+?</[Aa]>',re.S | re.M)
    tempResult = r.sub('',tempResult)
    #去除选择框的链接
    r = re.compile('<select.+?</select>', re.S | re.M)
    tempResult = r.sub('', tempResult)
    #去除所有的HTML标签
    tempResult = re.sub('(?is)<.*?>','',tempResult)

    #去除页脚标记
    tempResult = re.sub('.*版权所有.*', '', tempResult)
    tempResult = re.sub('.*[Cc]opy[Rr]ight.*', '', tempResult)

    # 去除强制空格及2个以上的空格（大于等于2是因为考虑到英文文本的自然空格）
    tempResult = tempResult.replace('&nbsp;', '')
    tempResult = tempResult.replace('&nbsp', '')
    tempResult = tempResult.replace('&raquo;', '')
    tempResult = tempResult.replace('  ', '')

    #去除空行
    r = re.compile(r'''^\s+$''', re.M | re.S)
    tempResult = r.sub('', tempResult)
    r = re.compile(r'''\n+''', re.M | re.S)
    tempResult = r.sub('\n', tempResult)

    #以\n为分隔符对字符串进行切片，返回列表
    tempResultArray = tempResult.split('\n')
    #print(tempResult)

    result_data = []

    #依据每行的长度判断是否为正文
    for oneLine in tempResultArray:
        if len(oneLine) > threshold_of_article:
            #print(oneLine)
            result_data.append(oneLine.strip())
    # print(result_data)
    return result_data

def get_article(academic_url):
    result_data=html2Article(get_html(academic_url))
    #将列表转为字符串
    return '\n'.join(result_data)

if __name__ == "__main__":
    # a = get_article('http://cab.cau.edu.cn/art/2019/2/1/art_24507_605787.html')
    a = get_html('http://cab.cau.edu.cn/col/col24507/index.html?uid=40369&pageNum=3')
    print(a)

    # with open('test.html', encoding='utf-8') as file:
    #     # start = time.time()
    #     a=html2Article(file.read())
    #     # print(time.time() - start)
    #     print('\n'.join(a))

