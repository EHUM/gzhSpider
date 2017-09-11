from bs4 import BeautifulSoup
import requests
import xlrd
import time

headers = {
    'Cookie':'_XIGUASTATE=XIGUASTATEID=530c7b23ce004356b2a5bca8c70665aa; ASP.NET_SessionId=xgpt5tlbos2ow4u13lwwfa2p; _stopKey=124.234.159.84; _chl=key=weixinrewen&word=5b6u5L+h5YWs5LyX5Y+354iG5paH; Hm_lvt_72aa476a79cf5b994d99ee60fe6359aa=1504573627,1504677364,1504691283,1504967901; Hm_lpvt_72aa476a79cf5b994d99ee60fe6359aa=1505094071; _XIGUA=UserId=40ed819e6fe90d08&Account=07565d5e3f5bb33c&checksum=cee5f032b92f; LV2=1; SERVERID=2e7fd5d7f4caba1a3ae6a9918d4cc9a6|1505094145|1505090870',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.3368.400 QQBrowser/9.6.11860.400'
}

data = xlrd.open_workbook(r'C:\Users\eeehu\Documents\Tencent Files\3416500170\FileRecv\总资源表.xls')
sheet = data.sheet_by_index(0)

sheetRows = int(input('开始行：')) - 1
sheetRowe = int(input('结束行：'))
sheetCol = input('ID列：')
fenSi = input('价格列：')

colDec = {'A': 0, 'B': 1, 'C': 2, 'D': 3,'E': 4,'F': 5,'G': 6,'H': 7,'I': 8,'J': 9,'K': 10,'L': 11,'M': 12,'N': 13,'O': 14,'P': 15,'Q': 16,'R': 17,'S': 18,'T': 19,
          'U': 20,'V': 21,'W': 22,'X': 23,'Y': 24,'Z': 25}

# 表单资源ID链接合成
Gzh = []
for i in range(sheetRows, sheetRowe):
    Gzh.append('http://zs.xiguaji.com/MBiz/AsyncSearch?keyword=' + sheet.cell_value(i, colDec[sheetCol]).strip('\n') + '&rnd=1')
    # fS.append(int(sheet.cell_value(i, colDec[fenSi])))

# 表单资源ID合成链接打印测试
# print(Gzh)
# print(fS)

# 保存西瓜搜索公众号ID的5页结果
# gzhLink = []

F = sheetRows

# 爬虫
def get_Gurl(url):
    web_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(web_data.text, 'lxml')
    global F
    FS = sheet.cell_value(F, colDec[fenSi])

    if len(soup.find_all('a')) == 0:
        print('null')

    else:
        url_2 = 'http://zs.xiguaji.com' + soup.find_all('a')[0].get('href').strip('#')
        final_data = requests.get(url_2, headers= headers)
        soup = BeautifulSoup(final_data.text, 'lxml')

        gzhName = soup.select('body > div.wrapper.wrapper-no-gap.page-popular-list > div.public-details-info.clearfix > div.col.col-lg-6.mp-account-header > div.clearfix > div > div > span')
        gzhId = soup.select('body > div.wrapper.wrapper-no-gap.page-popular-list > div.public-details-info.clearfix > div.col.col-lg-6.mp-account-header > div.clearfix > div > div > em')
        gzhHf = soup.select('body > div.wrapper.wrapper-no-gap.page-popular-list > div.public-details-info.clearfix > div.col.col-lg-6.mp-account-header > ul > li:nth-of-type(1) > span')

        for (gzhNames, gzhIds, gzhHfs) in zip(gzhName, gzhId, gzhHf):
            data = {
                '公众号': gzhNames.get_text(),
                'ID': gzhIds.get_text(),
                '活粉': gzhHfs.get_text()
            }
            print(str(data) + ' 金额：' + str(FS))
        time.sleep(0.5)
    F += 1

    # 循环显示西瓜搜索公众号单页所有公众号ID链接
    # for link in soup.find_all('a'):
    #     if str(link.get('href'))[0] == '#':
    #         gzhLink.append(link.get('href'))
    #         print(link.get('href'))

# 调用爬虫
for urls in Gzh:
    get_Gurl(urls)
# 调用单页Demo
# get_Gurl('http://zs.xiguaji.com/MBiz/AsyncSearch?keyword=vip66&rnd=508.65404276570337')

