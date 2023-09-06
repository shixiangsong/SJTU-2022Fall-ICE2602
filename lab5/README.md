# Assignment 5 for SJTU EE208
> 521030910013 Shixiang Song

This assignment contains three parts: the sorce code, the assignment report, and the ```REAMDME``` document.

## The source code
The source code of this assignemnt is by Python. To run the assignemnt successfully, you have to install ```BeautifulSoup``` and ```lxml``` advancedly. You may need also install `java` and `pylucene`  if it is not installed. The install method could be referred in https://lucene.apache.org/pylucene/install.html. 

## The report
The report of this assignemnt is written by LaTeX. To make the document lighter, we only provide PDF version.

# The souce code
The core code is in the folder `exercise1` and `exercise2` for the two exercises, with the source code and necessary auxauray dcouments.

In exercise1, we have already crawled and made index, so you just need to run `SearchFiles.py`.

In exercise2, we have also done these steps. If you need to crawl the website yourself, ***you need to turn on VPN when you are in China Mainland***. To run the code, please separately run `crawl.py`, `divide.py`, `IndexFiles.py`, and `SearchFiles.py`.


The file framework is as follows:

    -- REAMDME.md
    -- report.pdf
    -- exercise1
        -- html
        -- index 
        -- index.txt
        -- crawler_thread.py
        -- IndexFiles.py
        -- SearchFiles.py
    -- exercise2
        -- img
        -- index 
        -- index.txt
        -- crawler.py
        -- IndexFiles.py
        -- SearchFiles.py
        -- divide.py


