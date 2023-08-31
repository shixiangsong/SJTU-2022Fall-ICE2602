# SJTU EE208

import os
import re
import string
import sys
import urllib.error
import urllib.parse
import urllib.request

from bs4 import BeautifulSoup
import time

def valid_filename(s):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    s = ''.join(c for c in s if c in valid_chars)
    return s

# 获取页面
def get_page(page):
    content = ''
    try:
        req = urllib.request.Request(page)
        req.add_header('User-Agent ', "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0")# 添加报头（本机Edge）
        content = urllib.request.urlopen(req,timeout = 500).read()# 500ms内连接上
    except:
        return None
    return content

# 返回页面下所有链接
def get_all_links(content, page):
    # 如果爬不到会返回None 
    if content == None:
        return []
    links = []
    soup = BeautifulSoup(content, features="lxml")
    for link in soup.findAll('a',{'href' : re.compile('^http|^/')}): #正则表达式返回链接
        mylink = link.get("href")
        if mylink[0] == "/":
            mylink = urllib.parse.urljoin(page,mylink) #连接链接
            links.append(mylink)
        else:
            links.append(mylink)
    return links

def union_dfs(a, b):
    for e in b:
        if e not in a:
            a.append(e)

# 这里是第二题的答案
def union_bfs(a, b):
    for e in b:
        if e not in a:
            a.insert(0, e)


def add_page_to_folder(page, content):  # 将网页存到文件夹里，将网址和对应的文件名写入index.txt中
    index_filename = 'index.txt'  # index.txt中每行是'网址 对应的文件名'
    folder = 'html'  # 存放网页的文件夹
    filename = valid_filename(page)  # 将网址变成合法的文件名
    index = open(index_filename, 'a')
    index.write(page.encode('ascii', 'ignore').decode() + "\t" + filename + "\n")
    index.close()
    if not os.path.exists(folder):  # 如果文件夹不存在则新建
        os.mkdir(folder)
    f = open(os.path.join(folder, filename), 'w')
    f.write(str(content))  # 将网页存入文件
    f.close()

# 真正的主函数
def crawl(seed, method, max_page):
    tocrawl = [seed]
    crawled = []
    graph = {}
    count = 0

    while tocrawl:
        page = tocrawl.pop()
        if page not in crawled:
            print(page)
            # 这里是计数用
            count += 1
            if count > max_page:            
                return graph, crawled
            content = get_page(page)
            add_page_to_folder(page, content)
            outlinks = get_all_links(content, page)
            graph[page] = outlinks 
            globals()['union_%s' % method](tocrawl, outlinks)
            crawled.append(page)

    return graph, crawled

start = time.time()
if __name__ == '__main__':
    seed = sys.argv[1]
    method = sys.argv[2]
    max_page = sys.argv[3]
    max_page = int(max_page) #这里是防止系统直接调用的时候max_page是一个str格式的情况出现
    graph, crawled = crawl(seed, method, max_page)
end = time.time()
print("运行时间：{}".format(end-start))