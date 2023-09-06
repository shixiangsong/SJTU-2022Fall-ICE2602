# SJTU EE208

INDEX_DIR = "IndexFiles.index"

import sys, os, lucene, threading, time, re
from datetime import datetime

from java.io import File
from java.nio.file import Path
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType, StringField, TextField
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version

from org.apache.lucene.analysis.cjk import CJKAnalyzer
"""
This class is loosely based on the Lucene (java implementation) demo class 
org.apache.lucene.demo.IndexFiles.  It will take a directory as an argument
and will index all of the files in that directory and downward recursively.
It will index on the file path, the file name and the file contents.  The
resulting Lucene index will be placed in the current directory and called
'index'.
"""

class Ticker(object):

    def __init__(self):
        self.tick = True

    def run(self):
        while self.tick:
            sys.stdout.write('.')
            sys.stdout.flush()
            time.sleep(1.0)

class IndexFiles(object):
    """Usage: python IndexFiles <doc_directory>"""

    def __init__(self, root, storeDir, analyzer):

        if not os.path.exists(storeDir):
            os.mkdir(storeDir)

        store = SimpleFSDirectory(File(storeDir).toPath())
        analyzer = LimitTokenCountAnalyzer(analyzer, 1048576)
        config = IndexWriterConfig(analyzer)
        config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
        writer = IndexWriter(store, config)

        self.indexDocs(root, writer)
        ticker = Ticker()
        print('commit index')
        threading.Thread(target=ticker.run).start()
        writer.commit()
        writer.close()
        ticker.tick = False
        print('done')

    def getTxtAttribute(self, contents, attr):
        m = re.search(attr + ': (.*?)\n',contents)
        if m:
            return m.group(1)
        else:
            return ''
    def indexDocs(self, root, writer):   
        for root, dirnames, filenames in os.walk(root):
            for filename in filenames:
                if not filename.endswith('.txt'):
                    continue
                print("adding", filename)
                # try:
                path = os.path.join(root, filename)
                file = open(path, encoding='utf8')
                contents = file.read()
                file.close()
                doc = Document()
                # doc.add(Field("name", filename,
                #                      Field.Store.YES,
                #                      Field.Index.NOT_ANALYZED))
                doc.add(StringField("name", filename, Field.Store.YES))
                # doc.add(Field("path", path,
                #                      Field.Store.YES,
                #                      Field.Index.NOT_ANALYZED))
                doc.add(StringField("path", path, Field.Store.YES))
                if len(contents) > 0:
                    title = self.getTxtAttribute(contents, 'Title')
                    author = self.getTxtAttribute(contents, 'Author')
                    language = self.getTxtAttribute(contents, 'Language')
                    # doc.add(Field("title", title,
                    #                      Field.Store.YES,
                    #                      Field.Index.ANALYZED))
                    # doc.add(Field("author", author,
                    #                      Field.Store.YES,
                    #                      Field.Index.ANALYZED))
                    # doc.add(Field("language", language,
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
                # except Exception as e:
                #     print("Failed in indexDocs:", e)

if __name__ == '__main__':
    """
    if len(sys.argv) < 2:
        print IndexFiles.__doc__
        sys.exit(1)
    """
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print('lucene', lucene.VERSION)
    start = datetime.now()
    try:
        """
        base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        IndexFiles(sys.argv[1], os.path.join(base_dir, INDEX_DIR),
                   StandardAnalyzer(Version.LUCENE_CURRENT))
                   """
        analyzer = StandardAnalyzer()
        IndexFiles('testfolder', "index", analyzer)
        end = datetime.now()
        print(end - start)
    except Exception as e:
        print("Failed: ", e)
        raise e
