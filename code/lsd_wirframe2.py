import math

import cv2
import numpy as np
import os
import json
import lsd_sap
from line_pretreat import pretreat


def compare(a1,a2,lst1,lst2):
    if abs(a1-a2)<0.1:
        if math.sqrt((lst1[0]-lst2[0])**2+(lst1[1]-lst2[1])**2)+math.sqrt((lst1[2]-lst2[2])**2+(lst1[3]-lst2[3])**2)<10:
            return True
    return False




def read_dir(dir):
    array = []
    for filename in os.listdir(dir):
        img = cv2.imread(dir+"/"+filename)
        array.append(img)
    return array

array=read_dir("D:\LineSegmentDatasets\LineSegmentDatasets\images\wireframe-test")
with open(r"D:\LineSegmentDatasets\LineSegmentDatasets\annotations\wireframe-test.json") as f2:
    test1 = json.load(f2)

precision=[]
recall=[]
cnt=0
sig=0.24
sap=15
ssap = 0
for n in range(len(array)):
    img = cv2.cvtColor(array[n], cv2.COLOR_BGR2GRAY)
    lsd = cv2.createLineSegmentDetector(2)
    dlines = lsd.detect(img)
    sortlines = []
    for j in range(len(dlines[3])):  # 3是NFA的值
        sortlines.append([dlines[3][j][0], dlines[0][j][0]])
    sortlines.sort(key=lambda x: x[0], reverse=True)
    lsdlst = []
    for j in range(int(len(sortlines) * sig)):
        lsdlst.append(sortlines[j][1])
    linelet = pretreat(lsdlst)
    lenlist = []

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

        else:
            angle_list.append(math.pi / 2)
            blist.append(w1)
            zlist.append(w1)

    orderlen = []
    for i in range(len(lenlist)):
        orderlen.append([i, lenlist[i]])
    orderlen.sort(key=lambda x: x[1], reverse=True)

    res1 = set()
    for i in range(len(orderlen) - 1):
        for j in range(i + 1, len(orderlen)):
            # if abs(angle_list[orderlen[i][0]]-angle_list[orderlen[j][0]])<0.1:
            A = 1 - abs(angle_list[orderlen[i][0]] - angle_list[orderlen[j][0]]) / (math.pi)
            C = 1 - math.sqrt((cwlist[orderlen[i][0]] - cwlist[orderlen[j][0]]) ** 2 + (
                    chlist[orderlen[i][0]] - chlist[orderlen[j][0]]) ** 2) / 0.5 / lenlist[orderlen[i][0]]
            # C=abs(cwlist[orderlen[i][0]]*cwlist[orderlen[j][0]]+chlist[orderlen[i][0]]*chlist[orderlen[j][0]])/(math.sqrt(cwlist[orderlen[i][0]]*cwlist[orderlen[i][0]]+chlist[orderlen[i][0]]*chlist[orderlen[i][0]])*math.sqrt(cwlist[orderlen[j][0]]*cwlist[orderlen[j][0]]+chlist[orderlen[j][0]]*chlist[orderlen[j][0]]))
            L = 1 - abs(lenlist[orderlen[i][0]] - lenlist[orderlen[j][0]]) / lenlist[orderlen[i][0]]

            if A * C * L > 0.9:
                res1.add(j)
    res = []
    for i in range(len(linelet)):
        if i not in res1:
            res.append(i)
    test = pretreat(test1[n]['lines'])
    sqlist_elder = []
    lenlist_elder = []
    anglelist_elder = []
    for i in range(len(test)):
        w1 = test[i][0]
        h1 = test[i][1]
        w2 = test[i][2]
        h2 = test[i][3]
        sqlist_elder.append(math.sqrt(w1 * w1 + h1 * h1 + w2 * w2 + h2 * h2))
        lenlist_elder.append(math.sqrt((w1 - w2) ** 2 + (h1 - h2) ** 2))
        if w1 == w2:
            anglelist_elder.append(math.pi / 2)
        else:
            k = (h1 - h2) / (w1 - w2)
            anglelist_elder.append(math.atan(k))
    tp=0
    used=[]
    for i in range(len(test)):
        for j in range(len(res)):
            if j not in used and math.sqrt((test[i][0] - linelet[res[j]][0]) ** 2 + (
                        test[i][1] - linelet[res[j]][1]) ** 2) +math.sqrt(
                    (test[i][2] - linelet[res[j]][2]) ** 2 + (test[i][3] - linelet[res[j]][3]) ** 2) <= sap:
                    tp += 1
                    used.append(j)
                    break
    fp = len(res) - tp
    fn = len(test) - tp
    r = tp / (tp + fn)
    p = tp / (tp + fp)
    recall.append(r)
    precision.append(p)
    '''for i in range(len(test)):
        for j in range(len(res)):
            if abs(anglelist_elder[i] - angle_list[res[j]]) < 0.1:
                if math.sqrt((test[i][0] - linelet[res[j]][0]) ** 2 + (
                        test[i][1] - linelet[res[j]][1]) ** 2) < 10 or math.sqrt(
                    (test[i][2] - linelet[res[j]][2]) ** 2 + (test[i][3] - linelet[res[j]][3]) ** 2) < 10:
                    tp += 1
                    break'''


    '''p = tp / (len(res))
    r = tp / (len(test))
    cnt += 1
    precision += p
    recall += r'''


'''print(precision/len(array))
print(recall/len(array))
print(2*(precision/len(array))*(recall/len(array))/((recall/len(array))+(precision/len(array))))'''




