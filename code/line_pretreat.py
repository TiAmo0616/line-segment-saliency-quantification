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
