# Assignment 3 for SJTU EE208
> 521030910013 Shixiang Song

This assignment contains three parts: the sorce code, the assignment report, and the ```REAMDME``` document.

## The source code
The source code of this assignemnt is by Python. To run the assignemnt successfully, you have to install ```BeautifulSoup``` and ```lxml``` advancedly. You may need also install `threading` and `queue` if necessarily.

## The report
The report of this assignemnt is written by LaTeX. To make the document lighter, we only provide PDF version.

# The souce code
The source code is divided into two folders: `exercise1` and `exercise2`. The `exercise1` is for exercise 1. Our real source codes are `myHash.py`, while others are given. The testing files is in `HashCheck.` The `exercise2` is for exercise2. 

<font color = red><strong>
**NOTICE:``crawler.py`` and `crawler_thread.py` cannot run idividually. To run the code, the following two methods are both available!**
</strong></font>

Method 1:
```
python crawler.py https://www.sjtu.edu.cn bfs 10
```
Method 2
```
python
>>> from crawler import *
>>> crawl("https://www.sjtu.edu.cn", "bfs", 10)
```
**Additianal NOTICE:** Method 2 may create some unnecessary outputs, since the Python IDLE interpreter will also print the return value.

The `crawler_thread.py` is all the same but the second parameter should be omitted.

The file framework is as follows:

    -- REAMDME.md
    -- report.pdf
    -- code
        -- exercise1
            -- GeneralHashFunctions
                -- GeneralHashFunctions.py
                -- HashTest.py
            -- HashCheck
                -- test1.txt
                -- test2.txt
                -- test3.txt
                -- test4.txt
            -- Bitarray.py
            -- myHash.py
        -- exercise2
            -- crawler.py
            -- crawler_thread.py


