"""
根据抖音share提取会员uid

"""
import requests
import os,re
from lxml import etree

def get_uid(url):
    res = requests.get(url).text
    html = etree.HTML(res)
    pa_url_uid = '//span[@class="focus-btn go-author"]/@data-id'
    uid=html.xpath(pa_url_uid)[0]
    print('uid为：',uid)
    return uid


if __name__ == '__main__':
    url = 'http://v.douyin.com/dBEA1k/'
    get_uid(url)