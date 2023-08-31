# SJTU EE208

def get_page(page):
    return g.get(page, [])


def get_all_links(content):
    return content


def union_dfs(a, b):
    for e in b:
        if e not in a:
            a.append(e)

# 这里是第二题的答案
def union_bfs(a, b):
    for e in b:
        if e not in a:
            a.insert(0, e)


def crawl(seed, method):
    tocrawl = [seed]
    crawled = []
    graph = {}
    while tocrawl:
        page = tocrawl.pop()
        if page not in crawled:
            content = get_page(page)
            outlinks = get_all_links(content)
            graph[page] = outlinks #这里是第三题的答案
            globals()['union_%s' % method](tocrawl, outlinks)
            crawled.append(page)

    return graph, crawled


g = {'A': ['B', 'C', 'D'],
     'B': ['E', 'F'],
     'D': ['G', 'H'],
     'E': ['I', 'J'],
     'G': ['K', 'L']}


graph_dfs, crawled_dfs = crawl('A', 'dfs')
print('graph_dfs:', graph_dfs)
print('crawled_dfs:', crawled_dfs)

graph_bfs, crawled_bfs = crawl('A', 'bfs')
print('graph_bfs:', graph_bfs)
print('crawled_bfs:', crawled_bfs)
