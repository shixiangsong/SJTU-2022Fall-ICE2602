import extract_feature
import os
import numpy as np
import torch
import torchvision
import torchvision.transforms as transforms
from torchvision.datasets.folder import default_loader

resnet50 = list()

# Train
for i in range(1, 101):
    test_image = default_loader('./data/ ({}).bmp'.format(i))
    resnet50.append(extract_feature.main(test_image))


def comparison(img1, img2):
    sim = np.sum(img1 * img2) / (np.linalg.norm(img1) * np.linalg.norm(img2))
    return sim


for i in range(1, 11):
    print("Test {}!".format(i))
    test_image = default_loader('./test/ ({}).bmp'.format(i))
    out = extract_feature.main(test_image)
    compare = list()
    for j in range(100):
        compare.append(comparison(out, resnet50[j]))
    sort = sorted(compare)
    print(
        "The five most fitted images are:\n{} Score:{}\n{} Score:{}\n{} Score:{}\n{} Score:{}\n{} Score:{}"
        .format(
            compare.index(sort[-1]) + 1, sort[-1],
            compare.index(sort[-2]) + 1, sort[-2],
            compare.index(sort[-3]) + 1, sort[-3],
            compare.index(sort[-4]) + 1, sort[-4],
            compare.index(sort[-5]) + 1, sort[-5]))
