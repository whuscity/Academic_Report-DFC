# from selenium import webdriver
#
#
# driver = webdriver.Chrome()
# driver.get('http://sw.scu.edu.cn/info/1046/5758.htm')
# # cookie = driver.get_cookies()
# # for i in cookie:
# #     print(i)
# print(driver.find_element_by_tag_name('h1').text)  # sb_form_q before refresh
#
# driver.close()
import re
a = 'http://www.seiee.sjtu.edu.cn/seiee/list/683-2-20.htm'
r = re.findall('[0-9]+', a)
print(r)
new_url = a.replace(r[-2],'1', 1)
print(new_url)