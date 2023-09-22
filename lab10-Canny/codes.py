import numpy as np
import cv2
from matplotlib import pyplot as plt
import math

class Canny:
    img, Gause_img, gradient, theta = 0, 0, 0, 0
    dx, dy = 0, 0
    TH, TL = 0, 0
    _NMS = 0

    # 任务一:灰度读取
    def __init__(self, image_index):
        self.img = cv2.imread('dataset/{}.jpg'.format(str(image_index)), cv2.IMREAD_GRAYSCALE)

    # 任务二:高斯模糊
    def Guass_noise(self):
        Gause_img = cv2.GaussianBlur(self.img, (3, 3), 0)
        self.Gause_img = Gause_img

    # 任务三:灰一阶偏导的有限差分来计算梯度的幅值和方向
    def Guass_sobel_gradient(self):
        img_sobel_x = cv2.Sobel(self.Gause_img, cv2.CV_16S, 1, 0)
        img_sobel_y = cv2.Sobel(self.Gause_img, cv2.CV_16S, 0, 1)
        self.dx, self.dy = img_sobel_x, img_sobel_y
        theta = np.zeros(img_sobel_x.shape)
        gradient = np.zeros(img_sobel_x.shape)
        for i in range(img_sobel_x.shape[0]):
            for j in range(img_sobel_x.shape[1]):
                gradient[i][j] = math.sqrt((img_sobel_x[i][j]**2) +
                                           (img_sobel_y[i][j]**2))
                theta[i][j] = math.atan(img_sobel_y[i][j] / img_sobel_x[i][j])
        self.gradient = gradient
        # 这里按照Ppt要放,但是操作中我们不用，求反三角再求回去多少会引入误差)
        self.theta = theta

    # 任务四:对梯度幅值进行非极大值抑制
    def NMS(self):
        # 三个梯度
        dx, dy = self.dx, self.dy
        d = self.gradient
        width, height = d.shape
        # copy一个过来,但是不能直接做,会使得内存错误
        NMS = np.copy(d)
        for i in range(1, width - 1):
            for j in range(1, height - 1):
                # 如果当前梯度为0，该点就不是边缘点
                if d[i][j] == 0:
                    NMS[i][j] = 0
                else:
                    gradX = dx[i][j]  # 当前点 x 方向导数
                    gradY = dy[i][j]  # 当前点 y 方向导数
                    grad = d[i][j]  # 当前梯度点
                    # 如果 y 方向梯度值比较大，说明导数方向趋向于 y 分量
                    if abs(gradY) > abs(gradX):
                        weight = abs(gradX) / abs(gradY)
                        grad2 = d[i - 1][j]
                        grad4 = d[i + 1][j]
                        # 通过导数符号决定取得边界
                        if gradX * gradY > 0:
                            grad1 = d[i - 1][j - 1]
                            grad3 = d[i + 1][j + 1]
                        else:
                            grad1 = d[i - 1][j + 1]
                            grad3 = d[i + 1][j - 1]
                    # 如果 x 方向梯度值比较大
                    else:
                        weight = abs(gradY) / abs(gradX)
                        grad2 = d[i][j - 1]
                        grad4 = d[i][j + 1]
                        if gradX * gradY > 0:
                            grad1 = d[i + 1][j - 1]
                            grad3 = d[i - 1][j + 1]
                        else:
                            grad1 = d[i - 1][j - 1]
                            grad3 = d[i + 1][j + 1]
                    # 由ppt的公式进行插值运算
                    gradTemp1 = weight * grad1 + (1 - weight) * grad2
                    gradTemp2 = weight * grad3 + (1 - weight) * grad4
                    # 当前像素的梯度是局部的最大值，可能是边缘点，此时无需变动
                    if grad >= gradTemp1 and grad >= gradTemp2:
                        continue
                    else:
                        # 删掉~
                        NMS[i][j] = 0
        self._NMS = NMS

    # 任务五: 双阈值算法检测和连接边缘
    def double_threshold(self, Type='Sobel', th=0.4, tl=0.1):
        self.Guass_noise()
        if Type == 'Sobel':
            self.Guass_sobel_gradient()
        elif Type == "Roberts":
            self.Roberts()
        elif Type == 'Prewitt':
            self.Prewitt()
        else:
            self.Guass_sobel_gradient()
        self.NMS()
        NMS = self._NMS
        width, height = NMS.shape
        DT = np.zeros(NMS.shape)
        # 定义高低阈值
        TH = th * np.max(NMS)
        TL = tl * np.max(NMS)  #这里不能直接用max
        # 作为测试用
        self.TH = TH
        self.TL = TL
        
        for i in range(1, width - 1):
            for j in range(1, height - 1):
                # 双阈值选取
                if (NMS[i][j] < TL):
                    DT[i][j] = 0
                elif (NMS[i][j] > TH):
                    DT[i][j] = 1
            # 连接
                elif (NMS[i - 1][j - 1:j + 1] <TH).any() or NMS[i + 1][j - 1:
                    j + 1].any() or NMS[i][j - 1] < TH or NMS[i][j + 1] < TH:
                    DT[i][j] = 1
        return DT

    #给函数一个别名让结果更好看一点
    canny = double_threshold

    # 对比
    def comparison(self):
        return cv2.Canny(self.img, self.TH, self.TL)

    # 一些拓展（不同的算子）
    
    # Roberts算子
    def Roberts(self):
        kernelx = np.array([[-1, 0], [0, 1]], dtype=int)
        kernely = np.array([[0, -1], [1, 0]], dtype=int)
        x = cv2.filter2D(self.img, cv2.CV_16S, kernelx)
        y = cv2.filter2D(self.img, cv2.CV_16S, kernely)
        self.dx = x
        self.dy = y
        # 转转成uint8
        absX = cv2.convertScaleAbs(x)
        absY = cv2.convertScaleAbs(y)
        Roberts = cv2.addWeighted(absX, 0.5, absY, 0.5, 0)
        self.gradient = Roberts

    def Prewitt(self):
        # Prewitt算子
        kernelx = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]], dtype=int)
        kernely = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]], dtype=int)
        x = cv2.filter2D(self.img, cv2.CV_16S, kernelx)
        y = cv2.filter2D(self.img, cv2.CV_16S, kernely)
        self.dx = x
        self.dy = y
        # 转转成uint8
        absX = cv2.convertScaleAbs(x)
        absY = cv2.convertScaleAbs(y)
        Prewitt = cv2.addWeighted(absX, 0.5, absY, 0.5, 0)
        self.gradient = Prewitt

if __name__ == "__main__":
    for index in range(1, 4):
        print("正在进行图片{}".format(index))
        image = Canny(index)
        plt.imshow(image.canny())
        # plt.imshow(image.canny('Roberts'))
        plt.savefig("result/img{}.jpg".format(index)) 
        plt.cla()
        plt.imshow(image.comparison())
        plt.savefig("comparison/img{}.jpg".format(index))
        plt.cla()


