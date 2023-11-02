import itertools
import random
import sys
from collections import deque, defaultdict
from time import process_time


def getC(coords, it):
    cc = LL[it]
    return (coords[cc[0]], coords[cc[1]], coords[cc[2]], coords[cc[3]])


LL = list(itertools.permutations(list(range(4))))

N = int(input())
start_time = process_time()
C = int(input())
P = int(input())
T = int(input())
Z = int(input())

L = list(range(1, 14))

dx = [1,0,-1,0]
dy = [0,1,0,-1]
waterSources = set()
plants = set()
no_plants = []
plantsPerSpot = defaultdict(set)

# Read grid
grid = [[0 for x in range(N)] for y in range(N)]
for r in range(N):
    for c in range(N):
        grid[r][c] = int(input())
        if grid[r][c] == 1:  # Water source
            waterSources.add((r,c))
        if grid[r][c] == 2:
            plants.add((r,c))
        else:
            no_plants.append((r,c))

for r in range(N):
    for c in range(N):
        if grid[r][c] == 0:  # empty
            for (y, x) in plants:
                dx = abs(c - x)
                dy = abs(r - y)
                if dx ** 2 + dy ** 2 <= Z ** 2:
                    plantsPerSpot[(r,c)].add((y,x))


allDists = defaultdict(dict)
for (r, c) in waterSources:
    cell = (r, c)
    q = deque()
    q.appendleft((cell, 0, {cell}))
    visited = {cell}
    while q and len(allDists[cell].items()) < len(no_plants):
        (y, x), depth, path = q.pop()
        if (y, x) not in allDists[cell]:
            allDists[cell][(y, x)] = depth
            allDists[(y, x)][cell] = depth

        for (a, b) in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)):
            if 0 <= a < N and 0 <= b < N and (a, b) not in visited and (a, b) not in plants:
                visited.add((a, b))
                q.appendleft(((a, b), depth + 1, path | {(a,b)}))


closestWaterSourceDist = {}

for (r, c) in no_plants:
    for (y, x) in waterSources:
        if (r, c) in allDists[(y, x)]:
            if (r, c) not in closestWaterSourceDist or allDists[(y, x)][(r, c)] < closestWaterSourceDist[(r, c)]:
                closestWaterSourceDist[(r, c)] = allDists[(y, x)][(r, c)]

d1 = process_time() - start_time
remainingPlants = plants.copy()
arrosoirs = set()
arrosoirsL = []
remainingPlantsL = [plants.copy()]

while remainingPlants:
    M = 0
    best = set()
    b = None
    for (r, c) in no_plants:
        if (r, c) not in waterSources and (r, c) in closestWaterSourceDist:
                nbPlants = 0
                currPlants = set()
                for (y, x) in plantsPerSpot[(r, c)]:
                    if (y, x) in remainingPlants:
                        nbPlants += 1
                        currPlants.add((y, x))
                if nbPlants > M:
                    M = nbPlants
                    best = currPlants
                    b = (r, c)

    arrosoirs.add(b)
    arrosoirsL.append(b)
    remainingPlants = remainingPlants.difference(best)
    remainingPlantsL.append(remainingPlants)


sortedTargets = list(sorted(arrosoirs, key=lambda x: closestWaterSourceDist[x]))
pipes = set()
pipesL = []
pipesPaths = set()
for i in range(len(sortedTargets)):
    res = sortedTargets[i]
    pipesL.append((pipes.copy(), pipesPaths.copy(), sortedTargets))
    if res not in pipes:
        q = deque()
        q.appendleft((res, set(), {res}))
        visited = {res}

        while q:
            (current, path, pps) = q.pop()
            if current in pipes or current in waterSources:
                pipesPaths |= path
                pipes |= pps
                break

            (y, x) = current
            for (a, b) in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)):
                if 0 <= a < N and 0 <= b < N and (a, b) not in plants and (a, b) not in visited:
                    nei = (a, b)
                    q.appendleft((nei, path|{(current[0], current[1], nei[0], nei[1])}, pps|{nei}))
                    visited.add(nei)

