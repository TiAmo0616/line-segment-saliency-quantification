import json
from pathlib import Path
from PIL import Image, ImageDraw
import cv2
import os
import math


def read_dir(dir):
    array=[]
    for filename in os.listdir(dir):
        img = cv2.imread(dir+"/"+filename)
        array.append(img)
    return array

def pretreat(annotations):  # w1是小的
    res = []
    for i in range(len(annotations)):
        if annotations[i][0] < 0:
            annotations[i][0] = 0
        if annotations[i][1] < 0:
            annotations[i][1] = 0
        if annotations[i][2] < 0:
            annotations[i][2] = 0
        if annotations[i][3] < 0:
            annotations[i][3] = 0

        if annotations[i][0] > annotations[i][2]:
            w1 = annotations[i][2]
            w2 = annotations[i][0]
            h1 = annotations[i][3]
            h2 = annotations[i][1]
        elif annotations[i][0] == annotations[i][2]:
            if annotations[i][1] > annotations[i][3]:
                w1 = annotations[i][2]
                w2 = annotations[i][0]
                h1 = annotations[i][3]
                h2 = annotations[i][1]
            else:
                w2 = annotations[i][2]
                w1 = annotations[i][0]
                h2 = annotations[i][3]
                h1 = annotations[i][1]
        else:
            w2 = annotations[i][2]
            w1 = annotations[i][0]
            h2 = annotations[i][3]
            h1 = annotations[i][1]
        res.append([w1, h1, w2, h2])
    return res


def splice(lst, angle_list, gradlist, lenlist, zlist, cwlist, chlist, blist, sqlist, d):  # 直线拼接
    res = []
    for i in range(len(lst)):
        for j in range(len(lst)):
            if i != j:
                if abs(angle_list[i] - angle_list[j]) < 0.01 and abs(gradlist[i] - gradlist[j]) < 10 and abs(
                        blist[i] - blist[j]) < 10:
                    # if abs(angle_list[i]-angle_list[j])<0.01 and abs(gradlist[i]-gradlist[j])<10 and abs(zlist[i]-zlist[j])<8:
                    if (abs(lst[i][0] - lst[j][2]) < 20 and abs(lst[i][1] - lst[j][3]) < 20):
                        w1 = lst[j][0]
                        h1 = lst[j][1]
                        w2 = lst[i][2]
                        h2 = lst[i][3]
                        cw = (w1 + w2) / 2
                        ch = (h1 + h2) / 2
                        if w1 == w2:
                            angle_list.append(math.pi / 2)
                            zlist.append(w1)
                            blist.append(w1)
                        else:
                            angle_list.append(math.atan((h1 - h2) / (w1 - w2)))
                            zlist.append(b / math.sqrt(k * k + 1))
                            blist.append(h1 - (h1 - h2) / (w1 - w2) * w1)

                        lst.append([w1, h1, w2, h2])
                        sqlist.append(math.sqrt(w1 * w1 + w2 * w2 + h1 * h1 + h2 * h2))
                        gradlist.append((gradlist[i] + gradlist[j]) / 2)
                        lenlist.append(math.sqrt((w1 - w2) ** 2 + (h1 - h2) ** 2))
                        cwlist.append((w1 + w2) / 2)
                        chlist.append((h1 + h2) / 2)
                        res.append(j)
                        res.append(i)
                        index = len(lst) - 1
                        d[index] = [i, j]
                        if i in d:
                            d[index] += d[i]
                        if j in d:
                            d[index] += d[j]
                    if (abs(lst[i][2] - lst[j][0]) < 20 and abs(lst[i][3] - lst[j][1]) < 20):
                        w1 = lst[i][0]
                        h1 = lst[i][1]
                        w2 = lst[j][2]
                        h2 = lst[j][3]
                        cw = (w1 + w2) / 2
                        ch = (h1 + h2) / 2
                        if w1 == w2:
                            angle_list.append(math.pi / 2)
                            zlist.append(w1)
                            blist.append(w1)
                        else:
                            angle_list.append(math.atan((h1 - h2) / (w1 - w2)))
                            zlist.append(b / math.sqrt(k * k + 1))
                            blist.append(h1 - (h1 - h2) / (w1 - w2) * w1)
                        lst.append([w1, h1, w2, h2])
                        gradlist.append((gradlist[i] + gradlist[j]) / 2)
                        lenlist.append(math.sqrt((w1 - w2) ** 2 + (h1 - h2) ** 2))
                        cwlist.append((w1 + w2) / 2)
                        chlist.append((h1 + h2) / 2)
                        sqlist.append(math.sqrt(w1 * w1 + w2 * w2 + h1 * h1 + h2 * h2))
                        res.append(j)
                        res.append(i)
                        index = len(lst) - 1
                        d[index] = [i, j]
                        if i in d:
                            d[index] += d[i]
                        if j in d:
                            d[index] += d[j]
    return res

