# python-crawler

主要使用requests和BeautifulSoup两个库
requests用来请求
BeautifulSoup用来解析html

静态网站的爬虫直接使用requests.get(url)就可
动态网站可以分析具体网站的login方式使用post，这里是通过先在具体登录页面登录后通过开发者工具获取cookie信息，
创建session对象，将cookie信息塞到http的request headers中，再通过get方式请求url，之后就跟静态网站的请求方式相同了