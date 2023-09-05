import json
import cv2
from get_data_feature import simple_get_feature, get_feature_gray, get_gray_density
from init import read_dir, discard, compare, getf
from line_pretreat import pretreat


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
gray_len = get_gray_density(test,test_gray)
gradlist_test=gray_len[0]
lenlist_test=gray_len[1]
avegray=sum(gradlist_test)/len(gradlist_test)

with open(r"D:\LineSegmentDatasets\LineSegmentDatasets\annotations\linelet.json" )as f:
    annotations = json.load(f)

yorkurban=read_dir("D:\yorkurban")
with open(r"D:\LineSegmentDatasets\LineSegmentDatasets\annotations\elderlab.json" )as f3:
    elderlab = json.load(f3)

recall = 0
precision = 0
for n in range(len(yorkurban)):

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
    features = get_feature_gray(linelet,w,h,sobelxy_gray)
    lenlist = features[0]
    gradlist = features[7]
    sqlist = features[1]
    cwlist = features[2]
    chlist = features[3]
    angle_list = features[4]
    zlist = features[5]
    blist = features[6]

    d = {}
    lst=[]
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

    res1 = discard(orderlen,angle_list,lenlist,cwlist,chlist)
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
    elder_feature = simple_get_feature(elder)
    sqlist_elder = elder_feature[0]
    lenlist_elder = elder_feature[1]
    anglelist_elder = elder_feature[2]

    rp = compare(elder, anglelist_elder, res, angle_list, linelet)
    recall += rp[0]
    precision += rp[1]


ave_precision = precision/len(yorkurban)
ave_recall = recall/len(yorkurban)
F_1 = getf(ave_precision,ave_recall)