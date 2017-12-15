## a-example-of-python-Crawler

### 用python写一个简单的网络爬虫 (注：本内容摘自慕课网   《Python开发简单爬虫》)

Python网络爬虫
网络爬虫又称为网页蜘蛛，网络机器人，在FOAF社区中间，经常称为网页追逐者。网络爬虫技术用来从互联网上主动获取需要的数据，是一种按照一定的规则自动地抓取万维网信息的程序或脚本。另为一些不常用的名字还有蚂蚁，自动索引，模拟程序或者蠕虫。

××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××


URL管理器
URL管理器：管理待抓取URL集合和已经抓取的URL集合，是为了防止重复抓取/防止循环抓取

需要支持：
1.添加新的URL到待爬取集合中
2.判断待添加的URL是否在容器中
3.判断是否还有待爬取的URL
4.获取待爬取的URL
5.将URL从待爬取的集合中移动到已爬取的集合

实现方式：
1.将待爬取的URL集合和已爬取的URL集合存储在内存中
  比如，如果是Python语言，可以将这两个集合存储到  set() 中，因为python的 set() 可以自动去除集合中重复的元素。
2.可以将URL存储到关系数据库中
  比如MySQL，  urls(url, is_crawled)   ,用is_crawled这个字段来标志这个URL是待爬取还是已爬取，也就是用一个表存储了待爬取和已爬取的URL。
3.可以将URL存储在缓存数据库中
  比如redis,redis本身就支持set的数据结构，可以将待爬取和已爬取的URL分别存储在set中。

对于大型企业或公司，大部分会选择redis
个人或者是小公司 可以选择存储在内存当中
如果觉得内存不够用，或者是想永久的保存数据，可以选择存储在关系数据库中


××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××

网页下载器
网页下载器是将互联网上URL对应的 网页下载到本地的工具，类似网页浏览器。

Python有哪些网页下载器？

1.urllib2--Python官方基础模块
2.requests--第三方包，比python官方基础模块更加强大


urllib2下载网页方法1：最简洁方法

```python
import urllib2

#直接请求
response = urllib2.urlopen('http://www.baidu.com')

#获取状态码，如果是200表示取得成功
print response.getcode()

#读取内容
cont = response.read()
```

urllib2下载网页方法2：添加data，http header

```python
import urllib2

#创建Request对象
request = urllib2.Request(url)

#向服务器添加数据
request.add_data('a', '1')
#添加http的header
request.add_header('User-Agent', 'Mozilla/5.0')

#发送请求获取结果
response = urllib2.urlopen(request)
```

urllibe2下载网页方法3：添加特殊情景的处理器

1.需要用户登录的网页  HTTPCookieProcessor
2.需要代理的网页  ProxyHandler
3.使用HTTP加密访问的网页  HTTPSHandler
4.url相互自动跳转的网页   HTTPRedirectHandler


HTTPCookieProcessor  ProxyHandler  HTTPSHandler HTTPRedirectHandler
        |                 |             |              |
        |                 |             |              |
                  opener = urllib2.build_opener(handler)
                                  |
                                  |
                     urllib2.install_opener(opener)
                                  |
                                  |
                         urllib2.urlopen(url)
                       urllib2.urlopen(request)

```python
import urllib2,cookielib

#创建cookie容器
cj = cookielib.CookieJar()

#创建一个opener
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

#给urllib2安装opener
urllib2.install_opener(opener)

#使用带有cookie的urllib2访问页面
response = urllib2.urlopen("http://www.baidu.com/")
```
============================================================

```python
import urllib2
import cookielib
url = "http://www.baidu.com"

print '1'
response1 = urllib2.urlopen(url)
print response1.getcode()
print len(response1.read())

print '2'
request = urllib2.Request(url)
request.add_header("user-agent", "Mozilla/5.0")
response2 = urllib2.urlopen(request)
print response2.getcode()
print len(response2.read())

print '3'
cj = cookielib.CookieJar()  #注意，要引入cookielib的包
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)
response3 = urllib2.urlopen(url)
print response3.getcode()
print cj
print response3.read()
```

