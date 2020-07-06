import json
import requests
import re
import urllib.request
import time
import random
result_path=r"C:\Users\Zhaowei\Desktop\暑假实训\702\result_jingdong.txt"
comment_path=r"C:\Users\Zhaowei\Desktop\暑假实训\702\result_jingdong_comment"

def write_Product_to_file(content):  # 商品名+URL写文件
    with open(result_path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')

# 写入第k个商品的评论至txt
def write_Comments_to_file(content, k):
    with open(comment_path+str(k)+'.txt', 'a', encoding='utf-8') as f:  # 注意这里要用'a'
        f.write(json.dumps(content, ensure_ascii=False) + '\n')

# 获取第k个商品的评论
def GetComment(url, k):
    html = urllib.request.urlopen(url).read().decode('gbk', 'ignore')
    jsondata = html
    data = json.loads(jsondata)
    for i in data['comments']:
        content = i['content']
        write_Comments_to_file(content, k)  # 写入第k个商品的评论至txt


# 获取商品名和评论URL
def GetProductUrl(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
    }  # 必须加请求头，否则禁止访问
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'  # 编码问题！！注意！！
    # requests根据内容自动编码，会导致一些意想不到的问题，记得用encoding自定义所需编码
    html = response.text
    results = re.findall(u'.*?class\=\"p\-name.*?\<em\>(.*?)\<\/em\>', html, re.S)  # 找所有class=p-name标签的text部分
    i = 0
    for result in results:
        result = re.sub('<font.*?>|</font>|<span.*?>|</span>|<img.*?>|&hellip;|\n', '',result)
        results[i] = result
        i = i + 1
    results2 = re.findall('.*?class\=\"p\-commit.*?href\=\"(.*?)\"\sonclick', html, re.S)  # 获取评价的url

    dictionary = dict(zip(results, results2))  # 建立字典，表示商品名和评论URL的关系，为之后排序做准备
    print(dictionary)
    write_Product_to_file(dictionary)  # 将字典写入文件


# 获取该商品的评论数，默认评论数
def GetProduct_Comments_Number(result_ProID):
    url = 'http://club.jd.com/comment/productCommentSummaries.action?referenceIds=' + result_ProID
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
    }  # 必须加请求头，否则禁止访问
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'  # 编码问题！！注意！！
    # requests根据内容自动编码，会导致一些意想不到的问题，记得用encoding自定义所需编码
    html = response.text
    comments_count = re.findall('\"CommentCount\"\:(.*?)\,.*?\"DefaultGoodCount\"\:(.*?)\,', html, re.S) # 评论数，默认评论数
    print(comments_count)
    return comments_count


if __name__=="__main__":
    url = 'https://search.jd.com/Search?keyword=%E5%B8%BD%E5%AD%90&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E5%B8%BD%E5%AD%90&psort=3&click=0'  # 根据销量排序
    print("开始获取商品信息：")
    GetProductUrl(url)  # 获取商品名和评论URL

    f = open(result_path, 'r', encoding='utf-8')
    txt = f.read()
    result_ProIDs = re.findall('com\/(.*?)\.html', txt, re.S)  # 通过url获取商品id
    result_ProIDs = list(result_ProIDs)
    print(result_ProIDs) #30个商品

    cnt = 1
    for result_ProID in result_ProIDs:
        print("正在获取第{}个商品的评论数据".format(cnt))
        comments_count = GetProduct_Comments_Number(result_ProID)  # 获取该商品的评论数，默认评论数
        num = int(comments_count[0][0]) - int(comments_count[0][1])  # 删除默认评论
        print(num) #

        for i in range(0, int(num / 10)):
            print("正在获取第{}页评论数据".format(i + 1))
            url = 'http://club.jd.com/comment/productPageComments.action?' + '&productId=' + result_ProID + '&score=0&sortType=5&page=' + str(
                i) + '&pageSize=10&isShadowSku=0&fold=1'
            try:
                GetComment(url, cnt)
            except:
                print("第{}页获取失败".format(i + 1))
            time.sleep(random.randint(1, 3))
        cnt+=1

