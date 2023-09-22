import cv2
import math
import numpy as np
import math
import matplotlib.pyplot as plt
class MySIFT:
    def __init__(self, img) -> None:
        self.img = img
        self.gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        self.Feature = self.feature()
        self.guass()        
        self.M, self.T = self.calculte_gradient()

    # 高斯差金字塔
    def guassPyramid(self):
        src = self.img.copy()
        O = int(round((math.log(min(self.img.shape) / math.log(2)) - 1)))
        S = 4
        guass_lst = list()
        diff_lst = list()
        for i in range(O):
            layer = list()
            for j in range(S):
                sigma = 1.52 * (2**(i + j))
                layer.append(cv2.GaussianBlur((5, 5), sigma))
            guass_lst.append(layer)
            src = cv2.pyrDown(src)
        for i in guass_lst:
            layer = list()
            for j in range(S - 1):
                layer.append(guass_lst[i][j] - guass_lst[i][j + 1])
            diff_lst.append(layer)
        return diff_lst

    def imgPyramid(self):
        imglst = list()
        tp = (2.0, 1.5, 1.0, 0.75, 0.5)
        for i in tp:
            imglst.append(cv2.resize(self.img, self.img.size * i))
        return imglst


# 找极值点
# 后面那页ppt看不懂 放弃
# def findMaxPoint(self):
#     diffPyramid = self.guassPyramid()
#     ans = list()
#     for i in diffPyramid:
#         layer = i[1]
#         result = np.zeros(layer.shape)
#         for a in range(1, layer.shape[0] - 1):
#             for b in range(1, layer.shape[1] - 1):
#                 findmax = [
#                 diffPyramid[0][a - 1][b - 1], diffPyramid[0][a + 0][b - 1], diffPyramid[0][a + 1][b - 1],
#                 diffPyramid[0][a - 1][b + 0], diffPyramid[0][a + 0][b + 0], diffPyramid[0][a + 1][b + 0],
#                 diffPyramid[0][a - 1][b + 1], diffPyramid[0][a + 0][b + 1], diffPyramid[0][a + 1][b + 1],
#                 diffPyramid[1][a - 1][b - 1], diffPyramid[1][a + 0][b - 1], diffPyramid[1][a + 1][b - 1],
#                 diffPyramid[1][a - 1][b + 0], diffPyramid[1][a + 0][b + 0], diffPyramid[1][a + 1][b + 0],
#                 diffPyramid[1][a - 1][b + 1], diffPyramid[1][a + 0][b + 1], diffPyramid[1][a + 1][b + 1],
#                 diffPyramid[2][a - 1][b - 1], diffPyramid[2][a + 0][b - 1], diffPyramid[2][a + 1][b - 1],
#                 diffPyramid[2][a - 1][b + 0], diffPyramid[2][a + 0][b + 0], diffPyramid[2][a + 1][b + 0],
#                 diffPyramid[2][a - 1][b + 1], diffPyramid[2][a + 0][b + 1], diffPyramid[2][a + 1][b + 1]]
#                 if max(findmax) == layer[a][b]:
#                     result[a][b] = 1
#         ans.append(result)
#     return ans

    def feature(self):
        gray = self.gray.copy()
        # gray = cv2.cvtColor(i, cv2.COLOR_BGR2GRAY)
        gray = np.float32(gray)
        dst = cv2.cornerHarris(gray, 2, 3, 0.245)
        dst = cv2.dilate(dst, None)
        # self.img[dst > 0.01 * dst.max()] = [0, 0, 255]
        feature = list()
        feature += [dst > 0.01 * dst.max()]
        return np.array(feature[0])

    # 高斯模糊预处理
    def guass(self):
        self.gray = cv2.GaussianBlur(self.gray, (5, 5), 1.6)

    # 计算梯度幅值和梯度方向
    def calculte_gradient(self):
        M = np.zeros(self.gray.shape)
        T = np.zeros(self.gray.shape)
        theta_lst = list()
        for i in range(1, self.gray.shape[0] - 1):
            for j in range(1, self.gray.shape[1] - 1):
                theta = math.atan2(int(self.gray[i][j + 1]) - int(self.gray[i][j - 1]),
                                   int(self.gray[i + 1][j]) - int(self.gray[i - 1][j]))
                if theta < 0:
                    theta = 2 * math.pi + theta
                theta = int(theta * 360 / (2 * math.pi))
                theta_lst.append(theta)
                m = math.sqrt((int(self.gray[i][j + 1]) - int(self.gray[i][j - 1]))**2 +
                              (int(self.gray[i + 1][j]) - int(self.gray[i - 1][j]))**2)
                T[i][j] = theta
                M[i][j] = m
        return (M, T) 

    # 计算每一个关键点的梯度方向
    def calculate_direction(self):
        M, T = self.M, self.T
        feature = self.Feature
        directions = np.zeros(feature.shape)
        # print(feature.shape)
        for i in range(self.gray.shape[0]):
            for j in range(self.gray.shape[1]):
                if feature[i][j]:
                    weight_lst = [0] * 36
                    r = 3 * 1.5 * 1.6  #按照论文建议σ取1.6 r=7.2
                    # 以下是求极值点
                    minx = i - 7 if i - 7 > 0 else 0
                    maxx = i + 7 if i + 7 < self.gray.shape[
                        0] else self.gray.shape[0]
                    miny = j - 7 if j - 7 > 0 else 0
                    maxy = j + 7 if j + 7 < self.gray.shape[
                        1] else self.gray.shape[1]
                    for p in range(minx, maxx):
                        for q in range(miny, maxy):
                            distance = math.sqrt((p - i)**2 + (q - j)**2)
                            if (distance < r):
                                weight_lst[int(T[p, q]) // 10] += M[p, q] /(1+distance)
                    dirpoint = max(weight_lst)
                    direct = 0
                    # subdir = list() #辅助方向
                    for k in range(36):
                        if k == dirpoint:
                            direct = k * 10
                        # if k > 0.8 * dirpoint:
                        #     subdir += [k * 10]
                    directions[i, j] = direct
                    # if subdir:
                    #     subdirs[(i, j)] = subdir
        return directions

    # 计算特质值
    def sift_feature(self):
        features = dict()
        feature = self.Feature
        M, T = self.M, self.T
        directions = self.calculate_direction()
        for i in range(self.gray.shape[0]):
            for j in range(self.gray.shape[1]):
                theta_block = np.zeros((16, 16))
                m_block = np.zeros((16, 16))
                if feature[i, j]:
                    for p in range(0, 16):
                        for q in range(0, 16):
                            x = int(i + (p - 8) * math.cos(directions[i, j] /
                                                           360 * 2 * math.pi))
                            y = int(j + (q - 8) * math.cos(directions[i, j] /
                                                           360 * 2 * math.pi))
                            try:
                                m_block[p, q] = M[x, y]
                                theta_block[p, q] = T[x, y] - directions[i, j]
                                if theta_block[p, q] < 0:
                                    theta_block[p, q] += 360
                            except:
                                continue
                    # 生成特征向量
                    ans = [[[0]*8]*4]*4
                    for p in range(0,16):
                        for q in range(0,16):
                            ans[p//4][q//4][int(theta_block[p][q])//45] += m_block[p][q]
                    #ans = (ans-np.min(ans))/(np.max(ans)-np.min(ans))  
                    features[(i,j)] = np.array(ans)
                    
        return features

    def comparison(self, another):
        shown = self.show(another)
        #print(shown.shape)
        features1 = self.sift_feature()
        features2 = another.sift_feature()
        img1 = self.img
        img2 = another.img
        #print(len(features1))
        feat1 = list(features1.items())
        feat2 = list(features2.items())
        dises = dict()
        for index1, feature1 in feat1:
            try:
                points = list()
                indeices = list()
                for index2, feature2 in feat2:
                    point = feature2 - feature1
                    distance = np.linalg.norm(point)
                    points.append(distance)
                    indeices.append(index2)
                distance = min(points)
                index2 = indeices[points.index(distance)]
                for i in feat2:
                    if i[0] == index2:
                        feat2.remove(i)
                        break
                shown[index1] = (255,0,0)
                shown[index2[0], index2[1] + self.img.shape[1]] = (255, 0, 0)
                dises[(index1,index2)] = distance
            except:
                break
                # print(index1,index2)
        #print(match)
        match = list(dises.items())
        good_match = list()
        for i in range(len(match) - 1):
            if match[i][1] < 0.75*match[i+1][1]:
                good_match.append(match[i][0])
        print("There are {} matches!".format(len(good_match)))
        return (good_match, list(features1.keys()), list(features2.keys()))

    def show(self, another):
        image = self.img
        transformed_image = another.img
      #  print(image.shape)
        #print(transformed_image.shape)
        h0,w0=image.shape[0],image.shape[1]  #cv2 读取出来的是h,w,c
        h1,w1=transformed_image.shape[0],transformed_image.shape[1]
        h=max(h0,h1)
        w=max(w0,w1)
        org_image=np.ones((h,w,3),dtype=np.uint8)*255
        trans_image=np.ones((h,w,3),dtype=np.uint8)*255

        org_image[:h0,:w0,:]=image[:,:,:]
        trans_image[:h1,:w1,:]=transformed_image[:,:,:]
        all_image = np.hstack((org_image[:,:w0,:], trans_image[:,:w1,:]))
        return all_image

if __name__ == '__main__':
    good_points = list()
    length = list()
    box_in_sence = cv2.imread("./dataset/target.jpg")
    for i in range(1,6):
        print("This is image {}!".format(i))
        box = cv2.imread("./dataset/{}.jpg".format(i))
        test = MySIFT(box)
        test2 = MySIFT(box_in_sence)
        test.feature()
        lst = test.comparison(test2)
        good_points.append(lst)
        length.append(len(lst[0]))
    
    index = length.index(max(length))
    box = cv2.imread("./dataset/{}.jpg".format(index + 1))
    test = MySIFT(box)
    img = np.array(test.show(test2))
    cv_kpts1 = good_points[index][1]
    #cv_kpts1 = [cv2.KeyPoint(int(cv_kpts1[i][0]), int(cv_kpts1[i][1]), 1)
        # for i in range(len(cv_kpts1))]
    cv_kpts2 = good_points[index][2]
    #cv_kpts2 = [cv2.KeyPoint(int(cv_kpts2[i][0]), int(cv_kpts2[i][1]), 1)
         #for i in range(len(cv_kpts2))]
    for i in good_points[:10][index][0]:
        img[i[0][0]][i[0][1]] = (0,0,255)
        img[i[1][0]][box.shape[1]+i[1][1]] = (0,0,255)
        cv2.line(img,(i[0][1],i[0][0]),(box.shape[1]+i[1][1],i[1][0]),(0,0,255))
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    plt.imshow(img)
    plt.savefig('result.png')
        # sift = cv2.xfeatures2d.SIFT_create()

    # # 特征点提取与描述子生成
    # kp1, des1 = sift.detectAndCompute(box, None)
    # kp2, des2 = sift.detectAndCompute(box_in_sence, None)

    # # 暴力匹配
    # bf = cv2.DescriptorMatcher_create(cv2.DescriptorMatcher_BRUTEFORCE)
    # matches = bf.knnMatch(des1, des2, k=2)

    # 绘制最佳匹配

    # ratio1 = 0.75
    # good = []
    # for m, n in matches :
    #     if m.distance < .75* n.distance:
    #         good.append([m])
    #         print(m.distance)

    # result = cv2.drawMatchesKnn(box, kp1, box_in_sence, kp2, good[:120], None, flags=2)

    # cv2.imshow('s',result)
    # cv2.waitKey(0)
