# coding=utf-8
import cv2
import numpy as np

img0 = cv2.imread("D:\LineSegmentDatasets\LineSegmentDatasets\images\yorkurban\P1020171.jpg")
img = cv2.cvtColor(img0,cv2.COLOR_BGR2GRAY)
lsd = cv2.createLineSegmentDetector(2)
dlines = lsd.detect(img)
cnt=0
nfa=0
lsd=[]

for dline in dlines[0]:
    x0 = int(round(dline[0][0]))
    y0 = int(round(dline[0][1]))
    x1 = int(round(dline[0][2]))
    y1 = int(round(dline[0][3]))
    cv2.line(img0, (x0, y0), (x1,y1), (0,255,0), 1, cv2.LINE_AA)

# 显示并保存结果
cv2.imwrite('test3_r.jpg', img0)
cv2.imshow("LSD", img0)
cv2.waitKey(0)
cv2.destroyAllWindows()
