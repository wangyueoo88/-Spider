import requests
import traceback
import os
from hashlib import md5
import multiprocessing



#分析获取今日头条街拍的AJAX上传内容
def get_response(offset,text):
    #获取对应请求得到的页面
    url='https://www.toutiao.com/search_content/?'
    param = {
        'offset': offset*20,
        'format': 'json',
        'keyword': text,
        'autoload': 'true',
        'count': '20',
        'cur_tab': '3',
        'from':'gallery'
    }
    header={'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
            'x - requested -with': 'XMLHttpRequest',
            'cookie': 'uuid = "w:2125577692434a5c8aee7dbd817d68ad";_ga = GA1.2.1624702816.1516541347;sid_guard = 240d6c281da532ab53219f3b2001d668 % 7C1516541474 % 7C15552000 % 7CFri % 2C % 2020 - Jul - 2018 % 2013 % 3A31 % 3A14 % 20GMT;__tea_sdk__web_id = 2582676043;__tea_sdk__user_unique_id = 2582676043;__tea_sdk__ssid = 0;tt_webid = 6581416211295274504;WEATHER_CITY = % E5 % 8C % 97 % E4 % BA % AC;UM_distinctid = 164c77f6b8c329 - 04d3cccc905ee6 - 444a022e - 2a3000 - 164c77f6b8d177;tt_webid = 6581416211295274504;csrftoken = f2acdc9217820ac726c476a5e12f17f3;CNZZDATA1259612802 = 1403039684 - 1516541042 - https % 253A % 252F % 252Fwww.baidu.com % 252F % 7C1534339112;__tasessionId = e1emnz8jp1534343792360'
            }
    url_a=requests.get(url,params=param,headers=header).json()
    return url_a
def ananysis_json(json):
    # 解析传入的JSON
    if json:
        try:
            data=json.get('data')
            for dic in data:
                title_a=dic.get('title')
                url_list=dic.get('image_list')
                if title_a==None or url_list==None:
                    continue
                for i in url_list:
                    pic=i['url']
                    yield {'title':title_a   ,
                    'pic':pic
                            }
        except Exception as ee:
            print('error',ee)
            traceback.print_exc()
    else:
        print('传入的数据为空')
def save_data(data,text):
    if not os.path.exists(r'D:\今日头条图片%s的爬取' %text):
        os.mkdir(r'D:\今日头条%s的爬取' %text)
    try:
        if not os.path.exists(r'D:\今日头条图片%s的爬取\%s' % (text,data['title'])):
            os.mkdir(r'D:\今日头条%s的爬取\%s' % (text,data['title']))
        pic_data=requests.get(r'https:{}'.format(data['pic'])).content
        with open('D:\今日头条%s的爬取\%s\%s.png'%(text,data['title'],md5(pic_data).hexdigest()),'wb') as ziyuan:
            ziyuan.write(pic_data)
        print('---------------储存进行中----------------')
    except Exception as rr:
        print('err',rr)
        traceback.print_exc()
def  run_page(offset,text):
    #offst为爬取的更新页数
    for i in ananysis_json(get_response(offset,text)):
        save_data(i,text)
def run(text):
    #此方法默认爬取八次
    for kk in range(8):
        run_page(kk,text)

    print('爬取任务%s完成'%text)
    print('爬取完成')
def main():
    pool=multiprocessing.Pool(8)
    list_task=['街拍','随拍','美女','帅哥']
    for i in list_task:
        pool.apply_async(func=run,args=(i,))
    pool.close()
    pool.join()
    print('整个运行完成')

if __name__ == '__main__':
    main()
