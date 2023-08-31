# SJTU EE208

import re
import urllib.parse
import urllib.request
from http import cookiejar
from lxml import etree

from bs4 import BeautifulSoup

# 1. 构建一个CookieJar对象实例来保存cookie
cookie = cookiejar.CookieJar()
# 2. 使用HTTPCookieProcessor()来创建cookie处理器对象，参数为CookieJar()对象
cookie_handler = urllib.request.HTTPCookieProcessor(cookie)
# 3. 通过build_opener()来构建opener
opener = urllib.request.build_opener(cookie_handler)
# 4. addheaders接受一个列表，里面每个元素都是一个headers信息的元组，opener附带headers信息
opener.addheaders = [("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.50")] # 本机Edge报头
# 5. 需要登陆的账号和密码, 此处需要使用你们自己注册的账号密码
data = {"username": "_Pikachu",
        "password": "SJTUEE208"}

sign_in_url = "https://www.zhihu.com/signin"

# * 将这里的个人主页替换成你自己的主页 *
info_url = "https://tech.huanqiu.com/article/4AQSI2UxTlc" 
# 6. 通过urlencode转码
postdata = urllib.parse.urlencode(data).encode("utf8")
# 7. 构建Request请求对象，包含需要发送的用户名和密码
request = urllib.request.Request(sign_in_url)
# 8. 通过opener发送这个请求，并获取登陆后的Cookie值
opener.open(request)
# 9. opener包含用户登录后的Cookie值，可以直接访问那些登录后才能访问的页面
response = opener.open(info_url).read()
# 10. 解析HTML
tree = etree.HTML(response)
# The rest is done by you:
myname = tree.xpath("/html/body/div[1]/div/main/div/div[1]/div/div[2]/div/div[2]/div[1]/h1/span[1]")[0].text
my_signature = tree.xpath("/html/body/div[1]/div/main/div/div[1]/div/div[2]/div/div[2]/div[1]/h1/span[2]")[0].text
print("用户名：\t"+myname)
print("个性签名：\t"+my_signature)
# 以防止这个问题不是赞同回答是关注问题
try:
    question1 = tree.xpath("/html/body/div[1]/div/main/div/div[2]/div[1]/div/div[3]/div/div[2]/div[1]/div[2]/div/h2/div/meta[2]")[0].get("content")
    answer1 = tree.xpath("/html/body/div[1]/div/main/div/div[2]/div[1]/div/div[3]/div/div[2]/div[1]/div[2]/div/div[2]/span/div/span/text()")[0]
    print("问题1：  \t"+question1)
    print("回答1：  \t"+answer1)
except:
    print("问题1 Error:\t这个标签不是赞同的回答")
try:
    question2 = tree.xpath("/html/body/div[1]/div/main/div/div[2]/div[1]/div/div[3]/div/div[2]/div[2]/div[2]/div/h2/div/meta[2]")[0].get("content")
    answer2 = tree.xpath("/html/body/div[1]/div/main/div/div[2]/div[1]/div/div[3]/div/div[2]/div[2]/div[2]/div/div[2]/span/div/span/text()")[0]
    print("问题2：  \t"+question2)
    print("回答2：  \t"+answer2)
except:
    print("问题2 Error:\t这个标签不是赞同的回答")