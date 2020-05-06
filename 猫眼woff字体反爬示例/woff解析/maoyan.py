import re
import time
import difflib
import requests
import os
import urllib
from fontTools.ttLib.ttFont import TTFont
from pprint import pprint

# woff反爬
# 难点：爬下来的数字是个特殊符号，并且其对应的字符编码每次请求都会改变，
# 线索：虽然字符编码数不胜数轮番上阵，但表示某个数字的字符编码们有着唯一坐标，（坐标——多种编码——数字）
# 过程：下载一个woff文件，
#       通过fonttool找到编码与坐标的对应关系，通过手动python找到数字与编码的对应关系，从而找到数字与坐标的关系，这个关系是唯一的，无论字符编码怎么改变
#       在新的请求中爬取内容，得到特殊符号，解析字符编码，通过fonttool找到坐标，通过之前的对应关系找到数字
#       得到结果
#
# 然而以上并不成立，对应的坐标只是大致相同

crawl_url = 'https://maoyan.com/films/344869'

# 建立第坐标与数字对应关系
font = TTFont('maoyan7.woff')

FONT = { "uniE723":"0",
        "uniF4EF":"3",
        "uniF259":"7",
        "uniED7A":"5",
        "uniF202":"2",
        "uniE99E":"4",
        "uniEA38":"9",
        "uniED43":'1',
        "uniE153":'8',
        "uniE1DC":'6'}

dic = {font['glyf'][i].coordinates.array.tobytes().hex():FONT[i] for i in font.getGlyphOrder()[2:]}

# 下载当前页面woff文件
def get_cookies(cookies_string):
    cookies_string = '; ' + cookies_string + ';'
    keys = re.findall('; (.*?)=', cookies_string)
    values = re.findall('=(.*?);', cookies_string)
    cookies = dict(zip(keys, values))
    return cookies

cookies_str = '__mta=46011163.1586164010929.1586518522667.1586522393594.17; uuid_n_v=v1; uuid=3A8EEC5077E611EAB94CB3AA241DB1BC2B262789B09744949DDABB9017794081; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_cuid=1714ebe0c91c8-0df0ece2c085eb-3a36510f-144000-1714ebe0c91c8; _lxsdk=3A8EEC5077E611EAB94CB3AA241DB1BC2B262789B09744949DDABB9017794081; mojo-uuid=841eeb4e30d6c9694e330b8659315f92; __mta=46011163.1586164010929.1586164010929.1586440736365.2; _csrf=705df182c262270ac02e678ed0a7a9c3cc8eb7d4a9285bd5a6cb1f9a1458ea04; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1586164010,1586437425,1586518481; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1586522393; _lxsdk_s=171645279d4-3f5-3b3-422%7C%7C1'
cookies = get_cookies(cookies_str)
user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
headers = {
    'User-Agent':user_agent
}
r = requests.get(crawl_url,headers=headers,cookies=cookies)
woff = re.findall("<style>[\s\S]*url\('([\s\S]*)'\) format\('woff'\)[\s\S]*</style>",r.text)[0]
path = os.path.join('./font',os.path.basename(woff))
urllib.request.urlretrieve('http:{}'.format(woff),path)


# 建立第坐标与当前编码对应关系
font = TTFont(path)
dic2 = {font['glyf'][i].coordinates.array.tobytes().hex():i for i in font.getGlyphOrder()[2:]}


# 连接当前编码与数字的关系
dic3 = {}
for i in dic:
    res2 = 0
    for j in dic2:
        res = difflib.SequenceMatcher(None, i, j).quick_ratio()
        if res > res2 or res2 == None:
            res2 = res
            key_point = j
    dic3[dic2[key_point]] = dic[i]



#爬取内容 解析数据
def symbol_parse(original):                   #将特殊符号解析成数字
    parse = original.upper().split('&#X')     #['', 'E6A0;', 'F627;.', 'E727;', 'E60C;']
    res = ''
    for i in parse:
        if not i == '':
            parse2 = 'uni'+ i.replace(';','')
            res = res + parse2
    for i in dic3:
        res = res.replace(i,dic3[i])
    return res

original_info = re.findall('<span class="stonefont">([\s\S]*?)</span>',r.text)      #'&#xe6a0;&#xf627;.&#xe727;&#xe60c;'
result = []
for i in original_info:
    result.append(symbol_parse(i))

box_unit = re.findall('<span class="unit">([\s\S]*?)</span>',r.text)[0]


print('评分:',result[0],'\n票房:',result[2],box_unit)















