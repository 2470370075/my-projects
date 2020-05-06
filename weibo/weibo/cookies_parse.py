import re
def get_cookies(cookies_string):
    cookies_string = '; '+cookies_string+';'
    print(cookies_string)
    keys = re.findall('; (.*?)=',cookies_string)
    values = re.findall('=(.*?);',cookies_string)
    cookies = dict(zip(keys,values))
    return cookies