# -*- coding: utf-8 -*-
"""
Created on Tue May 22 13:31:18 2018

@author: Administrator
"""

import requests
from bs4 import BeautifulSoup
import json
def getNewsDetail(newsurl):
    result = {}
    res = requests.get(newsurl)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text,'lxml')
    result['title'] = soup.select('.main-title')[0].text
    result['article'] = '\n'.join([p.text.strip() for p in soup.select('#article p')[:-1]])
    result['editor'] = soup.select('.show_author')[0].text
    result['time'] = soup.select('.date-source')[0].contents[1].text
    return result
def ParseListLinks(url):
    newsdetail = []
    res = requests.get(url)
    jd = json.loads(res.text.lstrip('  newsloadercallback(').rstrip(');'))
    for ent in jd['result']['data']:
        newsdetail.append(getNewsDetail(ent['url']))
    return newsdetail
url = 'http://api.roll.news.sina.com.cn/zt_list?channel=news&cat_1=gjxw&level==1||=2&show_ext=1&show_all=1&show_num=22&tag=1&format=json&page=2&callback=newsloadercallback&_=1526969960281'
ParseListLinks(url)


#批量抓取新闻内文数量

url = 'http://api.roll.news.sina.com.cn/zt_list?channel=news&cat_1=gjxw&level==1||=2&show_ext=1&show_all=1&show_num=22&tag=1&format=json&page=2&callback=newsloadercallback&_=1526969960281'
news_total = []
for i in range(1,3):
    newsurl = url.format(i)
    newsary = ParseListLinks(newsurl)
    news_total.extend(newsary)
len(news_total)


#使用pandas整理数据

import pandas
df = pandas.DataFrame(news_total)
df


#将数据保存到Excel中

df.to_excel('news.xlsx')