import math


def splice(lst, angle_list, gradlist, lenlist, zlist, cwlist, chlist, blist, sqlist):  # 直线拼接
    res = []
    for i in range(len(lst)):
        for j in range(len(lst)):
            if i != j:
                if abs(angle_list[i] - angle_list[j]) < 0.01 and abs(gradlist[i] - gradlist[j]) < 10 and abs(
                        blist[i] - blist[j]) < 5:
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
                            k = (h2 - h1) / (w2 - w1)
                            b = h2 - k * w2
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
                            k = (h2 - h1) / (w2 - w1)
                            b = h2 - k * w2
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
    return res