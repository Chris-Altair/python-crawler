# -*- coding: utf-8 -*-

import logging
import os
import time
import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)


def timer(func):
    def wrapper(*args, **kw):
        start = time.time()
        f = func(*args, **kw)
        end = time.time()
        print('程序运行时间：%ss' % (end - start))
        return f

    return wrapper


class Crawler(object):
    def __init__(self):
        self._dir_url = 'https://www.yamibo.com/novel/125558'
        self._headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.36',
            'Cookie': 'your cookie info'
        }
        self._session = requests.Session()
        self._params = {}  # 这里没用到
        self._chapter_urls = []  # 这里没用到
        self._novel_name = ''
        self._filepath = '/home/amadeus/文档/小说'

    def write_chapter(self, text):
        dirname, filename = os.path.split(self._filepath)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        with open(self._filepath, 'a', encoding='utf8') as writer:
            writer.write(text)

    def crawl_chapter(self, chapter_name, url):
        resp = self._session.get(url, headers=self._headers)
        logging.debug(resp.encoding)
        html = resp.content.decode(resp.encoding, 'ignore')
        soup = BeautifulSoup(html, 'html5lib')
        chapter_name = soup.h3.string
        if chapter_name[3] == ' ':
            chapter_name = chapter_name[4:]
        elif chapter_name[4] == ' ':
            chapter_name = chapter_name[5:]
        p_list = soup.find('div', id='txt').find('div', id='w0-collapse1').div.find_all('p')
        chapter_text = '   ' + chapter_name + '\n'*3
        for p in p_list:
            chapter_text += '   ' + p.get_text('\n', '<br/>') + '\n'
        chapter_text += '\n'
        self.write_chapter(chapter_text)

    @timer
    def crawl_novel(self):
        print('爬虫开始')
        response = self._session.get(self._dir_url, headers=self._headers)
        logging.debug(response.encoding)
        # logging.debug(response.text)
        html = response.content.decode(response.encoding, 'ignore')
        soup = BeautifulSoup(html, 'html5lib')
        self._novel_name = soup.title.string[0:7].replace(' ', '')  # 小说名
        self._filepath = os.path.join(self._filepath, self._novel_name + '.txt')
        print('小说保存路径%s' % self._filepath)
        logging.info(self._novel_name)
        for chapter_info in soup.find_all("div", attrs={"data-key": True}):  # 筛选含有data-key属性的div
            chapter_name = chapter_info.a.string
            if chapter_name.endswith('无标题'):
                continue
            chapter_url = 'https://www.yamibo.com' + chapter_info.a['href']
            print('name:%s, url:%s' % (chapter_name, chapter_url))
            print('开始爬取%s' % chapter_name)
            self.crawl_chapter(chapter_name, chapter_url)
            print('爬取%s完成！' % chapter_name)
        print('爬虫结束！')


if __name__ == '__main__':
    c = Crawler()
    c.crawl_novel()
