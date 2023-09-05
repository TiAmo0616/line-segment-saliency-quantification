import math


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