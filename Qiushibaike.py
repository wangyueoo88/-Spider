import requests
import re
import traceback
#本次爬取可用时间为2018.8.14
class Qiushi:
    def __init__(self,page=1):
        self.page=page
        self.url='https://www.qiushibaike.com/text/page/{}/'
        self.header={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'}
    def get_url(self,page):
        url=self.url.format(page)
        return url
    def get_html(self,url):
        try:
            response=requests.get(url,headers=self.header).text
            return  response
        except Exception as error:
            print('error:',error)
            traceback.print_exc()
    def parase_html(self,html):
        if html:
            try:
                find_content=re.compile('<h2>(.*?)</h2>.*?<div class="content">.*?<span>(.*?)</span>.*?<span class="cmt-name">(.*?)</span>.*?<div class="main-text">(.*?)<div class="likenum">',re.S)
                result_content=re.findall(find_content,html)
                for i in result_content:
                    author_name=i[0].replace(r'\n','').replace(r'<br/>','')
                    author_content=i[1].replace(r'\n','').replace(r'<br/>','')
                    comment_author=i[2].replace(r'\n','').replace(r'<br/>','')
                    comment=i[3].replace(r'\n','').replace(r'<br/>','')
                    dictl={'author_name':author_name,
                           'author_content':author_content,
                           'comment_author':comment_author,
                           'comment':comment
                            }
                    print(dictl)
            except Exception as error:
                print('error:', error)
                traceback.print_exc()
        else:
            print('没有传入html')
    def run(self):
        for i in range(self.page):
            self.parase_html(self.get_html(self.get_url(i+1)))


def main():
    aa=Qiushi(13)
    aa.run()




if __name__ == '__main__':
    main()
