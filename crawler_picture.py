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
        print('times = %ss\n' % (end - start))
        return f

    return wrapper


class Crawler(object):
    def __init__(self):
        self._host = 'https://bbs.yamibo.com/'
        self._url = 'https://bbs.yamibo.com/forum.php?mod=viewthread&tid=188674&page=1&authorid=98260'
        self._headers = {
            'User-Agent':'ozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'Cookie':'Your Cookie'
        }
        self._session = requests.Session()
        self._filepath = '/home/XXX/picture/lily'

    @timer
    def crawler_url(self):
        req = self._session.get(self._url,headers=self._headers)
        if req.status_code == 200:
            logging.info("access success!")
            logging.info('url encoding:%s'%req.encoding)
            logging.info('begin crawler url:%s\n'%self._url)
            #logging.info(req.text)
            html = req.content.decode(req.encoding, 'ignore')
            soup = BeautifulSoup(html, 'html5lib')
            title = soup.title.string.split('-')[0].strip()  # str按-分割并去除前后空格
            print("title=>%s"%title)
            self._filepath = os.path.join(self._filepath,title)
            if not os.path.exists(self._filepath):
                os.makedirs(self._filepath)
            print("filepath=>%s\n"%self._filepath)
            for index,img in enumerate(soup.find_all("img", attrs={"zoomfile": True})):
                img_url = self._host+img['zoomfile']
                print("img_%s=>%s"%(index,img_url))
                self.download(index,img_url)
                break
            print('total')
        else:
            logging.debug("Access failed!")

    @timer
    def download(self,index,img_url):
        r = self._session.get(img_url,stream=True)  # 实现进度条需要(因为文件小不需要)
        img_name = str(index)+'.'+img_url.split('.')[-1]
        img_path = os.path.join(self._filepath,img_name)
        content_size = int(r.headers['content-length'])  # 通过response的headers中获取文件大小信息
        print("img size："+str(round(float(content_size/1024),4))+"[KB]")
        print('img_path=>%s'%img_path)
        with open(img_path,'wb') as f:
            f.write(r.content)


if __name__=="__main__":
    Crawler().crawler_url()

