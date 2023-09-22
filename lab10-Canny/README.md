# Assignment 10 for SJTU EE208
> 521030910013 Shixiang Song

This assignment contains four parts: the sorce code, the assignment report, and the ```REAMDME``` document, and the source images as well as the generated images.

## The source code
The source code of this assignemnt is by Python. To run the assignemnt successfully, you have to install ```numpy``` and ```OpenCV``` advancedly. The install steps are:
```
pip install numpy
pip install opencv-python
pip install opencv-contrib-python
```

Additionally, we provide some ways for you to change the parameters freely. In the source code `codes.py` Line 164, we provide some parameters for testing. 

```
plt.imshow(image.canny(Type="The convolution core"->str, th->int, tl->int))
```

## The report
The report of this assignemnt is written by LaTeX. To make the document lighter, we only provide PDF version.

# The souce code
The source code is in `code.py`. **Please make sure that the PowerShell of the VSCode is under the *current directory!=* while running the source code!** Otherwise the error information would be:

```
[ WARN:0@0.585] global D:\a\opencv-python\opencv-python\opencv\modules\imgcodecs\src\loadsave.cpp (239) cv::findDecoder imread_('images/img1.jpg'): can't open/read file: check file path/integrity
```

The file framework is as follows:

    -- REAMDME.md
    -- report.pdf
    -- codes.py
    -- dataset 
        -- img1.jpg
        -- img2.jpg
        -- img3.jpg
    -- comparison
        -- img1.jpg
        -- img2.jpg
        -- img3.jpg
    -- result
        -- img1.jpg
        -- img2.jpg
        -- img3.jpg
    -- other-aux
        -- 0.5
        -- 0.4-0.2
        -- Roberts
        -- Prewitt
