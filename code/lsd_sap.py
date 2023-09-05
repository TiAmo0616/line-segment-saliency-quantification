import math
import cv2
import numpy as np
import os
import json

from code.init import read_dir
from sap import ap, com


def line_score(array,test, threshold):
    tplist,fplist,scores=[],[],[]
    n_gt=0
    for i in range(len(array)):
        img = cv2.cvtColor(array[i], cv2.COLOR_BGR2GRAY)
        lsd = cv2.createLineSegmentDetector(2)
        dlines = lsd.detect(img)
        tp = [0 for a in range(len(dlines[0]))]
        fp = [0 for a in range(len(dlines[0]))]
        score=[]
        used = []
        n_gt+=len(test[i]['lines'])
        for k in range(len(dlines[0])):
            score.append(dlines[3][k][0])
            for j in range(len(test[i]['lines'])):
                temp = com(dlines[0][k][0], test[i]['lines'][j])
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



array=read_dir("D:\LineSegmentDatasets\LineSegmentDatasets\images\wireframe-test")
with open(r"D:\LineSegmentDatasets\LineSegmentDatasets\annotations\wireframe-test.json") as f2:
    test = json.load(f2)



print(100*line_score(array,test,15))







