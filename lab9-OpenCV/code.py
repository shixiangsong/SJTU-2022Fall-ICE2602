import numpy as np
import cv2
from matplotlib import pyplot as plt
import math
import time


# 造一个轮子
def make_color_histogram(index):
    # 读取图片
    img = cv2.imread('images/img{}.jpg'.format(index),cv2.IMREAD_COLOR)
    blue, green, red = 0, 0, 0
    # 记录RGB数值
    for i in range(len(img)):
        for j in range(len(img[0])):
            blue  += img[i][j][0]
            green += img[i][j][1]
            red   += img[i][j][2]
    # 计算比例并保留两位小数
    Sum = sum((blue, green, red))
    color_list = [round(blue/ Sum,2), round(green/ Sum,2), round(red/ Sum,2)]
    x=['blue', 'green', 'red'] 
    y = color_list
    plt.bar(x,y,color=['blue','green','red'],alpha=0.8) #指定不同颜色并设置透明度
    plt.xlabel('color')
    plt.ylabel('ratio')
    plt.title('img{}\'s Color Histogram'.format(index))
    # 添加标签
    for a,b in zip(x, y):
        plt.text(a, b+.001, b, ha='center', va='bottom')
    plt.savefig("color-hist/img{}.jpg".format(index)) 
    plt.cla()#清除图像

def make_gray_histogram(index):
    img = cv2.imread('images/img{}.jpg'.format(index),cv2.IMREAD_GRAYSCALE) 
    ravel_img = img.ravel()
    #将灰度图转化为一维数组 并获取直方图
    plt.hist(ravel_img, 256, density=True)
    plt.title('img{}\'s Gray Histogram'.format(index))
    #显示直方图
    plt.savefig("gray-hist/img{}.jpg".format(index)) 
    plt.cla()

def make_gray_gradient(index):
    img = cv2.imread('images/img{}.jpg'.format(index),cv2.IMREAD_GRAYSCALE) 
    img_gradient = np.gradient(img)
    img_gra = np.zeros(img.shape)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            img_gra[i][j] = math.sqrt(pow(img_gradient[0][i][j],2) + pow(img_gradient[1][i][j],2))
    # for i in range(img.shape[0]):
    #     for j in range(img.shape[1]):
    #         if (i == 0):
    #             Ix = -img[i+1][j]
    #         elif (i == img.shape[0] - 1):
    #             Ix =  img[i-1][j]
    #         else:
    #             Ix =  int(img[i-1][j]) - int(img[i+1][j])
    #         if (j == 0):
    #             Iy = -img[i][j+1]
    #         elif (j == img.shape[1] - 1):
    #             Iy =  img[i][j-1]
    #         else:
    #             Iy =  int(img[i][j-1]) - int(img[i][j+1])
    #         img_gradient[i][j] = math.sqrt(Ix**2+Iy**2)
    plt.hist(img_gra.ravel(), 360 , density=True)
    plt.title('img{}\'s Gray Gradient Histogram'.format(index))
    #显示直方图
    plt.savefig("gradient/img{}.jpg".format(index)) 
    plt.cla()
zz
if __name__ == "__main__":
    for index in range(1,4):
        make_color_histogram(index)
        make_gray_histogram(index)
        make_gray_gradient(index)