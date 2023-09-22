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
import threading
import queue
from lxml import etree

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
    for link in soup.findAll('li',{'class' : 'card content'}): 
        try:
            mylink = link.find("a").get("href","")
            
            if mylink[0] == "/":
                mylink = urllib.parse.urljoin(page,mylink) #连接链接
                links.append(mylink)
            else:
                links.append(mylink)
        except:
            print("Fail!")
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
    index = open(index_filename, 'a')
    filename = valid_filename(page)
    tree = etree.HTML(content)
# The rest is done by you:
    title = tree.xpath("/html/body/div[4]/main/div[1]/div/div[1]/h1")[0].text
    intro = tree.xpath("/html/body/div[4]/main/div[1]/div/div[1]/p[2]/text()")[0]
    pagesite = "https://wallpapers.com"+tree.xpath("/html/body/div[4]/main/div[1]/div/div[2]/div[1]/div[1]/picture/source/@srcset")[0]
    index.write(page.encode('ascii', 'ignore').decode() + "\t" + filename + "\t" + pagesite + "\t" + title + "\t" + intro + "\n")
    index.close()

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
            try:
                add_page_to_folder(page, content)
            except:
                a=0
            outlinks = get_all_links(content, page)
            graph[page] = outlinks 
            globals()['union_%s' % method](tocrawl, outlinks)
            crawled.append(page)

    return graph, crawled



count = 0
# 计数
size = 0
def working():
    global count, size
    # 循环终止条件
    while count < max_page:
        page = q.get()
        if page not in crawled:
            content = get_page(page)
            try:
                add_page_to_folder(page, content)
            except Exception as e:
                print(e)
            outlinks = get_all_links(content, page)
            if size < max_page:
                if varLock.acquire():
                    for link in outlinks:
                        q.put(link)
                        size += 1
                    graph[page] = outlinks
                    print(page)
                    crawled.append(page)
                    count += 1
                    varLock.release()
            else:
                if varLock.acquire():
                    print(page)
                    crawled.append(page)
                    count+=1
                    varLock.release()
        q.task_done()
        #pend = time.time()
        #print(str(pend-pstart)+"\\\\")
    else:
        # 强制清空队列
        while not q.empty():
            #end = time.time()
            #global start
            #print(end-start)
            if varLock.acquire():
                q.get()
                q.task_done()
                varLock.release()
          
           # print(web)
        #t = threading.currentThread()
        #print('Thread id : {}\\\\'.format(t.getName()))
        #time.sleep(10)# 避免误杀进程
        q.task_done()
        
     
# 使用sys
if __name__ == '__main__':
    global seed, max_page
    seed = sys.argv[1]
    max_page = sys.argv[2]
    max_page = int(max_page)

#seed = "https://www.sina.cn"
#max_page = 150

start = time.time()

NUM = 10
crawled = []
graph = {}
varLock = threading.Lock()
q = queue.Queue()
q.put(seed)
for i in range(NUM):
    t = threading.Thread(target=working)
    t.setDaemon(True)
    print("线程{}正在进行".format(i))
    t.setName("线程{}".format(i))
    t.start()
    
q.join() #这里如果队列不清空，它会一直等下去

end = time.time()
print("运行时间：{}".format(end - start))

