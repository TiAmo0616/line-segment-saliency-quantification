import math

from line_pretreat import pretreat


def get_data_feature(linelet):
    lenlist = []
    sqlist = []
    cwlist = []
    chlist = []
    angle_list = []
    blist = []
    zlist = []
    for i in range(len(linelet)):
        w1 = (linelet[i][0])
        w2 = (linelet[i][2])
        h1 = (linelet[i][1])
        h2 = (linelet[i][3])
        lenlist.append(math.sqrt((w1 - w2) * (w1 - w2) + (h1 - h2) * (h1 - h2)))
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
    res = [lenlist,sqlist,cwlist,chlist,angle_list,blist,zlist]
    return res

def simple_get_feature(elder):
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
        if w1 == w2:
            anglelist_elder.append(math.pi / 2)
        else:
            k = (h1 - h2) / (w1 - w2)
            anglelist_elder.append(math.atan(k))
    return [sqlist_elder,lenlist_elder,anglelist_elder]

def get_feature_gray(linelet,w,h,sobelxy_gray):
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
    return [lenlist,sqlist,cwlist,chlist,angle_list,blist,zlist,gradlist]

def get_gray_density(test,test_gray):
    gradlist_test = []
    lenlist_test = []
    for a in range(len(test_gray)):
        w = test_gray[a].shape[1]
        h = test_gray[a].shape[0]
        testline = pretreat(test[a]['lines'])
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
    return [gradlist_test,lenlist_test]