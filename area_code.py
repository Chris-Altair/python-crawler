import os
import logging
import time
import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.DEBUG)


class Association(object):
    id = 1  # 静态变量

    def __init__(self, parent_id, name, code):
        Association.id += 1
        self._id = Association.id
        self._parent_id = parent_id
        self._name = name
        self._code = code

    def to_sql(self):
        sql_str = 'insert into ASSOCIATION (ID, PARENT_ID, NAME, CODE, PX)values(%s,%s,\'%s\',\'%s\',\'%s\');' % (
            self._id, self._parent_id, self._name, self._code, 1)
        logging.debug(sql_str)
        return sql_str

    def print(self):
        print('id = %s' % self._id)
        print('parent_id = %s' % self._parent_id)
        print('name = %s' % self._name)
        print('code = %s\n' % self._code)


class Crawler(object):
    def __init__(self):
        self._url = 'http://www.ip33.com/area_code.html'
        self._file_path = 'C:\\Users\\Amadeus\\Desktop\\association.sql'

    def crawler(self):
        rsp = requests.get(self._url)
        html = rsp.content.decode('utf8', 'ignore')
        soup = BeautifulSoup(html, 'html5lib')
        # logging.debug(html)
        for province in soup.find_all('div', 'ip'):
            province_name, province_code = province.h4.string.split(' ', 1)  # 按空格分割成两个str
            province_code = province_code.ljust(6, '0')  # 6位长度，不全补0
            print('开始爬取省份信息(%s,%s)'%(province_name, province_code))
            province_association = Association(0, province_name, province_code)
            # province_association.to_sql()
            self.write_file(province_association.to_sql())  # 写入省份
            parent_id = province_association._id  # 省份的id
            print('#'*4+'开始爬取市级信息'+'#'*4)
            for city in province.ul.children:
                if city.find('h5') != -1:  # 过滤空元素
                    city_h5_str = city.find('h5').string
                    if '市' in city_h5_str and '区' not in city_h5_str:
                        city_name, city_code = city_h5_str.split(' ', 1)
                        city_code = city_code.ljust(6, '0')
                        city_association = Association(parent_id, city_name, city_code)
                        # city_association.to_sql()
                        self.write_file(city_association.to_sql())  # 写入市
            print('#'*4+'市级信息爬取完成'+'#'*4)
            print('省份信息(%s,%s)爬取完成!\n'%(province_name, province_code))

    def write_file(self, sql):
        with open(self._file_path, 'a', encoding='utf-8') as writer:
            writer.write(sql + '\n')


if __name__ == '__main__':
    Crawler().crawler()
