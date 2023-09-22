# SJTU EE208

INDEX_DIR = "IndexFiles.index"

import sys, os, lucene

from java.io import File
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.util import Version

from org.apache.lucene.analysis.cjk import CJKAnalyzer

#import jpype



"""
This script is loosely based on the Lucene (java implementation) demo class 
org.apache.lucene.demo.SearchFiles.  It will prompt for a search query, then it
will search the Lucene index in the current directory called 'index' for the
search query entered against the 'contents' field.  It will then display the
'path' and 'name' fields for each of the hits it finds in the index.  Note that
search.close() is currently commented out because it causes a stack overflow in
some cases.
"""
def run(searcher, analyzer):
    while True:
        print()
        print ("Hit enter with no input to quit.")
        command = input("Query:")
            #command = unicode(command, 'utf-8')
            #command = 'london author:shakespeare' 
        if command == '':
            return

        print()
        print ("Searching for:", command)
        query = QueryParser("contents", analyzer).parse(command)
        scoreDocs = searcher.search(query, 50).scoreDocs
        print ("%s total matching documents." % len(scoreDocs))

        for i, scoreDoc in enumerate(scoreDocs):
            doc = searcher.doc(scoreDoc.doc)
            try:
                print ('path:', doc.get("path"))
                print( 'name:', doc.get("name"))
                print("url:", doc.get("url")) 
                print("title:", doc.get("title"))
                print('------')
            except:
                continue
                # print 'explain:', searcher.explain(query, scoreDoc.doc)


if __name__ == '__main__':
    STORE_DIR = "index"
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print ('lucene', lucene.VERSION)
    #base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    directory = SimpleFSDirectory(File(STORE_DIR).toPath())
    searcher = IndexSearcher(DirectoryReader.open(directory))
    # 引入jpype模块
    """
    ①、使用jpype开启jvm
    ②、加载java类
    ③、调用java方法
    ④、关闭jvm
    """
    # ①、使用jpype开启虚拟机（在开启jvm之前要加载类路径）
    # 加载刚才打包的jar文件
   # jar_path = './lucene-analyzers-smartcn-8.6.1.jar'
    # 获取jvm.dll 的文件路径
    #jvmPath = jpype.getDefaultJVMPath()

    # 启动jvm
    #jpype.startJVM(jvmPath, "-ea", "-Djava.class.path=%s" % jar_path)

    # ②、加载java类（参数是java的长类名）
   # javaClass = jpype.JClass("SmartChineseAnalyzer")
    
    
    analyzer = CJKAnalyzer()#Version.LUCENE_CURRENT)
    run(searcher, analyzer)
    del searcher
    # ④、关闭jvm:jvm随着python程序的退出而结束
   # jpype.shutdownJVM()
