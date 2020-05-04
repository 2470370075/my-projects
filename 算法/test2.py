email_list= ["xiaoWang@163.com","xiaoWang@163.comheihem", ".com.xiaowang@qq.com" ]

for i in email_list:
    import re
    if re.findall('163.com$',i):
        print(i)

s = "xiaoWang@163.com"
