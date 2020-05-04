"""
爬取知乎首页推荐的问题：
打开知乎首页不停往下滑动发现能不停的加载知乎推荐的问题
但打开f12的network发现这些问题都是同一个url返回的，这个url似乎能随机的返回票数高的问题
这个url返回的是一个json数据，里面有问题的id，找到id，构建问题详情的url：https://www.zhihu.com/question/{}
在这个页面可以直接爬取问题和问题摘要，但是下面的答案内容仍然是异步加载的
异步加载的url形式为下面定义的变量字符串more_a，更改里面的offset可以得到不同的答案内容
这个url返回的仍然是json数据，里面有答案内容的信息，但是是一个html字符串，我把它直接写到了一个html文件里

关于反爬：只需注意headers和cookies
"""

import requests
import cookies_parse
import re
from lxml import etree
import os
import pymysql

# 起始url
url = 'https://www.zhihu.com/api/v3/feed/topstory/recommend?session_token=d6bbc3410aeac6592126988a1354180b&desktop=true&page_number=6&limit=6&action=down&after_id=29&ad_interval=-1'
# 更多回答url
more_a = 'https://www.zhihu.com/api/v4/questions/{}/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%2Cpaid_info%2Cpaid_info_content%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit=5&offset={}&platform=desktop&sort_by=default'

cookies = '_zap=b4a13056-7420-432a-868a-a0d15c124486; d_c0="ANDaSTrF6xCPTlTl4ihrNkHBnBd8ZCLDYQc=|1583480192"; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1587957029,1588074587,1588121409,1588130627; _ga=GA1.2.1644448594.1585048229; capsion_ticket="2|1:0|10:1588130762|14:capsion_ticket|44:MjA5YjRjOTY2MjBhNGIzNzk0YzRjYTBiNzJmYWZiOWQ=|f886063d35fb9c7c73b9b1462e3dfadb42d2de56cc5dfecceb4cc92e9f9bbcac"; _gid=GA1.2.481788775.1588074587; _xsrf=bb598eee-01bc-481b-b07c-554930165686; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1588130992; KLBRSID=b33d76655747159914ef8c32323d16fd|1588131618|1588130750; SESSIONID=o7901yvWUQzjAdN7LjmKaJPwubkimsKyuFoQXpkQIir; JOID=VFoRAEufJ-hoaWdbMJrFNg7Zc2gj9BbWW14aK2DMcpQFKwURASLVRDNrZVo0hgN1rob0Cg6nckcD45hrwlOXS5M=; osd=V14UBUqcI-1taGRfNZ_ENQrcdmkg8BPTWl0eLmXNcZAALgQSBSfQRTBvYF81hQdwq4f3Dguic0QH5p1qwVeSTpI=; z_c0="2|1:0|10:1588130784|4:z_c0|92:Mi4xX013MUFnQUFBQUFBME5wSk9zWHJFQ1lBQUFCZ0FsVk40RUdXWHdDU3Zuc0lKdVM0VkVjX1F4V3NGa0E3V1Q3ejh3|b6f39174cf91757da9b921a5cdead5073e30e2ae1340c2e13f1546ee7fd3cffa"; tst=r; tshl='
cookies = cookies_parse.get_cookies(cookies)
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0'}

# 存入html文件需要先写入这个head标签以防乱码
html_head ="""<head>
                <meta charset="UTF-8">
            </head>"""

conn = pymysql.connect(host='127.0.0.1',user='root',passwd='saber2014',database='zhihu')
cur = conn.cursor()

c = 0
def answer_parse(q_url,question_data):
    import time
    time.sleep(0.4)
    global c
    answer = requests.get(q_url, headers=headers, cookies=cookies)
    data = answer.json()
    answer_list = []
    for i in data['data']:
        answer_data={}
        # answer_data['content'] = i['content']           # 回答内容
        answer_data['author'] = i['author']['name']           # 答主用户名
        answer_data['voteup_count'] = int(i['voteup_count'])          # 点赞总数

        path = os.path.curdir + '/answer/'
        if not os.path.exists(path):
            os.mkdir(path)
        path = path + str(c) + '.html'
        path = os.path.abspath(path)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html_head)
            f.write(i['content'].replace('noscript', ''))    # 提取的数据里面img标签外面包了一个noscript标签，导致存入文件的img标签显示不出来，所以我直接把它去掉了
        c += 1

        answer_data['content_path'] = path       # 回答内容对应的路径
        answer_list.append(answer_data)
        sql = 'insert into questions (question,author,path,voteup_count) values (%s,%s,%s,%s)'
        cur.execute(sql, (question_data['question'],answer_data['author'],path,answer_data['voteup_count'],))
        conn.commit()
    return answer_list

def r_question(quesion_id):
    import time
    time.sleep(1)
    question_data = {}
    url = 'https://www.zhihu.com/question/{}'.format(quesion_id)
    print(url)
    r = requests.get(url, headers=headers, cookies=cookies)
    with open('1.html', 'w', encoding='utf-8') as f:
        f.write(r.text)
    e = etree.HTML(r.text)
    question = e.xpath('//h1/text()')[0]
    detail = re.findall('"excerpt":"(.*?)","commentPermission', r.text)[0]
    question_data['question'] = question
    # question_data['detail'] = detail              # 问题详情

    answerlist=[]     # 下一个函数里处理的所有答案都将存在这个列表里

    # url里的offset参数每增加5，都返回若干条答案数据，代码先爬取前20次加载出来的答案
    for offset in range(0, 100, 5):
        a_url = more_a.format(quesion_id, offset)
        answerlist += answer_parse(a_url,question_data)
    question_data['answer'] = answerlist
    print(question_data)           # 最终的爬取结果 question_data


def run(url):
    response = requests.get(url, headers=headers, cookies=cookies)
    print(response.status_code)
    data = response.json()
    for i in data['data']:
        target_id = i['target']['id']         # 本来是答案的id，但是后来发现，其实构建url的时候可以不用
        quesion = i['target'].get('question')          # 有一些问题比较特殊，取不到这个值，问题对应的url是另外的形式，先不考虑了
        if quesion:
            quesion_id = quesion['id']
            r_question(quesion_id)
        else:
            print(None)




# 由于不停的访问这个url可以返回不同的问题，所有循环访问这个url
while True:
    run(url)