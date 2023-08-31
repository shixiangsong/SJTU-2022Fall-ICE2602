# SJTU EE208

import contextlib
import re
import sys
import urllib.parse
import urllib.request

from bs4 import BeautifulSoup


def parseZhihuDaily(content, url):
    # 创建目标列表
    zhihulist = list()
    # 此处应指定features避免warning
    soup = BeautifulSoup(content,features="lxml")
    # 找到每一个链接（即boxes）通用格式为<div class = "box"><a href="....."><img><span>...</a></div>
    for boxes in soup.find_all("div",{"class":"box"}):
        # 直接调用boxes内部的img span 和 链接
        image = boxes.find("img").get("src","")
        title = boxes.find("span").contents[0]
        link = boxes.find("a").contents[0].get("href","")
        # 将链接和daily.zhihu.com连起来
        fulllink = urllib.parse.urljoin("http://daily.zhihu.com/",link)
        zhihu = [image, title, fulllink]
        zhihulist.append(zhihu)
    return zhihulist

# 输出函数
def write_outputs(zhihus, filename):
    file = open(filename, "w", encoding='utf-8')
    for zhihu in zhihus:
        for element in zhihu:
            file.write(element)
            file.write('\t')
        file.write('\n')
    file.close()

# 主函数
def main():
    url = "http://daily.zhihu.com/"
    req = urllib.request.Request(url)
    req.add_header('User-Agent ', "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0")# 本机Firefox的报头
    content = urllib.request.urlopen(req).read()
    zhihus = parseZhihuDaily(content, url)
    write_outputs(zhihus, "res3.txt")


if __name__ == '__main__':
    main()
 