import random
import sys
from collections import deque, defaultdict
from time import process_time


def getCoord(ddd,dddd,ddddd):
    (dx, dy, dz) = ddd
    (a, b, c) = dddd
    (rx, ry, rz) = ddddd
    if (rx,ry,rz) == (0,0,0):
        return (a+dx, b+dy, c+dz)
    if (rx,ry,rz) == (0,0,1):
        return (a+dy, b-dx, c+dz)
    if (rx,ry,rz) == (0,0,3):
        return (a-dy, b+dx, c+dz)
    if (rx,ry,rz) == (1,0,0):
        return (a+dx, b-dz, c+dy)
    if (rx,ry,rz) == (3,0,0):
        return (a+dx, b+dz, c-dy)
    if (rx,ry,rz) == (0,1,0):
        return (a-dz, b+dy, c+dx)
    if (rx,ry,rz) == (0,3,0):
        return (a+dz, b+dy, c-dx)

    if (rx,ry,rz) == (2,0,1):
        return (a-dy, b-dx, c+dz)
    if (rx,ry,rz) == (2,0,3):
        return (a+dy, b+dx, c+dz)
    if (rx,ry,rz) == (1,2,0):
        return (a+dx, b-dz, c+dy)
    if (rx,ry,rz) == (3,2,0):
        return (a+dx, b-dz, c+dy)
    if (rx,ry,rz) == (2,1,0):
        return (a-dz, b+dy, c-dx)
    if (rx,ry,rz) == (2,3,0):
        return (a+dz, b+dy, c+dx)

    if (rx,ry,rz) == (0,2,1):
        return (a+dy, b-dx, c-dz)
    if (rx,ry,rz) == (0,2,3):
        return (a-dy, b+dx, c-dz)
    if (rx,ry,rz) == (1,0,2):
        return (a-dx, b-dz, c+dy)
    if (rx,ry,rz) == (3,0,2):
        return (a-dx, b+dz, c-dy)
    if (rx,ry,rz) == (0,1,2):
        return (a-dz, b-dy, c+dx)
    if (rx,ry,rz) == (0,3,2):
        return (a+dz, b-dy, c-dx)

    if (rx,ry,rz) == (2,2,1):
        return (a-dy, b-dx, c-dz)
    if (rx,ry,rz) == (2,2,3):
        return (a+dy, b+dx, c-dz)
    if (rx,ry,rz) == (1,2,2):
        return (a-dx, b-dz, c-dy)
    if (rx,ry,rz) == (3,2,2):
        return (a-dx, b+dz, c+dy)
    if (rx,ry,rz) == (2,1,2):
        return (a-dz, b-dy, c-dx)
    if (rx,ry,rz) == (2,3,2):
        return (a+dz, b-dy, c+dx)

scname, LAB, MM, CTR, BLC = "aa", 2, 1, 20, 1
LAB = int(LAB)
MM = int(MM)
CTR = int(CTR)
BLC = int(BLC)

scnamei, ROT, TIME, STEP, STEP2 = "aa", 1, 4, 3, 1
TIME = float(TIME)/4
STEP = float(STEP)/20
STEP2 = float(STEP2)/200

D = int(input())
start_time = process_time()

coveredX = [[] for i in range(2)]
coveredY = [[] for i in range(2)]


f = [[] for i in range(2)]
r = [[] for i in range(2)]
for i in range(2):
    for k in range(D):
        f[i].append(input())
        coveredX[i].append([-1 for j in range(D)])
    for k in range(D):
        r[i].append(input())
        coveredY[i].append([-1 for j in range(D)])

freeBlocks = [set(), set()]
initFreeBlocks = [set(), set()]
allBlocks = []

for i in range(2):
    for x in range(D):
        for y in range(D):
            for z in range(D):
                if f[i][z][x] == '1' and r[i][z][y] == '1':
                    freeBlocks[i].add((x, y, z))
                    initFreeBlocks[i].add((x, y, z))
