import json
import cv2
from get_data_feature import get_data_feature, simple_get_feature
from init import read_dir, getf, discard, compare
from line_pretreat import pretreat


sig=0.21
recall=0
precision=0
yorkurban=read_dir("D:\yorkurban")
with open(r"D:\LineSegmentDatasets\LineSegmentDatasets\annotations\elderlab.json" )as f3:
    elderlab = json.load(f3)

for n in range(len(yorkurban)):
    img0=yorkurban[n]
    img = cv2.cvtColor(img0, cv2.COLOR_BGR2GRAY)
    lsd = cv2.createLineSegmentDetector(2)
    dlines = lsd.detect(img)
    sortlines=[]
    for j in range(len(dlines[3])):
        sortlines.append([dlines[3][j][0],dlines[0][j][0]])
    sortlines.sort(key=lambda x:x[0],reverse=True)
    lsdlst=[]
    for j in range(int(len(sortlines)*sig)):
        lsdlst.append(sortlines[j][1])
    linelet=pretreat(lsdlst)
    features = get_data_feature(linelet)
    lenlist = features[0]
    sqlist = features[1]
    cwlist = features[2]
    chlist = features[3]
    angle_list = features[4]
    blist = features[5]
    zlist = features[6]

    orderlen = []
    for i in range(len(lenlist)):
        orderlen.append([i, lenlist[i]])
    orderlen.sort(key=lambda x: x[1], reverse=True)

    res1 = discard(orderlen,angle_list,lenlist,cwlist,chlist)
    res=[]
    for i in range(len(linelet)):
        if i not in res1:
            res.append(i)
    elder = pretreat(elderlab[n]['lines'])
    elder_feature = simple_get_feature(elder)
    sqlist_elder = elder_feature[0]
    lenlist_elder = elder_feature[1]
    anglelist_elder = elder_feature[2]

    rp = compare(elder,anglelist_elder,res,angle_list,linelet)
    recall +=rp[0]
    precision+=rp[1]



ave_precision = precision/len(yorkurban)
ave_recall = recall/len(yorkurban)
F_1 = getf(ave_precision,ave_recall)


