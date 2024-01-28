
from collections import defaultdict
v = True
currentCounting = []
lines = []
sums = defaultdict(int)
ccccc = defaultdict(int)
iiii = 0
while 1:
    iiii += 1
    try:
        a = input().split()
        if "cd" == a[1]:
            if ".." == a[2]:
                currentCounting = currentCounting[:-1]
            else:
                current = a[-1]
                currentCounting.append(current)
                ccccc[current] += 1
        elif a[0].isdigit():
            for element in currentCounting:
                sums[element] += int(a[0])
    except Exception:
        total = 0
        for x, y in sums.items():
            if y <= 100000:
                total += y
        print(total, ccccc)
        exit()

