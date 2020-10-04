# -*- coding: utf-8 -*-
# author:Gary
# 参考博客：https://blog.csdn.net/weixin_43046974/article/details/106145524
import glob
import os
import time

import numpy
from PIL import Image
from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
# options.add_experimental_option('excludeSwitches', ['enable-automation'])#提示浏览器不是selenium,但是好像没效果
chrome_options.add_argument('--headless')  # 无头
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')  # 这个配置很重要


class ScreenLongShot(object):

    # 需要传入的参数为爬取的链接，以及对应的文件名
    def __init__(self, url, filename):
        self.get_img = "./img/{}.png".format(filename)
        # self.driver=webdriver.Chrome(options=chrome_options)  #  初始化浏览器，服务器上跑用这个
        self.driver = webdriver.Chrome()  # 本地测试用这个
        self.driver.maximize_window()
        self.page = url

    def get_height(self):
        # 获取谷歌浏览器的高度以及网页的高度
        chrome_height = self.driver.get_window_size()["height"]
        page_height = self.driver.execute_script('return document.documentElement.scrollHeight')
        return chrome_height, page_height

    def scree_shot(self):
        try:
            self.driver.get(self.page)
            # 隐式等待，效果不佳
            self.driver.implicitly_wait(10)
            time.sleep(5)  # 睡眠5s，等待一些异步加载操作完成
            chrome_height, page_height = self.get_height()
            temp_img = "tmp.png"
            self.driver.save_screenshot(temp_img)
            """取余网页高度和谷歌浏览器高度的余数来判断滚动几次鼠标"""
            if page_height > chrome_height:
                n = page_height // chrome_height
                base_mat = numpy.atleast_2d(Image.open(temp_img))
                for i in range(n):
                    """每滚动一次鼠标就截图一次"""
                    self.driver.execute_script(f'document.documentElement.scrollTop={chrome_height * (i + 1)};')
                    time.sleep(.5)
                    self.driver.save_screenshot(f'tmp_{i}.png')
                    mat = numpy.atleast_2d(Image.open(f'tmp_{i}.png'))
                    base_mat = numpy.append(base_mat, mat, axis=0)
                Image.fromarray(base_mat).save(self.get_img)
        except Exception as e:
            print(e)
        finally:
            """删除执行中间的缓存图片"""
            for i in glob.glob(os.path.join(os.getcwd(), 'tmp*.png')):
                os.remove(i)

    def close_chrome(self):
        self.driver.quit()


def main():
    url = "https://www.aliyun.com/"

    s = ScreenLongShot(url=url, filename='test')
    try:
        s.scree_shot()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
