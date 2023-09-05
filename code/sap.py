import math

import numpy as np


def ap(tp,fp):
    recall = tp
    precision = tp / np.maximum(tp + fp, 1e-9)

    recall = np.concatenate(([0.0], recall, [1.0]))
    precision = np.concatenate(([0.0], precision, [0.0]))

    for i in range(precision.size - 1, 0, -1):
        precision[i - 1] = max(precision[i - 1], precision[i])
    i = np.where(recall[1:] != recall[:-1])[0]
    return np.sum((recall[i + 1] - recall[i]) * precision[i + 1])

def com(lst1,lst2):
    return math.sqrt((lst1[0] - lst2[0]) ** 2 + (lst1[1] - lst2[1]) ** 2) + math.sqrt(
        (lst1[2] - lst2[2]) ** 2 + (lst1[3] - lst2[3]) ** 2)

def get_angle(lst):
    w1=lst[0]
    h1=lst[1]
    w2=lst[2]
    h2=lst[3]
    if w1 != w2:
        k = (h2 - h1) / (w2 - w1)
        return math.atan(k)
    else:
        return math.pi/2