nbCon = 0
counters = {}
countersC = defaultdict(int)
for (a, b, c, d) in pipesPaths:
    if (a,b) not in waterSources:
        countersC[(a, b)] += 1
    if (c,d) not in waterSources:
        countersC[(c, d)] += 1
    if (a,b) not in counters:
        counters[(a, b)] = {0:0, 1:0}
    if (c,d) not in counters:
        counters[(c, d)] = {0:0, 1:0}
    if c == a:
        counters[(a, b)][0] += 1
        counters[(c, d)][0] += 1
    else:
        counters[(a, b)][1] += 1
        counters[(c, d)][1] += 1

for (a,b) in counters:
    if countersC[(a, b)] != 2:
        nbCon += countersC[(a, b)]
    else:
        if counters[(a, b)][1] == counters[(a, b)][0]:
            nbCon += countersC[(a, b)]

bestScore = nbCon*C + P*len(pipes.difference(waterSources)) + T*len(arrosoirs)
bsortedTargets = sortedTargets

d2 = process_time() - start_time

timeForASim = d2-d1
if timeForASim in (0.0, 0):
    timeForASim = 0.001

print("timeForASim", timeForASim, file=sys.stderr)

time = process_time()
while time - start_time + timeForASim < 8.5:

    nb = random.randint(1, len(arrosoirs)//2)

    remainingPlants = remainingPlantsL[nb]
    temp_remainingPlantsL = remainingPlantsL[:nb+1]
    temp_arrosoirsL = arrosoirsL[:nb]
    temp_arrosoirs = set(temp_arrosoirsL)

    while remainingPlants:
        scores = {}
        for (r, c) in no_plants:
            if (r, c) not in waterSources and (r, c) in closestWaterSourceDist:
                nbPlants = 0
                currPlants = set()
                for (y, x) in plantsPerSpot[(r, c)]:
                    if (y, x) in remainingPlants:
                        nbPlants += 1
                        currPlants.add((y, x))
                scores[(r,c)] = (nbPlants, currPlants)

        sortedScores = {a:b for a,b in sorted(scores.items(), key=lambda x:x[1], reverse=True)}
        sortedKeys = list(sortedScores.keys())
        sortedValues = list(sortedScores.values())
        nn = len(sortedScores)

        for i in range(nn):
            if random.randint(1, 30) in L or i == nn-1:
                temp_arrosoirs.add(sortedKeys[i])
                temp_arrosoirsL.append(sortedKeys[i])
                remainingPlants = remainingPlants.difference(sortedValues[i][1])
                temp_remainingPlantsL.append(remainingPlants)
                break

    sortedTargets = list(sorted(temp_arrosoirs, key=lambda x: closestWaterSourceDist[x]))
    it = 0
    while time - start_time + timeForASim < 8.5 and it < 24:
        pipes = set()
        temp_pipesPaths = set()
        all_pipesL = []
        for i in range(len(sortedTargets)):
            res = sortedTargets[i]
            all_pipesL.append((pipes.copy(), temp_pipesPaths.copy(), sortedTargets))
            if res not in pipes:
                q = deque()
                q.appendleft((res, set(), {res}))
                visited = {res}

                while q:
                    (current, path, pps) = q.pop()
                    if current in pipes or current in waterSources:
                        temp_pipesPaths |= path
                        pipes |= pps
                        break

                    (y, x) = current
                    coords = [(y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)]
                    for (a, b) in getC(coords, it):
                        if 0 <= a < N and 0 <= b < N and (a, b) not in plants and (a, b) not in visited:
                            nei = (a, b)
                            q.appendleft((nei, path | {(current[0], current[1], nei[0], nei[1])}, pps | {nei}))
                            visited.add(nei)

        nbCon = 0
        counters = {}
        countersC = defaultdict(int)
        for (a, b, c, d) in temp_pipesPaths:
            if (a, b) not in waterSources:
                countersC[(a, b)] += 1
            if (c, d) not in waterSources:
                countersC[(c, d)] += 1
            if (a, b) not in counters:
                counters[(a, b)] = {0: 0, 1: 0}
            if (c, d) not in counters:
                counters[(c, d)] = {0: 0, 1: 0}
            if c == a:
                counters[(a, b)][0] += 1
                counters[(c, d)][0] += 1
            else:
                counters[(a, b)][1] += 1
                counters[(c, d)][1] += 1

        for (a, b) in counters:
            if countersC[(a, b)] != 2:
                nbCon += countersC[(a, b)]
            else:
                if counters[(a, b)][1] == counters[(a, b)][0]:
                    nbCon += countersC[(a, b)]

        score = nbCon * C + P * len(pipes.difference(waterSources)) + T * len(temp_arrosoirs)

        if score < bestScore:
            bestScore = score
            arrosoirs = temp_arrosoirs
            arrosoirsL = temp_arrosoirsL
            pipesPaths = temp_pipesPaths
            remainingPlantsL = temp_remainingPlantsL
            bsortedTargets = sortedTargets
            pipesL = all_pipesL
        it += 1
        time = process_time()
    time = process_time()

cc = list(range(4))


def getC1(coords):
    return (coords[cc[0]], coords[cc[1]], coords[cc[2]], coords[cc[3]])


while process_time() - start_time + timeForASim < 9.5:
    nb = random.randint(1, len(pipesL)-1)
    all_pipesL = []
    for i in range(nb):
        (pipes, temp_pipesPaths, sortedTargets) = pipesL[i]
        all_pipesL.append((pipes.copy(), temp_pipesPaths.copy(), sortedTargets))
    p, tp, sortedTargets = pipesL[nb]
    pipes = p.copy()
    temp_pipesPaths = tp.copy()

    for i in range(nb, len(sortedTargets)):
        res = bsortedTargets[i]
        all_pipesL.append((pipes.copy(), temp_pipesPaths.copy(), sortedTargets))
        if res not in pipes:
            q = deque()
            q.appendleft((res, set(), {res}))
            visited = {res}
            random.shuffle(cc)

            while q:
                (current, path, pps) = q.pop()
                if current in pipes or current in waterSources:
                    temp_pipesPaths |= path
                    pipes |= pps
                    break

                (y, x) = current
                coords = [(y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)]
                for (a, b) in getC1(coords):
                    if 0 <= a < N and 0 <= b < N and (a, b) not in plants and (a, b) not in visited:
                        nei = (a, b)
                        q.appendleft((nei, path | {(current[0], current[1], nei[0], nei[1])}, pps | {nei}))
                        visited.add(nei)

    nbCon = 0
    counters = {}
    countersC = defaultdict(int)
    for (a, b, c, d) in temp_pipesPaths:
        if (a, b) not in waterSources:
            countersC[(a, b)] += 1
        if (c, d) not in waterSources:
            countersC[(c, d)] += 1
        if (a, b) not in counters:
            counters[(a, b)] = {0: 0, 1: 0}
        if (c, d) not in counters:
            counters[(c, d)] = {0: 0, 1: 0}
        if c == a:
            counters[(a, b)][0] += 1
            counters[(c, d)][0] += 1
        else:
            counters[(a, b)][1] += 1
            counters[(c, d)][1] += 1

    for (a, b) in counters:
        if countersC[(a, b)] != 2:
            nbCon += countersC[(a, b)]
        else:
            if counters[(a, b)][1] == counters[(a, b)][0]:
                nbCon += countersC[(a, b)]

    score = nbCon * C + P * len(pipes.difference(waterSources)) + T * len(sortedTargets)

    if score < bestScore:
        bestScore = score
        pipesPaths = temp_pipesPaths
        pipesL = all_pipesL


output = []
for (r, c, y, x) in pipesPaths:
    output.append("P "+str(r)+" "+str(c)+" "+str(y)+" "+str(x))

for (r, c) in bsortedTargets:
    output.append("S "+str(r)+" "+str(c))

print(len(output))
for o in output:
    print(o)
sys.stdout.flush()

print("end output", file=sys.stderr)
print(process_time()-start_time, file=sys.stderr)
print("score", bestScore, file=sys.stderr)