best = None
bestScore = None
bestFreeBlocks = None

noChange = 0
inter = 1

TIME_SA = 5.3
reset = False

while process_time() - start_time < TIME or (not best and process_time() - start_time < TIME_SA):
    if freeBlocks[0] == set() or process_time() - start_time > STEP*inter or reset:
        inter += 1
        if not reset:
            counter = [0,0]
            for i in range(2):
                for z in range(D):
                    for y in range(D):
                        if r[i][z][y] == '1' and all([(x,y,z) in freeBlocks[i] for x in range(D)]):
                            counter[i] += 1

                    for x in range(D):
                        if f[i][z][x] == '1' and all([(x,y,z) in freeBlocks[i] for y in range(D)]):
                            counter[i] += 1
                            
            M = max(counter)
            m = min(counter)

            score = - (LAB*len(allBlocks) + MM*(M-m) + CTR*(counter[0] + counter[1]))

            for bloc in allBlocks:
                score -= BLC/len(bloc)
            
            if not best or (allBlocks and score > bestScore):
                bestScore = score
                best = []

                for bloc in allBlocks:
                    best.append(bloc.copy())
                    bestFreeBlocks = [freeBlocks[0].copy(), freeBlocks[1].copy()]
                
        allBlocks = []
        freeBlocks = [initFreeBlocks[0].copy(), initFreeBlocks[1].copy()]
        reset = False

    v = False
    ll = list(freeBlocks[0])
    random.shuffle(ll) 
    for starting in ll:
        nbBreak = 0
        if process_time() - start_time > TIME and not (not best and process_time() - start_time < TIME_SA):
            break

        (x,y,z) = starting


        x1 = min(D-x-1, x)
        x2 = D-x-1 if x1 == x else x
        rrx = list(range(x1, x2+1))
        random.shuffle(rrx)

        y1 = min(D - y - 1, y)
        y2 = D - y - 1 if y1 == y else y
        rry = list(range(y1, y2 + 1))
        random.shuffle(rry)

        z1 = min(D - z - 1, z)
        z2 = D - z - 1 if z1 == z else z
        rrz = list(range(z1, z2 + 1))
        random.shuffle(rrz)

        if ROT == 1:
            orr = [(0, 0, 0), (0, 0, 1), (0, 0, 3), (1, 0, 0), (3, 0, 0), (0, 1, 0), (0, 3, 0)]
        else:
            orr = [(0, 0, 0), (0, 0, 1), (0, 0, 3), (1, 0, 0), (3, 0, 0), (0, 1, 0), (0, 3, 0), (2, 2, 1), (2, 2, 3), (1, 2, 2), (3, 2, 2), (2, 1, 2), (2, 3, 2)]

        random.shuffle(orr)

        for dx in rrx:
            nbBreak = 0
            if v:
                break

            for dy in rry:
                nbBreak = 0
                if v:
                    break

                for dz in rrz:
                    nbBreak = 0
                    if v:
                        break
                    (x, y, z) = starting
                    if (x + dx, y + dy, z + dz) not in freeBlocks[1]:
                        continue

                    for rrr in orr:


                        q = deque()
                        q.appendleft((starting, (x + dx, y + dy, z + dz)))
                        toRemove = [{starting}, {(x + dx, y + dy, z + dz)}]
                        currentBlock = {(starting, (x + dx, y + dy, z + dz))}

                        while q:
                            (x,y,z), (a,b,c) = q.pop()

                            for (newPos0, newPos1) in [((x + 1, y, z), getCoord((1,0,0),(a,b,c),rrr)), ((x - 1, y, z), getCoord((-1,0,0),(a,b,c),rrr)),
                                                       ((x, y + 1, z), getCoord((0,1,0),(a,b,c),rrr)), ((x, y - 1, z), getCoord((0,-1,0),(a,b,c),rrr)),
                                                       ((x, y, z + 1), getCoord((0,0,1),(a,b,c),rrr)), ((x, y, z - 1), getCoord((0,0,-1),(a,b,c),rrr))]:


                                if newPos0 in freeBlocks[0] and newPos0 not in toRemove[0] and newPos1 in freeBlocks[
                                    1] and newPos1 not in toRemove[1]:
                                    toRemove[0].add(newPos0)
                                    toRemove[1].add(newPos1)

                                    currentBlock.add((newPos0,newPos1))
                                    q.appendleft((newPos0,newPos1))

                        T = process_time() - start_time
                        l = len(currentBlock)
                        nbBreak = 0
                        if l > D ** 1.5 or (T > STEP // 6 * inter and l > D ** 1.2) or (
                                T > STEP // 5 * inter and l > D) or (
                                T > STEP // 4 * inter and l > D ** 0.8) or (
                                T > STEP // 3 * inter and l > D ** 0.5) or (T > STEP // 2 * inter and l > 1):
                            allBlocks.append(currentBlock)

                            for elt in toRemove[0]:
                                freeBlocks[0].remove(elt)
                            for elt in toRemove[1]:
                                if elt not in freeBlocks[1]:
                                    reset = True
                                    break
                                freeBlocks[1].remove(elt)

                            v = True
                            break

                        else:
                            nbBreak = random.randint(0, 4)

                    if v or nbBreak > 0:
                        break
                if v or nbBreak > 1:
                    break
            if v or nbBreak > 2:
                break
        if v or nbBreak > 3:
            break

if best:
    allBlocks = []
    for bloc in best:
        allBlocks.append(bloc.copy())
    freeBlocks = [bestFreeBlocks[0].copy(), bestFreeBlocks[1].copy()]
    sumSize = 0

    rem = random.randint(0, len(allBlocks)-1)

    for (p0, p1) in allBlocks[rem]:
        freeBlocks[0].add(p0)
        freeBlocks[1].add(p1)

    sizeToBeat = len(allBlocks[rem])

    del allBlocks[rem]

while process_time() - start_time < TIME_SA:
    if freeBlocks[0] == set() or (process_time() - start_time > STEP2*inter) or reset:
        inter += 1 
        if not reset:
            counter = [0,0]
            for i in range(2):
                for z in range(D):
                    for y in range(D):
                        if r[i][z][y] == '1' and all([(x,y,z) in freeBlocks[i] for x in range(D)]):
                            counter[i] += 1

                    for x in range(D):
                        if f[i][z][x] == '1' and all([(x,y,z) in freeBlocks[i] for y in range(D)]):
                            counter[i] += 1
                            
            M = max(counter)
            m = min(counter)

            score = - (LAB*len(allBlocks) + MM*(M-m) + CTR*(counter[0] + counter[1]))

            for bloc in allBlocks:
                score -= BLC/len(bloc)

            if not best or (allBlocks and score > bestScore):
                bestScore = score
                best = []

                for bloc in allBlocks:
                    best.append(bloc.copy())
                    bestFreeBlocks = [freeBlocks[0].copy(), freeBlocks[1].copy()]
                #print(best)

        allBlocks = []
        for bloc in best:
            allBlocks.append(bloc.copy())
        freeBlocks = [bestFreeBlocks[0].copy(), bestFreeBlocks[1].copy()]
        reset = False

        rem = random.randint(0, len(allBlocks) - 1)

        for (p0, p1) in allBlocks[rem]:
            freeBlocks[0].add(p0)
            freeBlocks[1].add(p1)
        sizeToBeat = len(allBlocks[rem])

        del allBlocks[rem]
        sumSize = 0

    v = False
    ll = list(freeBlocks[0])
    random.shuffle(ll) 
    for starting in ll:
        nbBreak = 0
        if process_time() - start_time > TIME_SA:
            break

        (x,y,z) = starting


        x1 = min(D-x-1, x)
        x2 = D-x-1 if x1 == x else x
        rrx = list(range(x1, x2+1))
        random.shuffle(rrx)

        y1 = min(D - y - 1, y)
        y2 = D - y - 1 if y1 == y else y
        rry = list(range(y1, y2 + 1))
        random.shuffle(rry)

        z1 = min(D - z - 1, z)
        z2 = D - z - 1 if z1 == z else z
        rrz = list(range(z1, z2 + 1))
        random.shuffle(rrz)


        if ROT == 1:
            orr = [(0, 0, 0), (0, 0, 1), (0, 0, 3), (1, 0, 0), (3, 0, 0), (0, 1, 0), (0, 3, 0)]
        else:
            orr = [(0, 0, 0), (0, 0, 1), (0, 0, 3), (1, 0, 0), (3, 0, 0), (0, 1, 0), (0, 3, 0), (2, 2, 1), (2, 2, 3), (1, 2, 2), (3, 2, 2), (2, 1, 2), (2, 3, 2)]


        random.shuffle(orr)

        for dx in rrx:
            nbBreak = 0
            if v:
                break

            for dy in rry:
                nbBreak = 0
                if v:
                    break

                for dz in rrz:
                    nbBreak = 0
                    if v:
                        break
                    (x, y, z) = starting
                    if (x + dx, y + dy, z + dz) not in freeBlocks[1]:

                        continue

                    for rrr in orr:

                                q = deque()
                                q.appendleft((starting, (x + dx, y + dy, z + dz)))
                                toRemove = [{starting}, {(x + dx, y + dy, z + dz)}]
                                currentBlock = {(starting, (x + dx, y + dy, z + dz))}

                                while q:
                                    (x,y,z), (a,b,c) = q.pop()

                                    for (newPos0, newPos1) in [((x + 1, y, z), getCoord((1,0,0),(a,b,c),rrr)), ((x - 1, y, z), getCoord((-1,0,0),(a,b,c),rrr)),
                                                               ((x, y + 1, z), getCoord((0,1,0),(a,b,c),rrr)), ((x, y - 1, z), getCoord((0,-1,0),(a,b,c),rrr)),
                                                               ((x, y, z + 1), getCoord((0,0,1),(a,b,c),rrr)), ((x, y, z - 1), getCoord((0,0,-1),(a,b,c),rrr))]:


                                        if newPos0 in freeBlocks[0] and newPos0 not in toRemove[0] and newPos1 in freeBlocks[
                                            1] and newPos1 not in toRemove[1]:
                                            toRemove[0].add(newPos0)
                                            toRemove[1].add(newPos1)

                                            currentBlock.add((newPos0,newPos1))
                                            q.appendleft((newPos0,newPos1))


                                nbBreak = 0
                                if len(currentBlock) > 1:
                                    allBlocks.append(currentBlock)

                                    for elt in toRemove[0]:
                                        freeBlocks[0].remove(elt)
                                    for elt in toRemove[1]:
                                        if elt not in freeBlocks[1]:
                                            reset = True
                                            break
                                        freeBlocks[1].remove(elt)

                                    v = True
                                    break
                                else:
                                    nbBreak = random.randint(0, 4)

                    if v or nbBreak > 0:
                        break
                if v or nbBreak > 1:
                    break
            if v or nbBreak > 2:
                break
        if v or nbBreak > 3:
            break

allBlocks = best
linesFound = [defaultdict(list), defaultdict(list)]
if not bestFreeBlocks:
    bestFreeBlocks = freeBlocks
for i in range(2):
    for (x,y,z) in bestFreeBlocks[i]:

        (a,b,c) = (x,y,z)
        current = {(x,y,z)}
        while (a,b,c) in bestFreeBlocks[i]:
            linesFound[i][a-x+1].append(current.copy())
            a += 1
            current.add((a,b,c))

        (a,b,c) = (x,y,z)
        current = {(x,y,z)}
        while (a,b,c) in bestFreeBlocks[i]:
            linesFound[i][x-a+1].append(current.copy())
            a -= 1
            current.add((a,b,c))

        (a,b,c) = (x,y,z)
        current = {(x,y,z)}
        while (a,b,c) in bestFreeBlocks[i]:
            linesFound[i][b-y+1].append(current.copy())
            b += 1
            current.add((a,b,c))

        (a, b, c) = (x, y, z)
        current = {(x, y, z)}
        while (a, b, c) in bestFreeBlocks[i]:
            linesFound[i][y - b + 1].append(current.copy())
            b -= 1
            current.add((a, b, c))

        (a,b,c) = (x,y,z)
        current = {(x,y,z)}
        while (a,b,c) in bestFreeBlocks[i]:
            linesFound[i][z-c+1].append(current.copy())
            c -= 1
            current.add((a,b,c))

        (a,b,c) = (x,y,z)
        current = {(x,y,z)}
        while (a,b,c) in bestFreeBlocks[i]:
            linesFound[i][c-z+1].append(current.copy())
            c += 1
            current.add((a,b,c))


bb = [[0 for j in range(D * D * D)] for i in range(2)]

for j in range(len(allBlocks)):
    block = allBlocks[j]
    for (x,y,z),(a,b,c) in block:
        bb[0][x * D * D + y * D + z] = j+1

        bb[1][a * D * D + b * D + c] = j+1


N = min(max(linesFound[0].keys()), max(linesFound[1].keys()))
pairs = []
while N > 1 and process_time() - start_time < 5.8:

    if 0 < min(len(linesFound[0][N]), len(linesFound[1][N])):
        pairs.append((linesFound[0][N][0], linesFound[1][N][0]))
        for k in range(2):
            for coord in linesFound[k][N][0]:
                for i in range(2, N+1):
                    dim = linesFound[k][i]
                    j = 0
                    while j < len(dim):
                        line = dim[j]
                        if coord in line:
                            del linesFound[k][i][j]
                        else:
                            j += 1
    else:
        N -= 1


j = len(allBlocks) #+ 1
for (l1, l2) in pairs:#(x, y, z),(a,b,c)
    for (x, y, z) in l1:
        bb[0][x * D * D + y * D + z] = j + 1
        coveredX[0][z][x] = y
        coveredY[0][z][y] = x
    for (x, y, z) in l2:
        bb[1][x * D * D + y * D + z] = j + 1
        coveredX[1][z][x] = y
        coveredY[1][z][y] = x
    j += 1


for i in range(2):
    n = D * D * D * 3
    for z in range(D):
        for y in range(D):
            if r[i][z][y] == '1' and all([bb[i][x * D * D + y * D + z] == 0 for x in range(D)]):
                for x in range(D):
                    if f[i][z][x] == '1' and r[i][z][y] == '1':
                        bb[i][x * D * D + y * D + z] = n
                        n += 1
                        break

        for x in range(D):
            if f[i][z][x] == '1' and all([bb[i][x * D * D + y * D + z] == 0 for y in range(D)]):
                for y in range(D):
                    if f[i][z][x] == '1' and r[i][z][y] == '1':
                        bb[i][x * D * D + y * D + z] = n
                        n += 1
                        break


mapBBToCC = {0: 0}
n = 1
cc = [[0 for j in range(D * D * D)] for i in range(2)]
M = 1
for i in range(2):
    for j in range(len(bb[i])):
        nn = bb[i][j]
        if nn not in mapBBToCC:
            mapBBToCC[nn] = n
            cc[i][j] = n
            M = max(M, n)
            n += 1
        else:
            cc[i][j] = mapBBToCC[nn]


print(M)
print(' '.join(map(str, cc[0])))
print(' '.join(map(str, cc[1])))
