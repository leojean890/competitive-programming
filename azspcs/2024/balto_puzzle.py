import collections
import random
from collections import defaultdict
from time import process_time
import heapq
from typing import List, Tuple
from copy import deepcopy

class PriorityQueue:
    def __init__(self):
        self.elements: List[Tuple[tuple, tuple]] = []

    def empty(self) -> bool:
        return not self.elements

    def put(self, item: tuple, priority: tuple):
        heapq.heappush(self.elements, (priority, item))

    def get(self) -> tuple:
        return heapq.heappop(self.elements)[1]


target = {}
init_lines = {}
lines = {}
N = int(input())
oldBest = {3:71,4:192,5:845,6:1010,7:1129,8:4829,9:6737,10:10182,11:13572,12:18491,13:23748,14:30413,15:36078,16:45537,17:54026,18:63963,19:76180,20:89580,21:104881,22:122236,23:139549,24:158793,25:179248,26:201686,27:226757}[N]
TTT = 100.0
if N > 14:
    TTT = 300.0
if N > 20:
    TTT = 400.0
start_time = process_time()
middle = N-1
M = 2 * N - 1
MAX = -1
for i in range(M):
    init_lines[i] = input().split(",")
    MAX += len(init_lines[i])

counter = 0
counter1 = 0
for i in range(N):
    target[i] = {}
    lines[i] = {}
    target[M-1-i] = {}
    lines[M-1-i] = {}
    start = abs(middle-i)/2
    for j in range(len(init_lines[i])):
        if i == N-1 and j == len(init_lines[i])//2:
            counter += 1
            target[i][start + j] = 0
        else:
            counter += 1
            if i != N - 1:
                target[i][start + j] = counter
            target[M - 1 - i][start + len(init_lines[i]) - 1 - j] = MAX-counter1
            counter1 += 1

        lines[i][start+j] = int(init_lines[i][j])
        if lines[i][start+j] == 0:
            y,x = (i,start+j)
        lines[M-1-i][start+j] = int(init_lines[M-1-i][j])
        if lines[M-1-i][start+j] == 0:
            y,x = (M-1-i,start+j)

factorPerSpot = {}
categs = defaultdict(list)
categPerSpot = defaultdict(int)
next_d = {}

