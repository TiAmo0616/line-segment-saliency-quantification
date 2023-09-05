import json
from PIL import Image, ImageDraw
import cv2
import os
import math
from line_pretreat import pretreat

def read_dir(dir):
    array = []
    for filename in os.listdir(dir):
        img = cv2.imread(dir+"/"+filename)
        array.append(img)
    return array

datasets = [
    ["wireframe-test/", "wireframe-test.json"],
    ["yorkurban/", "linelet.json"],
    ["yorkurban/", "elderlab.json"]
]

with open(r"D:\LineSegmentDatasets\LineSegmentDatasets\annotations\wireframe-test.json") as f2:
    test = json.load(f2)

array=read_dir("D:\LineSegmentDatasets\LineSegmentDatasets\images\wireframe-test")

test_gray=[]
for i in range(len(array)):
    img_Gray = cv2.cvtColor(array[i], cv2.COLOR_BGR2GRAY)
    sobelx_gray=cv2.Sobel(img_Gray,cv2.CV_64F,1,0,ksize=3)
    sobely_gray=cv2.Sobel(img_Gray,cv2.CV_64F,0,1,ksize=3)
    sobelx_gray=cv2.convertScaleAbs(sobelx_gray)
    sobely_gray=cv2.convertScaleAbs(sobely_gray)
    sobelxy_gray=cv2.addWeighted(sobelx_gray,0.5,sobely_gray,0.5,0)
    test_gray.append(sobelxy_gray)

gradlist_test=[]
lenlist_test=[]
for a in range(len(test_gray)):
    w=test_gray[a].shape[1]
    h=test_gray[a].shape[0]
    for i in range(len(test[a]['lines'])):
        grad=0
        cnt=0
        w1=int(test[a]['lines'][i][0])
        w2=int(test[a]['lines'][i][2])
        h1=int(test[a]['lines'][i][1])
        h2=int(test[a]['lines'][i][3])
        lenlist_test.append(math.sqrt((w1-w2)*(w1-w2)+(h1-h2)*(h1-h2)))

        if  w1 != w2:
            k=(h2-h1)/(w2-w1)
            b = h2-k*w2
            if w1 > w2:
                temp = w1
                w1 = w2
                w2 = temp
            for j in range(w1,w2):
                if j >= w:
                    j = w-1
                pre_h=int(k*j+b)
                if pre_h > h-1:
                    pre_h = h-1
                grad+=test_gray[a][pre_h][j]
                cnt+=1

        else:
            if w1>=w:
                w1=w-1
            if h1 > h2:
                temp = h1
                h1 = h2
                h2 = temp
            for j in range(h1,h2):
                if j>=h:
                    j=h-1
                grad+=test_gray[a][j][w1]
                cnt+=1

        gradlist_test.append(grad/cnt)

avegray=sum(gradlist_test)/len(gradlist_test)

with open(r"D:\LineSegmentDatasets\LineSegmentDatasets\annotations\linelet.json" )as f:
    annotations = json.load(f)

src=cv2.imread("D:\LineSegmentDatasets\LineSegmentDatasets\images\yorkurban\P1020177.jpg")###
imgGray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
sobelx_gray=cv2.Sobel(imgGray,cv2.CV_64F,1,0,ksize=3)
sobely_gray=cv2.Sobel(imgGray,cv2.CV_64F,0,1,ksize=3)
sobelx_gray=cv2.convertScaleAbs(sobelx_gray)
sobely_gray=cv2.convertScaleAbs(sobely_gray)
sobelxy_gray=cv2.addWeighted(sobelx_gray,0.5,sobely_gray,0.5,0)

linelet=pretreat(annotations[1]['lines'])##
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

    if w1 != w2:
        k = (h2 - h1) / (w2 - w1)
        b = h2 - k * w2
        angle_list.append(math.atan(k))
        blist.append(h1 - k * w1)
        zlist.append(b / math.sqrt(k * k + 1))
        for j in range(int(w1), int(w2)):
            pre_h = int(k * j + b)
            if pre_h > 479:
                pre_h = 479
            if pre_h < 0:
                pre_h = 0
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

lst=[]
#lst=splice(linelet,angle_list,gradlist,lenlist,zlist,cwlist,chlist,blist,sqlist)

orderlen=[]
for i in range(len(lenlist)):
    orderlen.append([i,lenlist[i]])
orderlen.sort(key=lambda x :x[1],reverse=True)

sumlen=0
cnt=0
for i in range(len(lenlist)):
    if i not in lst:
        sumlen+=lenlist[i]
        cnt+=1
avelen=sumlen/cnt

res2=set()
for i in range(len(orderlen)-1):
    if orderlen[i][0] not in lst:
        for j in range(i+1,len(orderlen)):
            if orderlen[j][0] not in lst:
                if abs(angle_list[orderlen[i][0]]-angle_list[orderlen[j][0]])<0.1:
                    if math.sqrt((linelet[orderlen[i][0]][0]-linelet[orderlen[j][0]][0])**2+(linelet[orderlen[i][0]][1]-linelet[orderlen[j][0]][1])**2)<10 or math.sqrt((linelet[orderlen[i][0]][2]-linelet[orderlen[j][0]][2])**2+(linelet[orderlen[i][0]][3]-linelet[orderlen[j][0]][3])**2)<10:
                        res2.add(orderlen[j][0])
                    if math.sqrt((cwlist[orderlen[i][0]]-cwlist[orderlen[j][0]])**2+(chlist[orderlen[i][0]]-chlist[orderlen[j][0]])**2)<10:
                        res2.add(orderlen[j][0])

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

siglst = []
res=[]
for i in range(len(linelet)):
    if i not in res1 and i not in lst:#
        siglst.append([i, gradlist[i] * lenlist[i]])

siglst.sort(key=lambda x: x[1], reverse=True)
for i in range(int(len(siglst) * 0.4)):
    res.append(siglst[i][0])

image = Image.open("D:\LineSegmentDatasets\LineSegmentDatasets\images\yorkurban\P1020177.jpg")
draw = ImageDraw.Draw(image)
cnt = 0
for i in res:
        #cnt += 1
        draw.line(linelet[i], fill=(255, 165, 0),width=3)
        draw.line((linelet[i][0], linelet[i][1], linelet[i][0] + 0.5, linelet[i][1] + 0.5), (0, 255, 0), width=3)
        draw.line((linelet[i][2], linelet[i][3], linelet[i][2] + 0.5, linelet[i][3] + 0.5), (0, 255, 0), width=3)

image.show()

'''image = Image.open("D:\LineSegmentDatasets\LineSegmentDatasets\images\yorkurban\P1020177.jpg")#############################
draw = ImageDraw.Draw(image)
for i in range(len(linelet)):
    if i not in res1:
        draw.line(linelet[i], fill=(255, 165, 0),width=3)
        draw.line((linelet[i][0], linelet[i][1], linelet[i][0] + 0.5, linelet[i][1] + 0.5), (0, 255, 0), width=3)
        draw.line((linelet[i][2], linelet[i][3], linelet[i][2] + 0.5, linelet[i][3] + 0.5), (0, 255, 0), width=3)
image.show()'''


