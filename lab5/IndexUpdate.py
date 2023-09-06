# SJTU EE208

import sys, os, lucene, time, re
from java.io import File
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType, StringField, TextField
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexReader ,IndexWriterConfig, Term, DirectoryReader
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher, TermQuery
from org.apache.lucene.util import Version

class IndexUpdate(object):
    def __init__(self, storeDir):
        lucene.initVM(vmargs=['-Djava.awt.headless=true'])
        print('lucene', lucene.VERSION)
        self.dir = SimpleFSDirectory(File(storeDir).toPath())


    def getTxtAttribute(self, contents, attr):
        m = re.search(attr + ': (.*?)\n',contents)
        if m:
            return m.group(1)
        else:
            return ''
        
    def testDelete(self, fieldName, searchString):
        config = IndexWriterConfig(self.getAnalyzer())
        config.setOpenMode(IndexWriterConfig.OpenMode.APPEND)
        writer = IndexWriter(self.dir, config)
        writer.deleteDocuments(Term(fieldName, searchString))
        writer.close()

        
    def testAdd(self, filepath):
        config = IndexWriterConfig(self.getAnalyzer())
        config.setOpenMode(IndexWriterConfig.OpenMode.CREATE_OR_APPEND)
        writer = IndexWriter(self.dir, config)
        
        file = open(filepath, encoding='gbk')
        contents = file.read()
        file.close()
        doc = Document()
        # doc.add(Field("name", os.path.basename(filepath),
        #                      Field.Store.YES,
        #                      Field.Index.NOT_ANALYZED))
        doc.add(StringField('name', os.path.basename(filepath), Field.Store.YES))
        # doc.add(Field("path", filepath,
        #                      Field.Store.YES,
        #                      Field.Index.NOT_ANALYZED))
        doc.add(StringField('path', filepath, Field.Store.YES))
        if len(contents) > 0:
            title = self.getTxtAttribute(contents, 'Title')
            author = self.getTxtAttribute(contents, 'Author')
            language = self.getTxtAttribute(contents, 'Language')
            # doc.add(Field("Title", title,
            #                      Field.Store.YES,
            #                      Field.Index.ANALYZED))
            # doc.add(Field("Author", author,
            #                      Field.Store.YES,
            #                      Field.Index.ANALYZED))
            # doc.add(Field("Language", language,
            #                      Field.Store.YES,
            #                      Field.Index.ANALYZED))
            # doc.add(Field("contents", contents,
            #                      Field.Store.NO,
            #                      Field.Index.ANALYZED))
            doc.add(TextField('title', title, Field.Store.YES))
            doc.add(TextField('author', author, Field.Store.YES))
            doc.add(TextField('language', language, Field.Store.YES))
            doc.add(TextField('contents', contents, Field.Store.YES))
        else:
            print("warning: no content in %s" % filename)
        writer.addDocument(doc)
        writer.close()


    def getHitCount(self, fieldName, searchString):
        reader = DirectoryReader.open(self.dir) #readOnly = True
        print('%s total docs in index' % reader.numDocs())
        
        searcher = IndexSearcher(reader) #readOnly = True
        t = Term(fieldName, searchString)
        query = TermQuery(t)
        hitCount = len(searcher.search(query, 50).scoreDocs)

        reader.close()
        print("%s total matching documents for %s\n---------------" \
              % (hitCount, searchString))
        return hitCount


    def getAnalyzer(self):
        return StandardAnalyzer()

if __name__ == '__main__':
    try:
        fn = 'pg17565.txt'
        index = IndexUpdate('index')
        print(index.getHitCount('name', fn))

        print('delete %s' % fn)
        index.testDelete('name', fn)
        index.getHitCount('name', fn)

        print('add %s' % fn)
        index.testAdd('testfolder/%s' % fn)
        index.getHitCount('name', fn)
    except Exception as e:
        print("Failed: ", e)

