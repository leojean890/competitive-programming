data = []
allData = []
found = None
for i in range(1000):
    current = int(input())
    data.append(current)
    allData.append(current)
    if i > 24 and not found:
        v = False
        for j in range(24):
            for k in range(j+1, 25):
                if data[j]+data[k] == data[-1]:
                    v = True
                    break
            if v:
                break
        if not v:
            found = data[-1]
            print(found) #1492208709
        data = data[1:]


for i in range(999):
    sm = allData[i]
    for j in range(i+1, 1000):
        sm += allData[j]
        if sm == found:
            print(min(allData[i:j+1]) + max(allData[i:j+1]))
            exit() # 238243506
