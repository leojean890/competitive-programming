import random
from collections import deque
from time import process_time

T, H, W, I = [int(i) for i in input().split()]
entrance = (I,0)
start_time = process_time()

nbWaterways = 0

horizontal_bars = []
vertical_bars = []
for i in range(H-1):
    horizontal_bars.append([int(i) for i in input()])
    nbWaterways += horizontal_bars[-1].count(1)
for i in range(H):
    vertical_bars.append([int(i) for i in input()])
    nbWaterways += vertical_bars[-1].count(1)

def validateBars(dy,dx,i,j):
    if dy == 1 and not horizontal_bars[i-1][j]:
        return True
    if dy == -1 and not horizontal_bars[i][j]:
        return True
    if dx == 1 and not vertical_bars[i][j-1]:
        return True
    if dx == -1 and not vertical_bars[i][j]:
        return True

chosenPath = set()
chosenCropsSpots = set()
best = 0

while process_time() - start_time < 1:
    q = deque()
    q.appendleft(entrance)
    cropsSpots = set()
    path = {entrance}

    while q:
        y, x = q.pop()
        for (i,j,dy,dx) in ((y+1,x,1,0), (y-1,x,-1,0), (y,x+1,0,1), (y,x-1,0,-1)):
            if 0 <= i < H and 0 <= j < W and (i,j) not in cropsSpots and (i,j) not in path and validateBars(dy,dx,i,j):
                value = random.randint(1,10)
                if value == 1:
                    cropsSpots.add((i,j))
                else:
                    path.add((i,j))
                    q.appendleft((i,j))

    if len(cropsSpots) > best:
        best = len(cropsSpots)
        chosenPath = path
        chosenCropsSpots = cropsSpots

for (a,b) in chosenPath:
    q = deque()
    q.appendleft(entrance)
    cropsSpots = set()
    path = chosenPath.difference({(a,b)})
    visited = {entrance}

    while q:
        y, x = q.pop()
        for (i,j,dy,dx) in ((y+1,x,1,0), (y-1,x,-1,0), (y,x+1,0,1), (y,x-1,0,-1)):
            if 0 <= i < H and 0 <= j < W and (i,j) not in visited and validateBars(dy,dx,i,j):
                visited.add((i, j))
                if (i,j) not in path:
                    if (i,j) not in cropsSpots:
                        cropsSpots.add((i,j))
                else:
                    q.appendleft((i,j))

    if all({elt not in chosenCropsSpots for elt in chosenCropsSpots.difference(cropsSpots)}):
        best = len(cropsSpots)
        chosenPath = path
        chosenCropsSpots = cropsSpots

K = int(input())

avg = 0
crops = {}
for i in range(K):
    crops[i+1] = [int(i) for i in input().split()]
    avg += (crops[i+1][1] - crops[i+1][0])
avg /= K

sumGaps = 0
for i in range(K):
    sumGaps += abs(avg - (crops[i+1][1] - crops[i+1][0]))
sumGaps /= K

takenIndexes = {}
takenSpots = {}
output = []

for turn in range(1,T+1):
    for (index, (s,d)) in crops.items(): 
        if turn > d and index in takenIndexes:
            del takenSpots[takenIndexes[index]]
            del takenIndexes[index]

    availableSpots = []
    for (i, j) in chosenCropsSpots:
        if (i, j) not in takenSpots:
            availableSpots.append((i, j))

    scores = {}
    for (index, (s,d)) in crops.items(): 
        if index not in takenIndexes and turn <= s:

            scores[index] = (d-s+1) + max(2,150-(sumGaps-5)*100)*(turn-s)

    sortedCrops = list({a:b for a,b in sorted(scores.items(), key=lambda x:x[1], reverse=True)}.keys())

    for k in range(min(len(sortedCrops),len(availableSpots))):
        index = sortedCrops[k]
        (i,j) = availableSpots[k]

        takenIndexes[index] = (i, j)
        takenSpots[(i, j)] = index
        output.append((index, i, j, turn))


print(len(output))

for elt in output:
    print(*elt)
