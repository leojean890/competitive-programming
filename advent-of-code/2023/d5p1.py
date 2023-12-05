import sys

lines = []
for i in range(245):
    lines.append(input())

seeds = [int(i) for i in lines[0].split()[1:]]

maps = []
currMap = []
current = 3

while current < len(lines):
    while current < len(lines) and lines[current]:
        currMap.append([int(i) for i in lines[current].split()])
        current += 1

    current += 2
    maps.append(currMap)
    currMap = []
M = sys.maxsize
for seed in seeds:
    current = seed
    for currMap in maps:
        for currList in currMap:
            to, frm, lgth = currList
            if current in range(frm, frm+lgth):
                delta = current - frm
                current = to+delta
                break
    M = min(current, M)
print(M) # 226172555
