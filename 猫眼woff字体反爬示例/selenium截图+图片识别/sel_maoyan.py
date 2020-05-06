from selenium import webdriver
import pytesseract
from PIL import Image
import re

# selenium截图加图片识别获取猫眼电影woff加密的票房


def get_cookies(cookies_string):
    cookies_string = '; ' + cookies_string + ';'
    keys = re.findall('; (.*?)=', cookies_string)
    values = re.findall('=(.*?);', cookies_string)
    cookies = dict(zip(keys, values))
    return cookies


chrome_driver = 'E:\chromedriver.exe'
driver = webdriver.Chrome(executable_path=chrome_driver)
driver.implicitly_wait(time_to_wait=10)

cookies = '__mta=248273592.1586437357428.1587104820864.1587105099942.11; uuid_n_v=v1; uuid=AA67BB507A6211EA90A9E7F7829CDC84A8A1155F0CC64282B6D36692DDC843F2; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1587094201,1587094714,1587103309,1587104818; _lxsdk_cuid=1715f08feaec8-068ca95fec2a348-153b7540-144000-1715f08feafc8; _lxsdk=AA67BB507A6211EA90A9E7F7829CDC84A8A1155F0CC64282B6D36692DDC843F2; mojo-uuid=03e343b0ef867d01fbb0c99907ce8121; __mta=248273592.1586437357428.1587094714192.1587104818462.6; t_lxid=171862fa7dcc8-08d0ea7ed5a1618-153a7440-144000-171862fa7ddc8-tid; _csrf=d304ce144245e9d7a370522140b598034fd6ef435900bc78830ff381f91ea395; mojo-trace-id=6; mojo-session-id={"id":"f57ef219b5d45953a8fe349c715c12d2","time":1587103308853}; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1587105099; _lxsdk_s=17186ba9de1-dd5-ddf-733%7C%7C10; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic'
cookies_dic = get_cookies(cookies)
cookies_dic['name'] = 'wjx'
cookies_dic['value'] = 'abc'

driver.get('https://maoyan.com')
driver.add_cookie(cookies_dic)

driver.get('https://maoyan.com/board/4')
movies = driver.find_elements_by_class_name('image-link')

l = []
for i in movies:
    url = i.get_attribute('href')
    l.append(url)

for i in l:
    driver.get(i)
    try:
        office = driver.find_elements_by_class_name('stonefont')[0]          #找到标签
        print(office)
        office.screenshot('b.png')                                           #截图标签
        image = Image.open("b.png")                                          #打开截图
        text = pytesseract.image_to_string(image)                             #识别数字
        print(text)
    except:
        pass
