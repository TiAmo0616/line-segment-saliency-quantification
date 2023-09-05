import math

import cv2
import numpy as np
import os
import json
import line_pretreat
from init import read_dir, discard
from sap import ap, com


def line_score(array,test, t_slist,threshold):
    tplist,fplist,scores=[],[],[]
    n_gt=0
    for i in range(len(array)):
        dlines=array[i]

        tp = [0 for a in range(len(dlines))]
        fp = [0 for a in range(len(dlines))]
        score=[]
        used = []
        n_gt+=len(test[i]['lines'])
        for k in range(len(dlines)):
            score.append(t_slist[i][k])
            for j in range(len(test[i]['lines'])):
                temp = com(dlines[k], test[i]['lines'][j])
                if temp <= threshold and j not in used:
                    tp[k]=1
                    used.append(j)
                    break
            else:
                fp[k]=1

        scores.append(score)
        tplist.append(tp)
        fplist.append(fp)

    lcnn_tp = np.concatenate(tplist)
    lcnn_fp = np.concatenate(fplist)
    lcnn_scores = np.concatenate(scores)
    lcnn_index = np.argsort(-lcnn_scores)
    lcnn_tp = np.cumsum(lcnn_tp[lcnn_index]) / n_gt
    lcnn_fp = np.cumsum(lcnn_fp[lcnn_index]) / n_gt
    return ap(lcnn_tp, lcnn_fp)


def get_gray(img_Gray):
    test_gray = []
    sobelx_gray = cv2.Sobel(img_Gray, cv2.CV_64F, 1, 0, ksize=3)
    sobely_gray = cv2.Sobel(img_Gray, cv2.CV_64F, 0, 1, ksize=3)
    sobelx_gray = cv2.convertScaleAbs(sobelx_gray)
    sobely_gray = cv2.convertScaleAbs(sobely_gray)
    sobelxy_gray = cv2.addWeighted(sobelx_gray, 0.5, sobely_gray, 0.5, 0)
    test_gray.append(sobelxy_gray)
    return sobelxy_gray


array=read_dir("D:\LineSegmentDatasets\LineSegmentDatasets\images\wireframe-test")
with open(r"D:\LineSegmentDatasets\LineSegmentDatasets\annotations\wireframe-test.json") as f2:
    test = json.load(f2)
new_array=[]
t_slist=[]
for n in range(len(array)):
    img = cv2.cvtColor(array[n], cv2.COLOR_BGR2GRAY)
    lsd = cv2.createLineSegmentDetector(2)
    dlines = lsd.detect(img)

    linelet = []
    for i in range(len(dlines[0])):
        linelet.append(dlines[0][i][0])
    sobelxy_gray = get_gray(img)

    w = array[n].shape[1]
    h = array[n].shape[0]

    lenlist = []
    gradlist = []
    sqlist = []
    cwlist = []
    chlist = []
    angle_list = []
    zlist = []
    blist = []
    for i in range(len(linelet)):
        grad = 0
        cnt = 0
        w1 = (linelet[i][0])
        w2 = (linelet[i][2])
        h1 = (linelet[i][1])
        h2 = (linelet[i][3])
        lenlist.append(math.sqrt((w1 - w2) * (w1 - w2) + (h1 - h2) * (h1 - h2)))
        lenline = math.sqrt((w1 - w2) * (w1 - w2) + (h1 - h2) * (h1 - h2))
        sqlist.append(math.sqrt(w1 * w1 + w2 * w2 + h1 * h1 + h2 * h2))
        cwlist.append((w1 + w2) / 2)
        chlist.append((h1 + h2) / 2)

        if abs(w1 - w2) >= 1:
            k = (h2 - h1) / (w2 - w1)
            b = h2 - k * w2
            angle_list.append(math.atan(k))
            blist.append(h1 - k * w1)
            zlist.append(b / math.sqrt(k * k + 1))
            for j in range(int(w1), int(w2)):
                pre_h = int(k * j + b)
                if not (pre_h < 0 or pre_h >= h) and j < w:
                    grad += sobelxy_gray[pre_h][j]
                    cnt += 1

        else:
            angle_list.append(math.pi / 2)
            blist.append(w1)
            zlist.append(w1)
            for j in range(int(h1), int(h2)):
                grad += sobelxy_gray[j][int(w1)]
                cnt += 1
        if cnt != 0:

            gradlist.append(grad / cnt)
        else:
            gradlist.append(0)

    orderlen = []
    for i in range(len(lenlist)):
        orderlen.append([i, lenlist[i]])
    orderlen.sort(key=lambda x: x[1], reverse=True)

    res1 = discard(orderlen,angle_list,lenlist,cwlist,chlist)
    res = []
    sig = 0.5
    siglst = []
    for i in range(len(linelet)):
        if i not in res1:  #
            siglst.append([i, gradlist[i] * lenlist[i]])

    siglst.sort(key=lambda x: x[1], reverse=True)
    slist=[]
    for i in range(int(len(siglst) * sig)):
        res.append(linelet[siglst[i][0]])
        slist.append(siglst[i][1])
    new_array.append(res)
    t_slist.append(slist)

print(100*line_score(new_array,test,t_slist,15))

