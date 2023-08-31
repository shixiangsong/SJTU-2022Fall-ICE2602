import crawler
import time
start = time.time()
crawler.crawl("https://www.sjtu.edu.cn", "bfs", 10)
end = time.time()
print("运行时间：{}".format(end-start))
#print("↑DFS------我是分割线------BFS↓")
#crawler.crawl("https://www.sjtu.edu.cn", "bfs", 10)