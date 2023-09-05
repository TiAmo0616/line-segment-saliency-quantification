import math
import os
import cv2

from get_data_feature import simple_get_feature


def read_dir(dir):
    array=[]
    for filename in os.listdir(dir):
        img = cv2.imread(dir+"/"+filename)
        array.append(img)
    return array

def getf(p,r):
    return 2*p*r/(p+r)

def discard(orderlen,angle_list,lenlist,cwlist,chlist):
    res1 = set()
    for i in range(len(orderlen) - 1):
        for j in range(i + 1, len(orderlen)):
            # if abs(angle_list[orderlen[i][0]]-angle_list[orderlen[j][0]])<0.1:
            A = 1 - abs(angle_list[orderlen[i][0]] - angle_list[orderlen[j][0]]) / (math.pi)
            C = 1 - math.sqrt((cwlist[orderlen[i][0]] - cwlist[orderlen[j][0]]) ** 2 + (
                    chlist[orderlen[i][0]] - chlist[orderlen[j][0]]) ** 2) / 0.5 / lenlist[orderlen[i][0]]
            L = 1 - abs(lenlist[orderlen[i][0]] - lenlist[orderlen[j][0]]) / lenlist[orderlen[i][0]]

            if A * C * L > 0.9:
                res1.add(j)
    return res1



def compare(elder,anglelist_elder,res,angle_list,linelet):
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
        return [cnt / len(elder),cntr / (len(res))]

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