def get_testgray(array):
    test_gray=[]
    for i in range(len(array)):
        img_Gray = cv2.cvtColor(array[i], cv2.COLOR_BGR2GRAY)
        sobelx_gray=cv2.Sobel(img_Gray,cv2.CV_64F,1,0,ksize=3)
        sobely_gray=cv2.Sobel(img_Gray,cv2.CV_64F,0,1,ksize=3)
        sobelx_gray=cv2.convertScaleAbs(sobelx_gray)
        sobely_gray=cv2.convertScaleAbs(sobely_gray)
        sobelxy_gray=cv2.addWeighted(sobelx_gray,0.5,sobely_gray,0.5,0)
        test_gray.append(sobelxy_gray)
    return test_gray

datasets = [
    ["wireframe-test/", "wireframe-test.json"],
    ["yorkurban/", "linelet.json"],
    ["yorkurban/", "elderlab.json"]
]

with open(r"D:\LineSegmentDatasets\LineSegmentDatasets\annotations\wireframe-test.json") as f2:
    test = json.load(f2)

array=read_dir("D:\LineSegmentDatasets\LineSegmentDatasets\images\wireframe-test")

test_gray=get_testgray(array)
gradlist_test=[]
lenlist_test=[]
for a in range(len(test_gray)):
    w=test_gray[a].shape[1]
    h=test_gray[a].shape[0]
    testline=pretreat(test[a]['lines'])
    for i in range(len(testline)):
        grad=0
        cnt=0
        w1=testline[i][0]
        w2=testline[i][2]
        h1=testline[i][1]
        h2=testline[i][3]
        lenlist_test.append(math.sqrt((w1-w2)*(w1-w2)+(h1-h2)*(h1-h2)))

        if  w1 != w2:
            k=(h2-h1)/(w2-w1)
            b = h2-k*w2
            for j in range(int(w1),int(w2)):
                if j >= w:
                    j = w-1
                pre_h=int(k*j+b)
                if not(pre_h > h-1 or pre_h<0):
                    grad+=test_gray[a][pre_h][j]
                    cnt+=1

        else:
            if w1>=w:
                w1=w-1
            for j in range(int(h1),int(h2)):
                if j<h:
                    grad+=test_gray[a][j][int(w1)]
                    cnt+=1
        if cnt != 0:
            gradlist_test.append(grad/cnt)
        else:
            gradlist_test.append(0)

avegray=sum(gradlist_test)/len(gradlist_test)


with open(r"D:\LineSegmentDatasets\LineSegmentDatasets\annotations\linelet.json" )as f:
    annotations = json.load(f)

yorkurban=read_dir("D:\yorkurban")
with open(r"D:\LineSegmentDatasets\LineSegmentDatasets\annotations\elderlab.json" )as f3:
    elderlab = json.load(f3)

