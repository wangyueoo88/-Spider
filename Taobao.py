from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import traceback
import time
from lxml import etree
from multiprocessing import Queue
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver import ActionChains
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

browser = webdriver.Chrome(chrome_options=chrome_options)
#使用无头浏览器爬取
# 梳理一下流程
# 1.进去淘宝，输入关键词，点击搜索
# 2.提取总计页数
# 3.提取elements
# 4.切换页面
def taobao(text,page):
    try:
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        browser = webdriver.Chrome(chrome_options=chrome_options)
        wait = WebDriverWait(browser, 10)
        browser.get('https://www.taobao.com/')
        input=browser.find_element_by_id('q')
        input.send_keys(text)
        sousuo=browser.find_element_by_xpath('//*[@id="J_TSearchForm"]/div[1]/button')
        sousuo.click()
        if page>1:
            input_page=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > div.form > input')))
            input_submit = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit')))
            input_page.clear()
            input_page.send_keys(page)
            input_submit.click()
            time.sleep(2)
            page_index=wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="mainsrp-pager"]/div/div/div/ul/li[@class="item active"]/span')))
            if int(page_index.text)==page:
                #如果找到了这个元素说明成功跳转到了
                return browser.page_source
                #判定网页元素是否成功跳转
            else:
                taobao(text,page)
        else:
            return  browser.page_source
    except Exception as error:
        #出错了会报错
        print('error',error)
        traceback.print_exc()
    except TimeoutException:
        print('--------超时  两秒后尝试重连---------')
        time.sleep(2)
        taobao(text,page)

def parase_html_1(html):
    #解析淘宝的内容
    if html:
        selector=etree.HTML(html)
        nodes=selector.xpath('//*[@id="mainsrp-itemlist"]/div/div/div[1]/div')
        nodesl = selector.xpath('//*[@id="J_itemlistPersonality"]/div/div')
        nodes_all=nodes+nodesl
        for node in nodes_all:
            pic_url=node.xpath('./div[1]/div[1]/div[1]/a/img/@src')
            title_name=node.xpath('./div[2]/div[2]/a/text()')
            purchase_num=node.xpath('./div[2]/div[1]/div[2]/text()')
            price=node.xpath('./div[2]/div[1]/div[1]/strong/text()')
            yield {'pic_url':'https'+pic_url[0],
                   'title_name':title_name,
                   'purchase_num':purchase_num[0],
                   'price':price[0]
            }
    else:
        print('html没有')
def main():
    n=1
    while n<20:
        for i in parase_html_1(taobao('美食',n)):
            print(i)
        n+=1

if __name__ == '__main__':
    main()
