# Assignment 7 for SJTU EE208
> 521030910013 Shixiang Song

This assignment contains three parts: the sorce code, the assignment report, and the ```REAMDME``` document.

## The source code
The source code of this assignemnt is by Python and HTML. To run the assignemnt successfully, you have to install ```BeautifulSoup``` and ```lxml``` advancedly. You may need also install `java` and `pylucene` and flask template if necessary. if it is not installed. The install method could be referred in https://lucene.apache.org/pylucene/install.html. 

## The report
The report of this assignemnt is written by LaTeX. To make the document lighter, we only provide PDF version.

# The souce code
The core code is in the folder `code` for the exercise, with the source code and necessary auxauray dcouments.

To run the code successfully, you shoule frist run `app.py`. After that, you need to visit [127.0.0.1:8080](127.0.0.1:8080). If not successfully, please visit [127.0.0.1:8081](127.0.0.1:8081)


The file framework is as follows:

    -- REAMDME.md
    -- report.pdf
    -- codes
        -- html
        -- index
        -- static
            -- LOGO.png
        -- templates
            -- bio_form.html
            -- result.html
            -- show_bio.html
        -- app.py
        -- SearchFiles.py
        -- IndexFiles.py
        -- index.txt
        -- crawler_thread.py