# SJTU EE208

import os
import re
import string
from symbol import except_clause
import sys
import urllib.error
import urllib.parse
import urllib.request

from bs4 import BeautifulSoup
import time
import threading
import queue


def valid_filename(s):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    s = ''.join(c for c in s if c in valid_chars)
    s += ".html"
    return s

def get_page(page):
    content = ''
    try:
        req = urllib.request.Request(page)
        
        req.add_header('User-Agent ', "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0")# 添加报头（本机Edge）
        #print(req)
        content = urllib.request.urlopen(req,timeout=500).read()# 500ms内连接上
        
        
        #print("F")
        #print(content)
    except:
        return None
    return content

# 返回页面下所有链接
def get_all_links(content, page):
    # 如果爬不到会返回None 
    if content == None:
        return []
    links = []
    soup = BeautifulSoup(content, features="lxml", from_encoding="utf-8")
    for link in soup.findAll('a',{'href' : re.compile('^http|^/')}): #正则表达式返回链接
        mylink = link.get("href")
        if mylink[-3:] == "apk":
            return links
        elif mylink[0] == "/":
            mylink = urllib.parse.urljoin(page,mylink) #连接链接
            links.append(mylink)
        else:
            links.append(mylink)
    return links


def add_page_to_folder(page, content):  # 将网页存到文件夹里，将网址和对应的文件名写入index.txt中
    index_filename = 'index.txt'  # index.txt中每行是'网址 对应的文件名'
    folder = 'html'  # 存放网页的文件夹
    try:
        soup = BeautifulSoup(content, features="lxml")
        title = soup.title.string
    except:
        return
    try:
        filename = valid_filename(page)  # 将网址变成合法的文件名
        index = open(index_filename, 'a')
        index.write(page.encode('ascii', 'ignore').decode() + "\t" + title + '\t' + filename + "\n")
        index.close()
    except:
        return
    if not os.path.exists(folder):  # 如果文件夹不存在则新建
        os.mkdir(folder)
    try:
        content = soup.contents
    except:
        return
    f = open(os.path.join(folder, filename), 'w',encoding="utf-8")
    f.write(str(content))  # 将网页存入文件
    f.close()

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
            add_page_to_folder(page, content)
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

NUM = 4
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