recall = 0
pre = 0
for n in range(102):

    img_Gray = cv2.cvtColor(yorkurban[n], cv2.COLOR_BGR2GRAY)
    sobelx_gray = cv2.Sobel(img_Gray, cv2.CV_64F, 1, 0, ksize=3)
    sobely_gray = cv2.Sobel(img_Gray, cv2.CV_64F, 0, 1, ksize=3)
    sobelx_gray = cv2.convertScaleAbs(sobelx_gray)
    sobely_gray = cv2.convertScaleAbs(sobely_gray)
    sobelxy_gray = cv2.addWeighted(sobelx_gray, 0.5, sobely_gray, 0.5, 0)
    test_gray.append(sobelxy_gray)

    w = yorkurban[n].shape[1]
    h = yorkurban[n].shape[0]

    linelet = pretreat(annotations[n]['lines'])

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

    d = {}
    lst=[]
    #lst = splice(linelet, angle_list, gradlist, lenlist, zlist, cwlist, chlist, blist, sqlist, d)
    orderlen = []
    for ii in range(len(lenlist)):
        orderlen.append([ii, lenlist[ii]])
    orderlen.sort(key=lambda x: x[1], reverse=True)
    sumlen = 0
    cnt1 = 0
    for i5 in range(len(lenlist)):
        if i5 not in lst:
            sumlen += lenlist[i5]
            cnt1 += 1
    avelen = sumlen / cnt1

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

    '''res2 = set()
    for iii in range(len(orderlen) - 1):
        if orderlen[iii][0] not in lst:
            for j in range(iii + 1, len(orderlen)):
                if orderlen[j][0] not in lst:
                    if abs(angle_list[orderlen[iii][0]] - angle_list[orderlen[j][0]]) < 0.1:
                        if math.sqrt((linelet[orderlen[iii][0]][0] - linelet[orderlen[j][0]][0]) ** 2 + (
                                linelet[orderlen[iii][0]][1] - linelet[orderlen[j][0]][1]) ** 2) < 6 or math.sqrt(
                                (linelet[orderlen[iii][0]][2] - linelet[orderlen[j][0]][2]) ** 2 + (
                                        linelet[orderlen[iii][0]][3] - linelet[orderlen[j][0]][3]) ** 2) < 6:
                            res2.add(orderlen[j][0])
                        if math.sqrt((cwlist[orderlen[iii][0]] - cwlist[orderlen[j][0]]) ** 2 + (
                                chlist[orderlen[iii][0]] - chlist[orderlen[j][0]]) ** 2) < 6:
                            res2.add(orderlen[j][0])'''

    cnt2 = 0
    res = []
    sig=0.9
    siglst = []
    for i in range(len(linelet)):
        if i not in res1 and i not in lst:#
            siglst.append([i, gradlist[i] * lenlist[i]])

    siglst.sort(key=lambda x: x[1], reverse=True)
    for i in range(int(len(siglst) * sig)):
        res.append(siglst[i][0])

    elder = pretreat(elderlab[n]['lines'])
    sqlist_elder = []
    lenlist_elder = []
    anglelist_elder = []
    for i in range(len(elder)):
        w1 = elder[i][0]
        h1 = elder[i][1]
        w2 = elder[i][2]
        h2 = elder[i][3]
        sqlist_elder.append(math.sqrt(w1 * w1 + h1 * h1 + w2 * w2 + h2 * h2))
        lenlist_elder.append(math.sqrt((w1 - w2) ** 2 + (h1 - h2) ** 2))
        if abs(w1 - w2) < 1:
            anglelist_elder.append(math.pi / 2)
        else:
            k = (h1 - h2) / (w1 - w2)
            anglelist_elder.append(math.atan(k))

    cnt = 0

    for i in range(len(elder)):
        for j in range(len(res)):
            if abs(anglelist_elder[i] - angle_list[res[j]]) < 0.1:
                if math.sqrt((elder[i][0] - linelet[res[j]][0]) ** 2 + (
                        elder[i][1] - linelet[res[j]][1]) ** 2) < 10 or math.sqrt(
                        (elder[i][2] - linelet[res[j]][2]) ** 2 + (elder[i][3] - linelet[res[j]][3]) ** 2) < 10:
                    cnt += 1
                    break
    cntr = 0
    for j in range(len(res)):
        for i in range(len(elder)):
            if abs(anglelist_elder[i] - angle_list[res[j]]) < 0.1:
                if math.sqrt((elder[i][0] - linelet[res[j]][0]) ** 2 + (
                        elder[i][1] - linelet[res[j]][1]) ** 2) < 10 or math.sqrt(
                        (elder[i][2] - linelet[res[j]][2]) ** 2 + (elder[i][3] - linelet[res[j]][3]) ** 2) < 10:
                    cntr += 1
                    break
    if len(res) > 0:
        recall += cnt / len(elder)
        pre += cntr / (len(res))

def getf(p,r):
    return 2*p*r/(p+r)
print(pre/102)
print(recall/102)
print(getf(pre/102,recall/102))