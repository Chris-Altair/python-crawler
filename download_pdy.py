import os
import logging
import time
import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.DEBUG)


def timer(func):
    def wrapper(*args, **kw):
        start = time.time()
        f = func(*args, **kw)
        end = time.time()
        print('程序运行时间：%ss' % (end - start))
        return f

    return wrapper


class DownLoader(object):
    def __init__(self):
        self._url_head = 'https://m.hjgze.com'
        self._start_url = 'https://m.hjgze.com/hjgz/29/29848/2678861.html'
        self._end_url = 'https://m.hjgze.com/book/29848.shtml'
        self._filepath = '/home/amadeus/文档/小说/novel.txt'

    @timer
    def download_chapters(self):
        index = 0
        rsp = requests.get(self._start_url)
        html = rsp.content.decode('gbk', 'ignore')
        soup = BeautifulSoup(html, 'html5lib')
        dirname, filename = os.path.split(self._filepath)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        while True:
            index += 1
            next_chapter_url = self._url_head + soup.find('div', class_='chaper_na5').a['href']  # 获取下一页的url
            logging.debug('next_chapter_url:%s' % next_chapter_url)
            chapter_text = soup.find('div', class_='chapter_co').get_text('\n', '<br/>')  # 爬取的文本要用get_text不要用.string
            self.write_file(chapter_text)
            # logging.debug(chapter_text)
            if next_chapter_url == self._end_url:
                self.write_file(chapter_text)
                print('总计爬取%s个页面，共%sKB' % (index, os.path.getsize(self._filepath) / 1024))
                return
            catch_html = requests.get(next_chapter_url).content.decode('gbk', 'ignore')
            soup = BeautifulSoup(catch_html, 'html5lib')

    def write_file(self, chapter_text):
        with open(self._filepath, 'a', encoding='utf-8') as writer:
            writer.write(chapter_text)

    @timer
    def test(self):
        time.sleep(3)


if __name__ == '__main__':
    d = DownLoader()
    print('开始抓取数据')
    d.download_chapters()
    print('抓取数据完成')
