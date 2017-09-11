from bs4 import BeautifulSoup
import requests
import time
import re

headers = {
    'Cookie':'_XIGUASTATE=XIGUASTATEID=530c7b23ce004356b2a5bca8c70665aa; ASP.NET_SessionId=xgpt5tlbos2ow4u13lwwfa2p; _stopKey=124.234.159.84; _chl=key=weixinrewen&word=5b6u5L+h5YWs5LyX5Y+354iG5paH; Hm_lvt_72aa476a79cf5b994d99ee60fe6359aa=1504573627,1504677364,1504691283,1504967901; Hm_lpvt_72aa476a79cf5b994d99ee60fe6359aa=1505094071; _XIGUA=UserId=40ed819e6fe90d08&Account=07565d5e3f5bb33c&checksum=cee5f032b92f; LV2=1; SERVERID=2e7fd5d7f4caba1a3ae6a9918d4cc9a6|1505094145|1505090870',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.3368.400 QQBrowser/9.6.11860.400'
}

gzh = input('公众号ID：')

url = 'http://zs.xiguaji.com/MBiz/AsyncSearch?keyword=' + gzh + '&rnd=1'
web_data = requests.get(url, headers = headers)
soup = BeautifulSoup(web_data.text, 'lxml')

url_2 = 'http://zs.xiguaji.com' + soup.find_all('a')[0].get('href').strip('#')
data = requests.get(url_2, headers=headers)
code = BeautifulSoup(data.text, 'lxml')
a = code.select('body > div.wrapper.wrapper-no-gap.page-popular-list > div.public-details-main.public-details-padding.recentlyArticle > div.loadingMorePanel.text-center')[0]
a_a = (str(a))
id = re.findall(r'".{2,7}"', a_a)
data_id = id[0].strip('"')
data_key = id[1].strip('"')
url_3 = ['http://zs.xiguaji.com/MBiz/GetMBizHistory/' + data_key + '/' + data_id + '/{}'.format(str(i)) for i in range(1, 6)]

def get_article(url):
    final_data = requests.get(url, headers=headers)
    final_code = BeautifulSoup(final_data.text, 'lxml')

    gxsj = final_code.select('body > div.public-article-time > em:nth-of-type(1)')
    tssj = final_code.select('body > div.public-article-time > em:nth-of-type(2)')
    article = final_code.select('body > div > table > tbody > tr > td:nth-of-type(2) > div > a')
    read = final_code.select('body > div.mp-article-list > table > tbody > tr > td:nth-of-type(5)')

    global c
    global d
    c = 0
    d = 0
    for i in range(0,5):
        print('-------------------' + gxsj[i].text + '  ' + tssj[i].text + '-------------------')
        d +=int(len(article)/5)
        for j in range(c,d):
            print(article[j].text + '               ' + read[j].text)
        c +=int(len(article)/5)
    time.sleep(1)

    # for (gzhgxsj,gzhtssj) in zip(gxsj,tssj):
    #     sj = {
    #         '推文时间':'--------------' + gzhgxsj.get_text(),
    #         '更新时间': gzhtssj.get_text() + '--------------',
    #     }
    #     print(sj)
    #
    # for (gzhwz, gzhyd) in zip(article, read):
    #     wz = {
    #         '文章标题': gzhwz.get_text(),
    #         '文章阅读': gzhyd.get_text()
    #     }
    #     print(wz)

for urls in url_3:
    get_article(urls)

