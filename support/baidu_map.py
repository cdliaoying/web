import requests
import re
import csv
import time


def BusinessFromBaiduDitu(citycode = '287',key_word='筛网',pageno=0):
    parameter = {
        "newmap": "1",
        "reqflag": "pcmap",
        "biz": "1",
        "from": "webmap",
        "da_par": "direct",
        "pcevaname": "pc4.1",
        "qt": "con",
        "c": citycode,        # 城市代码
        "wd": key_word,       # 搜索关键词
        "wd2": "",
        "pn": pageno,         # 页数
        "nn": pageno * 10,
        "db": "0",
        "sug": "0",
        "addr": "0",
        "da_src": "pcmappg.poi.page",
        "on_gel": "1",
        "src": "7",
        "gr": "3",
        "l": "12",
        "tn": "B_NORMAL_MAP",
        # "u_loc": "12621219.536556,2630747.285024",
        "ie": "utf-8",
        # "b": "(11845157.18,3047692.2;11922085.18,3073932.2)",  #这个应该是地理位置坐标，可以忽略
        "t": "1468896652886"}

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) '
                             'AppleWebKit/537.36(KHTML, like Gecko) Chrome/56.0.2924.87Safari/537.36'}

    url = 'http://map.baidu.com/'
    htm = requests.get(url, params=parameter, headers=headers)
    htm = htm.text.encode('latin-1').decode('unicode_escape')  # 转码
    pattern = r'(?<=\baddress_norm":"\[).+?(?="ty":)'
    htm = re.findall(pattern, htm)  # 按段落匹配

    for r in htm:
        pattern = r'(?<=\b"\},"name":").+?(?=")'
        name = re.findall(pattern, r)
        if not name:
            pattern = r'(?<=\b,"name":").+?(?=")'
            name = re.findall(pattern, r)
        # print(name[0])  # 名称

        pattern = r'.+?(?=")'
        adr = re.findall(pattern, r)
        pattern = r'\(.+?\['
        address = re.sub(pattern, ' ', adr[0])
        pattern = r'\(.+?\]'
        address = re.sub(pattern, ' ', address)
        #print(address)  # 地址

        pattern = r'(?<="phone":").+?(?=")'
        phone = re.findall(pattern, r)
        try:
            if phone[0] and '",' != phone[0]:
                phone_list = phone[0].split(sep=',')
                for number in phone_list:
                    if re.match('1', number):
                        print(citycode+name[0]+','+address+','+number)
                        writer.writerow((name[0], address, number))
        except:
            continue
    print(citycode + '  ' + key_word + '  ' + str(pageno))


citynumlist = ['33','34','35','370','371','372']
keywordlist = ['丝网','筛网']

start = time.time()
num = 1

# 建立csv文件，保存数据
csvFile = open(r'/Users/apple888/PycharmProjects/百度地图/Data/%s.csv' % 'CityData','a+', newline='', encoding='utf-8')
writer = csv.writer(csvFile)
writer.writerow(('name', 'address', 'number'))


for citycode in citynumlist:
    for kw in keywordlist:
        for page in range(10):
            BusinessFromBaiduDitu(citycode=citycode, key_word=kw, pageno=page)

            # 防止访问频率太高，避免被百度公司封
            time.sleep(1)
            if num%20 == 0:
                time.sleep(2)
            if num%100 == 0:
                time.sleep(3)
            if num%200 ==0:
                time.sleep(7)
            num = num + 1

end = time.time()
lasttime = int((end-start))
print('耗时'+str(lasttime)+'s')