for a,b in sorted(lines.items()):
    srtdB = list({x:y for x,y in sorted(b.items(), key=lambda z:z[0])}.keys())
    print(a,b)
    print(a,target[a])
    next_d[a] = {max(b.keys())+1:0,min(b.keys())-1:0}

    for i in range(len(srtdB)//2+1):
        cat = min(i, a, len(lines.items()) - 1 - a, len(srtdB) - 1 - i)
        categPerSpot[(a,srtdB[i])] = cat
        categPerSpot[(a,srtdB[len(srtdB)-1-i])] = cat
        categs[cat].append((a,srtdB[i]))
        categs[cat].append((a,srtdB[len(srtdB)-1-i]))
        multiplier = 3*N - 2 - 3*cat
        if (a,srtdB[i]) not in factorPerSpot:
            if target[a][srtdB[i]] > 0:
                factorPerSpot[(a,srtdB[i])] = 10**multiplier + 3**target[a][srtdB[i]]
            if target[a][srtdB[len(srtdB)-1-i]] > 0:
                factorPerSpot[(a,srtdB[len(srtdB)-1-i])] = 10**multiplier + 3**target[a][srtdB[len(srtdB)-1-i]]

sortedTargets = list({a:b for a,b in sorted(factorPerSpot.items(), key=lambda x:x[1], reverse=True)}.keys())
print(y,x)

init_y,init_x = y,x

def get_next(x,y):
    if x in next_d[y]:
        return "X"
    else:
        return x


M1 = 100000
a1 = list(range(1, 7))
a2 = list("ABCDEF")


currentPath = ""

catkeys = list(sorted(categs.keys()))
(y, x) = (init_y,init_x)
for mutation in currentPath:

                    if mutation not in a2:
                        mutation = int(mutation)

                    if mutation in (1, 'A'):
                        if y == 0: continue
                        u, v = ((y - 1) % M, get_next(x + 0.5, (y - 1) % M)) if mutation == 1 else (y, get_next(x + 1, y))
                        u1, v1 = (y, get_next(x + 1, y)) if mutation == 1 else ((y - 1) % M, get_next(x + 0.5, (y - 1) % M))
                        if "X" in (v, v1): continue
                    elif mutation in (2, 'B'):
                        if y == M - 1: continue
                        u, v = (y, get_next(x + 1, y)) if mutation == 2 else ((y + 1) % M, get_next(x + 0.5, (y + 1) % M))
                        u1, v1 = ((y + 1) % M, get_next(x + 0.5, (y + 1) % M)) if mutation == 2 else (y, get_next(x + 1, y))
                        if "X" in (v, v1): continue
                    elif mutation in (3, 'C'):
                        if y == M - 1: continue
                        u, v = ((y + 1) % M, get_next(x + 0.5, (y + 1) % M)) if mutation == 3 else (
                        (y + 1) % M, get_next(x - 0.5, (y + 1) % M))
                        u1, v1 = ((y + 1) % M, get_next(x - 0.5, (y + 1) % M)) if mutation == 3 else (
                        (y + 1) % M, get_next(x + 0.5, (y + 1) % M))
                        if "X" in (v, v1): continue
                    elif mutation in (4, 'D'):
                        if y == M - 1: continue
                        # h = x-0.5 if y < 4 else
                        u, v = ((y + 1) % M, get_next(x - 0.5, (y + 1) % M)) if mutation == 4 else (y, get_next(x - 1, y))
                        u1, v1 = (y, get_next(x - 1, y)) if mutation == 4 else ((y + 1) % M, get_next(x - 0.5, (y + 1) % M))
                        if "X" in (v, v1): continue
                    elif mutation in (5, 'E'):
                        if y == 0: continue
                        u, v = (y, get_next(x - 1, y)) if mutation == 5 else ((y - 1) % M, get_next(x - 0.5, (y - 1) % M))
                        u1, v1 = ((y - 1) % M, get_next(x - 0.5, (y - 1) % M)) if mutation == 5 else (y, get_next(x - 1, y))
                        if "X" in (v, v1): continue
                    elif mutation in (6, 'F'):
                        if y == 0: continue
                        u, v = ((y - 1) % M, get_next(x - 0.5, (y - 1) % M)) if mutation == 6 else (
                        (y - 1) % M, get_next(x + 0.5, (y - 1) % M))
                        u1, v1 = ((y - 1) % M, get_next(x + 0.5, (y - 1) % M)) if mutation == 6 else (
                        (y - 1) % M, get_next(x - 0.5, (y - 1) % M))
                        if "X" in (v, v1): continue

                    lines[y][x], lines[u][v], lines[u1][v1] = lines[u1][v1], lines[y][x], lines[u][v]
                    y, x = u, v


spotsPerValue = {}
score = len(currentPath)/1000000
for y2,line in sorted(lines.items()):
    for (x2,value) in sorted(line.items()):
        spotsPerValue[value] = (y2,x2)
for y1, line in target.items():
    for (x1, value1) in line.items():
        if value1 != 0:
            (y2,x2) = spotsPerValue[value1]
            dy = abs(y2-y1)
            dx = abs(x2-x1)
            d = dy + dx - 0.5*min(2*dx,dy)
            score += d

init_y, init_x = y, x
M1 = score
initial_score = score
print("oo",M1,process_time() - start_time)


(init_y,init_x) = (y, x)
in_lines = deepcopy(lines)
(in_y,in_x) = (y, x)
ncurrentPath = currentPath
rebootOptions = {1:(in_lines,ncurrentPath,in_y,in_x, M1)}
rebootOptionsList = list(rebootOptions.values())
SAVINGS = {}
currSave = 0
nbReboots = 0
SZ = 30
SZ2 = 15
breakCounter = defaultdict(int)
nbSuccessiveReboots = 0
nM2 = None

while True:
    elapsed = process_time()
    catkeys = list(sorted(categs.keys()))
    print("reboot", elapsed)
    nbReboots += 1

    if len(currentPath) >= oldBest:
        if nM2 and (nM2 - float(int(nM2)))*1000000.0 + TTT < oldBest: # 400 pour anticiper les allers et venues pour fixer ce qu'il reste
            nbSuccessiveReboots = 21 #=> attention c risqué que je me retrouve en boucle infinie
        else:
            M1 = 0.9999999999
        if nM2:
            print("diff",(nM2 - float(int(nM2)))*1000000.0 + TTT, oldBest)
        print("len(currentPath) >= oldBest", len(currentPath), oldBest)

    if M1 < 4 or nbSuccessiveReboots > 20:
        if M1 < 1 or not nM2:
            (in_lines, ncurrentPath, in_y,in_x, M1) = random.choice(rebootOptionsList)
            lines = deepcopy(in_lines)
            (init_y,init_x) = (in_y,in_x)
            currentPath = ncurrentPath
            print("big reboot 1", rebootOptions.keys(), len(rebootOptionsList))
            SAVINGS = {}
            currSave = 0
        else:
            lines = deepcopy(in_lines2)
            (init_y,init_x) = (in_y2,in_x2)
            currentPath = ncurrentPath2
            M1 = nM2
            SAVINGS = {}
            currSave = 0
            print("big reboot 2", M1)

        nbReboots = 0
        breakCounter = defaultdict(int)
        nbSuccessiveReboots = 0

    if nbReboots > 10:
        nbSuccessiveReboots += 1
        aaa = random.randint(0,1)
        if aaa > 0:
            nbReboots = 0
            M1 = 100000
            #currSave = random.randint(0,currSave-1)
            if (currSave+1)%SZ in SAVINGS:
                (init_y, init_x, currentPath, lines) = SAVINGS[(currSave+1)%SZ]
            elif (currSave+SZ2)%SZ in SAVINGS:
                (init_y, init_x, currentPath, lines) = SAVINGS[(currSave+SZ2)%SZ]
            elif currSave > 1:
                currSave = random.randint(0,currSave-1)
                (init_y, init_x, currentPath, lines) = SAVINGS[currSave]

            print("change lines")
    for categ in catkeys:
        aaa = random.randint(0,4)
        if aaa == 0:
            categs[categ] = list(sorted(categs[categ], key=lambda x:x[0]-x[1]))
        if aaa == 1:
            categs[categ] = list(sorted(categs[categ], key=lambda x:x[0]+x[1]))
        if aaa == 2:
            categs[categ] = list(sorted(categs[categ], key=lambda x:-x[0]-x[1]))
        if aaa == 3:
            categs[categ] = list(sorted(categs[categ], key=lambda x:-x[0]+x[1]))
    breaked = False
    change = True
    while not breaked and change and M1>3:
        change = False
        breaked = False
        for categ in catkeys:
            solved = set()
            for (cy,cx) in categs[categ]:
                if lines[cy][cx] == target[cy][cx]:
                    solved.add((cy,cx))
                    continue

                q = PriorityQueue()
                q.put((init_y,init_x,currentPath,lines),0)

                ll = []
                for y2, line in sorted(lines.items()):
                    for (x2, value) in sorted(line.items()):
                        ll.append(value)

                hhh = tuple(ll)
                visited = {hhh}

                while not q.empty():
                    (y, x, path, lines1) = q.get()

                    if len(visited) > 2000:
                        visited.clear()
                        break

                    if lines1[cy][cx] == target[cy][cx]:
                        init_y, init_x, currentPath, lines = y, x, path, lines1
                        SAVINGS[currSave] = (init_y, init_x, currentPath, deepcopy(lines))
                        currSave = (currSave+1)%SZ
                        nbReboots = 0
                        change = True
                        break

                    if not path:
                        mutations = a1 + a2
                    else:
                        mutations = a1 if path[-1] in a2 else a2

                    for mutation in mutations:
                        ny, nx = y, x
                        nLines = {}
                        for (a, b) in lines1.items():
                            nLines[a] = b.copy()

                        if mutation in (1, 'A'):
                            if y == 0: continue
                            u, v = ((y - 1) % M, get_next(x + 0.5, (y - 1) % M)) if mutation == 1 else (y, get_next(x + 1, y))
                            u1, v1 = (y, get_next(x + 1, y)) if mutation == 1 else ((y - 1) % M, get_next(x + 0.5, (y - 1) % M))
                            if "X" in (v, v1): continue
                        elif mutation in (2, 'B'):
                            if y == M - 1: continue
                            u, v = (y, get_next(x + 1, y)) if mutation == 2 else ((y + 1) % M, get_next(x + 0.5, (y + 1) % M))
                            u1, v1 = ((y + 1) % M, get_next(x + 0.5, (y + 1) % M)) if mutation == 2 else (y, get_next(x + 1, y))
                            if "X" in (v, v1): continue
                        elif mutation in (3, 'C'):
                            if y == M - 1: continue
                            u, v = ((y + 1) % M, get_next(x + 0.5, (y + 1) % M)) if mutation == 3 else (
                            (y + 1) % M, get_next(x - 0.5, (y + 1) % M))
                            u1, v1 = ((y + 1) % M, get_next(x - 0.5, (y + 1) % M)) if mutation == 3 else (
                            (y + 1) % M, get_next(x + 0.5, (y + 1) % M))
                            if "X" in (v, v1): continue
                        elif mutation in (4, 'D'):
                            if y == M - 1: continue
                            # h = x-0.5 if y < 4 else
                            u, v = ((y + 1) % M, get_next(x - 0.5, (y + 1) % M)) if mutation == 4 else (y, get_next(x - 1, y))
                            u1, v1 = (y, get_next(x - 1, y)) if mutation == 4 else ((y + 1) % M, get_next(x - 0.5, (y + 1) % M))
                            if "X" in (v, v1): continue
                        elif mutation in (5, 'E'):
                            if y == 0: continue
                            u, v = (y, get_next(x - 1, y)) if mutation == 5 else ((y - 1) % M, get_next(x - 0.5, (y - 1) % M))
                            u1, v1 = ((y - 1) % M, get_next(x - 0.5, (y - 1) % M)) if mutation == 5 else (y, get_next(x - 1, y))
                            if "X" in (v, v1): continue
                        elif mutation in (6, 'F'):
                            if y == 0: continue
                            u, v = ((y - 1) % M, get_next(x - 0.5, (y - 1) % M)) if mutation == 6 else (
                            (y - 1) % M, get_next(x + 0.5, (y - 1) % M))
                            u1, v1 = ((y - 1) % M, get_next(x + 0.5, (y - 1) % M)) if mutation == 6 else (
                            (y - 1) % M, get_next(x - 0.5, (y - 1) % M))
                            if "X" in (v, v1): continue

                        if lines1[u1][v1] == target[u1][v1] and (categPerSpot[(u1,v1)] < categ or ((u1,v1) in categs[categ] and categs[categ].index((u1,v1)) < categs[categ].index((cy,cx)))):
                            continue

                        if lines1[u][v] == target[u][v] and (categPerSpot[(u,v)] < categ or ((u,v) in categs[categ] and categs[categ].index((u,v)) < categs[categ].index((cy,cx)))):
                            continue

                        nLines[y][x], nLines[u][v], nLines[u1][v1] = nLines[u1][v1], nLines[y][x], nLines[u][v]
                        ny, nx = u, v

                        ll = []
                        for y2, line in sorted(nLines.items()):
                            for (x2, value) in sorted(line.items()):
                                ll.append(value)
                                if value == target[cy][cx]:
                                    ty, tx = y2,x2

                        hhh = tuple(ll)
                        if hhh not in visited:
                            visited.add(hhh)
                            q.put((ny, nx, path+str(mutation),nLines),abs(ny-ty)+abs(nx-tx)+10*(abs(ty-cy)+abs(tx-cx)))

                if q.empty() or (init_y, init_x, currentPath, lines) != (y, x, path, lines1):
                    continue

                spotsPerValue = {}
                score = len(currentPath)/1000000
                for y2,line in sorted(lines.items()):
                    for (x2,value) in sorted(line.items()):
                        spotsPerValue[value] = (y2,x2)
                for y1, line in target.items():
                    for (x1, value1) in line.items():
                        if value1 != 0:# pas grave car 3**0 == 1 et ça ne diminue pas trop le score
                            (y2,x2) = spotsPerValue[value1]
                            dy = abs(y2-y1)
                            dx = abs(x2-x1)
                            d = dy + dx - 0.5*min(2*dx,dy)
                            score += d

                if score <= M1:
                    M1 = score
                    print("oo",M1,(path if score < 1 else ""))
                    if M1 < 1:
                        f = open("best_score5.txt", "a")
                        f2 = open("best_score6.txt", "a")
                        f.write(path + "\n")
                        f2.write(str(M1) + "\n")
                        f.close()
                        f2.close()
                        if len(currentPath) < oldBest:
                            oldBest = len(currentPath)
                            print("maj oldBest", oldBest)

                    elif 70 < M1 < 95:
                        in_lines2 = deepcopy(lines)
                        (in_y2, in_x2) = (y, x)
                        ncurrentPath2 = path
                        nM2 = M1
                    elif initial_score / 10 < M1 < 25 + (initial_score / 10):
                        rebootOptions[10] = (deepcopy(lines), path, y, x, M1)
                        rebootOptionsList = list(rebootOptions.values())
                    elif initial_score / 5 < M1 < 25 + (initial_score / 5):
                        rebootOptions[5] = (deepcopy(lines), path, y, x, M1)
                        rebootOptionsList = list(rebootOptions.values())
                    elif initial_score / 20 < M1 < 25 + (initial_score / 20):
                        rebootOptions[20] = (deepcopy(lines), path, y, x, M1)
                        rebootOptionsList = list(rebootOptions.values())
                    elif initial_score / 2 < M1 < 25 + (initial_score / 2):
                        rebootOptions[2] = (deepcopy(lines), path, y, x, M1)
                        rebootOptionsList = list(rebootOptions.values())
                    elif initial_score / 3 < M1 < 25 + (initial_score / 3):
                        rebootOptions[3] = (deepcopy(lines), path, y, x, M1)
                        rebootOptionsList = list(rebootOptions.values())
                    elif initial_score / 30 < M1 < 25 + (initial_score / 30):
                        rebootOptions[30] = (deepcopy(lines), path, y, x, M1)
                        rebootOptionsList = list(rebootOptions.values())

                if score < 1:
                    print(path)
                    break
            if len(solved) < len(categs[categ]) and breakCounter[categ] < 8 and categ not in catkeys[-2:]:
                breaked = True
                breakCounter[categ] += 1
                break
            elif categ in catkeys[-3:]:
                breakCounter = defaultdict(int)
                print("restart breakcounter")
                if any(breakCounter[bct] >= 8 for bct in breakCounter):
                    nbSuccessiveReboots += 1
