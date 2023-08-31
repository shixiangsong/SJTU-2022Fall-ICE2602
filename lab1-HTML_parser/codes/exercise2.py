# SJTU EE208

import re
import sys
import urllib.request

from bs4 import BeautifulSoup


def parseURL(content):
    urlset = set()
    # 此处应指定features避免warning
    soup = BeautifulSoup(content,features="lxml")
    # 图片格式一般为 <img src=...>
    for k in soup.find_all('img'):
        urlset.add(k.get('src', ''))
    return urlset

# 输出结果
def write_outputs(urls, filename):
    file = open(filename, 'w', encoding='utf-8')
    for i in urls:
        file.write(i)
        file.write('\n')
    file.close()

# 主函数
def main():
    url = "http://www.baidu.com"

    content = urllib.request.urlopen(url).read()

    urlSet = parseURL(content)
    write_outputs(urlSet, "res2.txt")


if __name__ == '__main__':
    main()
