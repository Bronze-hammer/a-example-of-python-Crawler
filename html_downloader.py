
import urllib2

class HtmlDownloader(object):


    def download(self, url):
        if url is None:
            return None
        
        #直接请求
        response = urllib2.urlopen(url)

        #获取状态吗，如果是200则表示获取成功
        if response.getcode() != 200:
            return None

        #读取内容
        return response.read()
