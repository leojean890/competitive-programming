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
            dy = y-a
            dx = x-b
            ny = a-dy
            nx = b-dx
            if ny in range(N) and nx in range(N) and (ny,nx) not in allRealPositions:
                allRealPositions.add((ny,nx))
            ny = y+dy
            nx = x+dx
            if ny in range(N) and nx in range(N) and (ny,nx) not in allRealPositions:
                allRealPositions.add((ny,nx))


print(len(allRealPositions), process_time() - start_time) # 320

