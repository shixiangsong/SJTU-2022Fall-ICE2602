import numpy as np
import cv2
from matplotlib import pyplot as plt
import math
import time

# 向量的归一化
def normalize(v):
    v = np.array(v)
    return v/np.linalg.norm(v)

# 获取特征向量
def make_color_histogram(img):
    # 读取图片
    blue1, green1, red1 = 0, 0, 0
    blue2, green2, red2 = 0, 0, 0
    blue3, green3, red3 = 0, 0, 0
    blue4, green4, red4 = 0, 0, 0
    # 记录RGB数值
    for i in range(len(img)//2):
        for j in range(len(img[0])//2):
            blue1  += img[i][j][0]
            green1 += img[i][j][1]
            red1   += img[i][j][2]
        for j in range(len(img[0])//2,len(img[0])):
            blue2  += img[i][j][0]
            green2 += img[i][j][1]
            red2   += img[i][j][2]
    for i in range(len(img)//2,len(img)):
        for j in range(len(img[0])//2):
            blue3  += img[i][j][0]
            green3 += img[i][j][1]
            red3   += img[i][j][2]
        for j in range(len(img[0])//2,len(img[0])):
            blue4  += img[i][j][0]
            green4 += img[i][j][1]
            red4   += img[i][j][2]
    v1, v2, v3, v4,  = [blue1, red1, green1],[blue2, red2, green2],[blue3, red3, green3],[blue4, red4, green4]
    v1, v2, v3, v4 = normalize(v1), normalize(v2), normalize(v3), normalize(v4)
    v = np.concatenate((v1,v2,v3,v4))
    return v


def normalization(v):   
    v= v.copy()
    for i in range(12):
        if v[i] < 0.3:
            v[i] = 0
        elif v[i] < 0.6:
            v[i] = 1
        else:
            v[i] = 2
    return v

# 获得汉明码
def Hamming(v):
    ans = str()
    for i in v:
        if i == 0:
            ans += '00'
        elif i == 1:
            ans += '10'
        else:
            ans += '11'
    return ans

def g(p, index):
    ans = ''
    for i in index:
        ans += p[i]
    return ans

if __name__ == '__main__':
    
    dataset = list()
    vectors = list()
    returned = dict()
    #key = list(range(24))
    key = [1,7,17,23] #选中的Index要-1，如如果选中第2的数就要选[1]
    for i in range(1,41):
        img = cv2.imread('./Dataset/{}.jpg'.format(i))
        hists_vec = make_color_histogram(img)
        vectors.append(hists_vec)
        hists_vec = normalization(hists_vec)
        hamming = Hamming(hists_vec)
        index = g(hamming, key)
        dataset.append(index)
    target = cv2.imread("./target.jpg")
    hists_vec = make_color_histogram(target)
    histvec = normalization(hists_vec)
    hamming = Hamming(histvec)
    index = g(hamming, key)
    begin = time.time()
    print("The similar images are:")
    for i in range(0,40):
        #if dataset[i] == index:
        returned[i] = abs(np.dot(vectors[i], hists_vec))
        print(i+1)
    temp = 0
    for i in returned:
        if returned[i] > temp:
            temp = returned[i]
            index = i
    print("The most fit is {}".format(index+1))
    end = time.time()
    print(end-begin)