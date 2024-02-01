import heapq
import random
import sys
from collections import defaultdict, deque
from typing import List, Tuple


class PriorityQueue:
    def __init__(self):
        self.elements: List[Tuple[float, tuple]] = []

    def empty(self) -> bool:
        return not self.elements

    def put(self, item: tuple, priority: float):
        heapq.heappush(self.elements, (priority, item))

    def get(self) -> tuple:
        return heapq.heappop(self.elements)[1]


H = 81
W = 81
lines = []
portes = []
cles = []
blocked = {}
blocking = {}

# calcul des dists bfs entre 2 lettres
# lister les obstacles et cles du bfs entre 2 lettres

def bfs(p1,p2):
    q = deque()
    q.appendleft((p1[0],p1[1],0,set(),set()))
    visited = {p1}

    while q:
        (y,x,depth,obs,keys) = q.pop()
        if (y,x) == p2:
            return (depth, obs, keys)

        for (a,b) in ((y+1,x),(y-1,x),(y,x-1),(y,x+1)):
            # if lines[a][b] in cles and lines[a][b] != p2
            # => ne rien faire car parfois on doit accéder avant a une autre cle pour deverouiller la chaine
            if lines[a][b] != "#" and (a,b) not in visited:
                visited.add((a,b))
                if (a,b) in portes:
                    q.appendleft((a, b, depth + 1, obs | {(a, b)}, keys.copy()))
                elif (a, b) in cles and (a,b) not in (p1,p2):
                    q.appendleft((a,b,depth+1, obs.copy(), keys|{(a,b)}))
                else:
                    q.appendleft((a,b,depth+1,obs.copy(), keys.copy()))



for i in range(H):
    line = input()
    lines.append(line)
    for j in range(W):
        if line[j] not in "#.":
            if line[j] == "@":
                start = (i,j)
            elif line[j].isupper():
                portes.append((i,j))
                for (a,b) in cles:
                    if lines[a][b] == line[j].lower():
                        blocked[(a,b)] = (i,j)
                        blocking[(i,j)] = (a,b)
            else:
                cles.append((i,j))
                for (a,b) in portes:
                    if lines[a][b] == line[j].upper():
                        blocked[(i,j)] = (a,b)
                        blocking[(a,b)] = (i,j)


    for u in cles:
        if u not in blocked:
            blocked[u] = (-1,-1)

allDists = defaultdict(dict)
allObs = defaultdict(dict)
allKeys = defaultdict(dict)

for i in range(len(cles)):
    d, obs, keys = bfs(cles[i], start)
    allDists[cles[i]][start] = d
    allObs[cles[i]][start] = obs
    allKeys[cles[i]][start] = keys
    allDists[start][cles[i]] = d
    allObs[start][cles[i]] = obs
    allKeys[start][cles[i]] = keys

    for j in range(i+1, len(cles)):
        d, obs, keys = bfs(cles[i],cles[j])
        allDists[cles[i]][cles[j]] = d
        allObs[cles[i]][cles[j]] = obs
        allKeys[cles[i]][cles[j]] = keys
        allDists[cles[j]][cles[i]] = d
        allObs[cles[j]][cles[i]] = obs
        allKeys[cles[j]][cles[i]] = keys

(y,x) = start

#blocked : {cle:porte}, tant qu'il en reste, aller les chercher. enlever ensuite de blocked.
# ne pas prendre le chemin si l'un des obstacles est encore dans blocked.values()
# minimiser au global

q = PriorityQueue()
q.put((y,x,0,0,blocked),0)
M = sys.maxsize
it = 0
while not q.empty():
    it += 1
    (y, x, depth, aaa, blocked) = q.get()
    if it%100000 == 0:
        print(it, len(blocked),depth)
    if not blocked:
        if M > depth:
            M = depth
            print("BEST",M) # 4668
            # I found the best state after 2660000 iterations, luck ? Often, with other Astar params combinations, I was stuck at score 4686

        continue
    for a,b in blocked:
        # si j'ai pas de clés sur le chemin qui ne sont pas recup
        if (a,b) != (y,x) and all((i,j) not in blocked for (i,j) in allKeys[(y,x)][(a,b)]):
            for obs in allObs[(y,x)][(a,b)]:
                if blocking[obs] in blocked:
                    break
            else:
                nblocked = {}
                for c,d in blocked.items():
                    if c != (a,b):
                        nblocked[c] = d
                score = depth + allDists[(y, x)][(a, b)]
                q.put((a, b, score, random.randint(1, sys.maxsize), nblocked), score+10*len(allKeys[(y,x)][(a,b)])+200*len(nblocked))

