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
from org.apache.lucene.search.highlight import Highlighter
from org.apache.lucene.search.highlight import QueryScorer
from org.apache.lucene.search.highlight import SimpleFragmenter
from org.apache.lucene.search.highlight import SimpleHTMLFormatter
from org.apache.lucene.analysis.cjk import CJKAnalyzer

#import jpype
command = ""
numDocs = 0
results = []


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
    global numDocs, results
    print()
    numDocs = 0
    results = []
    if not command:
        return 
    query = QueryParser("contents", analyzer).parse(command)
    formatter = SimpleHTMLFormatter("<font color='red'>", "</font>")
    fragmentScorer =  QueryScorer(query)
    highlighter = Highlighter(formatter, fragmentScorer)
    fragmenter = SimpleFragmenter(50)
    highlighter.setTextFragmenter(fragmenter)
    scoreDocs = searcher.search(query, 50).scoreDocs
    numDocs = len(scoreDocs)
    for i, scoreDoc in enumerate(scoreDocs):
        doc = searcher.doc(scoreDoc.doc)
        docContent = doc.get("contents")
        hc = highlighter.getBestFragment(analyzer, "contents", docContent)
        if (not hc):
            if(len(docContent)>=50) :
                hc = docContent[0:50]
            else :
                hc = docContent
        try:
            results += [[doc.get("path"), hc, doc.get("url"), doc.get("title")]]
        except:
            i = 0
        # print 'explain:', searcher.explain(query, scoreDoc.doc)

		

def main():
    STORE_DIR = "index"
    try:
        vm_env = lucene.initVM(vmargs=['-Djava.awt.headless=true'])
        print ('lucene', lucene.VERSION)
    except:
        vm_env = lucene.getVMEnv()
    vm_env.attachCurrentThread()
    directory = SimpleFSDirectory(File(STORE_DIR).toPath())
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = CJKAnalyzer()#Version.LUCENE_CURRENT)
    run(searcher, analyzer)
    del searcher

if __name__ == '__main__':
    main()