×××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××

网页解析器
网页解析器是从网页中提取有价值数据的工具，提取出我们想要的数据以及新的待爬取的URL
python有哪几种网页解析器？
1.正则表达式  直观，但是如果提取的网页内容复杂的话，非常麻烦。
2.python自带的html.parser模块来解析网页
3.第三方插件Beautiful Soup
4.第三方插件lxml解析html网页或者是xml网页

网页解析器-Beautiful Soup语法
Html网页下载完毕——>创建BeautifulSoup对象，同时字符串会被自动记加载成DOM树——>根据DOM树，搜索节点find_all/find——>访问节点的名称，属性，文字（find_all方法会搜索所有满足要求的节点，find方法只会搜索出第一个满足要求的节点）
在搜索节点的时候我们也可以按照节点的名称进行搜索，或者按照节点的属性值进行搜索，或者按照节点文字进行搜索
```html
<a href = '123.html' class = 'article_link'>Python</a>
```
节点名称：a
节点属性：href = '123.html'   class = 'article_link'
节点内容：Python

创建BeautifulSoup对象

```python
from bs4 import BeautifulSoup
#根据HTML网页字符串创建BeautifulSoup对象
soup = BeautifulSoup(
    html_doc,                 #HTML文档字符串
    'html.parser',            #HTML解析器
    from_encoding = 'utf8'    #HTML文档的编码
)

搜索节点（find_all,find）
#方法:find_all(name, attrs, string)
#查找所有标签为a的节点

soup.find_all('a')

#查找所有标签为a，链接符合/view/123.html形式的节点

soup.find_all('a', href = '/view/123.html')
soup.find_all('a', href = re.compile(r'/view/\d+\.html))

#查找所有标签为div，class为abc，文字为Python的节点
soup.find_all('div', class_ = 'abc', string = 'Python')
注：class后面有个_是因为python存在名字为class的关键字，为了避免冲突，所以书写为 class_

访问节点信息
#得到节点：<a href = '1.html'>Python</a>

#获取查找到的节点的标签名称
node.name

#获取查找到的a节点的href属性
node['href']

#获取查找到的a节点的链接文字
node.get_text()
```

×××××××××××××××××××××××××××××××××××××××××××××××××
BeautifulSoup实例测试
×××××××××××××××××××××××××××××××××××××××××××××××××

```python
from bs4 import BeautifulSoup
import re

html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""

soup = BeautifulSoup(html_doc, 'html.parser', from_encoding='utf8')

#获取所有的链接
print '1'
links = soup.find_all('a')
for link in links:
    print link.name, link['href'], link.get_text()

#获取lacie的链接
print '2'
link_node = soup.find('a', href='http://example.com/lacie')
print link_node.name, link_node['href'], link_node.get_text()

#正则表达式获取
link_node = soup.find('a', href=re.compile(r"ill"))
print link_node.name, link_node['href'], link_node.get_text()

#获取p段落文字
p_node = soup.find('p', class_ = "title")
print p_node.name, p_node.get_text()
```

***************************************************************************
接下来我们来进行实战演练--爬取百度百科1000个页面数据

开发一个爬虫的步骤
1.确定抓取的目标
2.分析目标--  分析抓取目标页面的URL格式，抓取的数据格式，分析页面的编码
3.编写代码
4.执行爬虫

慕课网上《Python网络爬虫》这节课上，老师以百度百科上Python词条的相关网页作为例子为大家讲解，大家可以去搜索这节课，看看具体 
的讲解，这里就简单的总结分析一下我们接下来要爬去的目标

入口页：http://baike.baidu.com/view/21087.html
URL格式：词条页面URL:/view/125370.htm
数据格式：
    标题：
    ```python
    <dd class="lemmaWgt-lemmaTitle-title"><h1>****</h1></dd>
    ```
    简介：
    ```python
    <div class="lemma-summary">****</div>
    ```
页面编码：UTF-8
