import sys
from collections import defaultdict
from time import process_time

start_time = process_time()
N = 50
positions = defaultdict(list)
allPositions = set()
allRealPositions = set()
sys.setrecursionlimit(10000000)
# pour toutes les paires, je reproduis le delta a droite et gauche
for i in range(N):
    line = input()
    for j in range(N):
        if line[j] not in ".#":
            positions[line[j]].append((i,j))

for letter in positions:
    s = len(positions[letter])
    for i in range(s):
        (a, b) = positions[letter][i]
        for j in range(i+1,s):
            (y, x) = positions[letter][j]
            if (a,b) not in allRealPositions:
                allRealPositions.add((a,b))
            if (y,x) not in allRealPositions:
                allRealPositions.add((y,x))

            dy = y-a
            dx = x-b

            c,d=a,b
            while c-dy in range(N) and d-dx in range(N):
                c -= dy
                d -= dx
                if (c, d) not in allRealPositions:
                    allRealPositions.add((c, d))

            c,d=y,x
            while c+dy in range(N) and d+dx in range(N):
                c += dy
                d += dx
                if (c, d) not in allRealPositions:
                    allRealPositions.add((c, d))

print(len(allRealPositions), process_time() - start_time) # 1157

