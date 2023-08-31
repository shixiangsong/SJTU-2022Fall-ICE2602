# SJTU EE208
import time
import re
import urllib.parse
import urllib.request
from http import cookiejar

from bs4 import BeautifulSoup

# 1. 构建一个CookieJar对象实例来保存cookie
cookie = cookiejar.CookieJar()
# 2. 使用HTTPCookieProcessor()来创建cookie处理器对象，参数为CookieJar()对象
cookie_handler = urllib.request.HTTPCookieProcessor(cookie)
# 3. 通过build_opener()来构建opener
opener = urllib.request.build_opener(cookie_handler)
# 4. addheaders接受一个列表，里面每个元素都是一个headers信息的元组，opener附带headers信息
opener.addheaders =[("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.50")] # 本机Edge报头
# 5. 需要登陆的账号和密码, 此处需要使用你们自己注册的账号密码
data = {"username": "_Pikachu",
        "pwd": "SJTUEE208",
        "formhash": "4A95C39D38",
        "backurl": "https%3A%2F%2Fwww.yaozh.com%2F"}
sign_in_url = "https://www.yaozh.com/login/"
info_url = "https://www.yaozh.com/member/basicinfo/"
# 6. 通过urlencode转码
postdata = urllib.parse.urlencode(data).encode("utf8")
# 7. 构建Request请求对象，包含需要发送的用户名和密码
request = urllib.request.Request(sign_in_url, data=postdata,headers = dict(Referer = sign_in_url))
# 8. 通过opener发送这个请求，并获取登陆后的Cookie值
opener.open(request)
# 9. opener包含用户登陆后的Cookie值，可以直接访问那些登陆后才能访问的页面
response = opener.open(info_url).read()
# 10. The rest is done by you
# 创建一个soup并爬取对应的链接
soup = BeautifulSoup(response,features="lxml")
my_identity = soup.find("div",{"class":"U_myinfo clearfix"})
# 注意到值在<input value=...>中，因此需要打印出该信息即可
print("真实姓名:\t"+my_identity.contents[3].find("input").get("value",""))
print("用户名：\t"+my_identity.contents[5].find("input").get("value",""))
print("性别：  \t"+my_identity.contents[7].find("input").get("value",""))
print("出生年月：\t"+my_identity.contents[9].find("input").get("value",""))
# 个人简介为直接的文字
print("个人简介：\t"+my_identity.contents[11].find("textarea").contents[0])