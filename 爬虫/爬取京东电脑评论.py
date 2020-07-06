import csv
import time
import random
import json
import requests
from bs4 import BeautifulSoup
from lxml import etree


def write_into_csv(path,items,attrs):
    with open(path,'w',encoding="utf-8",newline="")as fp:
        writer = csv.writer(fp)
        writer.writerow(attrs)  # 属性列名
        writer.writerows(items)


def read_from_csv(path):
    items=[]
    with open(path,'r',encoding="utf-8",newline="")as csvfile:
        reader=csv.reader(csvfile)
        for line in reader:
            items.append(line)
    return items


headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'}

if __name__=="__main__":
    url="https://search.jd.com/Search?"
    params={'keyword':'笔记本电脑',
            'enc':'utf-8',
            'wq':'笔记本电脑',
            'pvid':'4d77fd638d44494d8476bf000ae3a4c7'}
    res=requests.get(url,headers=headers,params=params)
    selector=etree.HTML(res.text)
    good_list=selector.xpath('//*[@id="J_goodsList"]/ul/li')
    items=[]
    cnt=0
    for good in good_list:
        cnt+=1
        if cnt==10:
            break
        good_id=good.xpath('@data-sku')[0]
        good_url='https://item.jd.com/{}.html'.format(good_id)
        res=requests.get(good_url,headers=headers)
        selector=etree.HTML(res.text)
        good_brand=selector.xpath('//*[@id="parameter-brand"]/li/a/text()')[0]
        good_name=selector.xpath('//*[@id="detail"]/div[2]/div[1]/div[1]/ul[2]/li[1]/text()')[0]

        for i in range(1): # 页数，每页9条评论
            comment_url='https://club.jd.com/comment/productPageComments.action?'\
            'callback=fetchJSON_comment98&productId='+str(good_id)+'&score=0&sortType=5&' \
            'page='+str(i)+'&pageSize=10&isShadowSku=0&fold=1' # network->search:comment
        res_comment=requests.get(comment_url,headers=headers)
        res_comment_text=res_comment.text.replace('fetchJSON_comment98(','').replace(');','')
        comments=json.loads(res_comment_text)['comments']
        for comment in comments:
            good_comment=comment['content']
            item=[good_brand,good_name,good_comment]
            items.append(item)
        print("商品{}信息已收集...".format(cnt))
        time.sleep(random.randint(1,5))
    path=r"C:\Users\Zhaowei\Desktop\暑假实训\comment.csv"
    write_into_csv(path,items,['品牌','商品名称','评论内容'])
