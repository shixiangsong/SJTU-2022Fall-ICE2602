# SJTU EE208

INDEX_DIR = "IndexFiles.index"

import sys, os, lucene
import math
from java.io import File
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.util import Version
from org.apache.pylucene.search.similarities import PythonSimilarity, PythonClassicSimilarity

"""
This script is loosely based on the Lucene (java implementation) demo class 
org.apache.lucene.demo.SearchFiles.  It will prompt for a search query, then it
will search the Lucene index in the current directory called 'index' for the
search query entered against the 'contents' field.  It will then display the
'path' and 'name' fields for each of the hits it finds in the index.  Note that
search.close() is currently commented out because it causes a stack overflow in
some cases.
"""

class SimpleSimilarity(PythonClassicSimilarity):

    def lengthNorm(self, numTerms):
        return 1/math.sqrt(numTerms)

    def tf(self, freq):
        return math.log(1+freq)

    def sloppyFreq(self, distance):
        return 1/(distance + 1)

    def idf(self, docFreq, numDocs):
        return math.log(numDocs/docFreq)

    def idfExplain(self, collectionStats, termStats):
        return Explanation.match(self.idf(termStats.docFreq(),collectionStats.numDocs()), "inexplicable", [])


def run(searcher, analyzer):
    # while True:
    print()
    print ("Hit enter with no input to quit.")
    # command = raw_input("Query:")
    # command = unicode(command, 'GBK')
    command = 'london author:shakespeare' 
    if command == '':
        return

    print()
    print ("Searching for:", command)
    query = QueryParser("contents", analyzer).parse(command)
    scoreDocs = searcher.search(query, 50).scoreDocs
    print ("%s total matching documents." % len(scoreDocs))

    for i, scoreDoc in enumerate(scoreDocs):
        doc = searcher.doc(scoreDoc.doc)
        print ('path:', doc.get("path"), 'name:', doc.get("name"), 'score:', scoreDoc.score)
            # print 'explain:', searcher.explain(query, scoreDoc.doc)


if __name__ == '__main__':
    STORE_DIR = "index2"
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print ('lucene', lucene.VERSION)
    #base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    directory = SimpleFSDirectory(File(STORE_DIR).toPath())
    searcher = IndexSearcher(DirectoryReader.open(directory))
    # set a new similarity computing method
    searcher.setSimilarity(SimpleSimilarity())
    analyzer = StandardAnalyzer()#Version.LUCENE_CURRENT)
    run(searcher, analyzer)
    del searcher
