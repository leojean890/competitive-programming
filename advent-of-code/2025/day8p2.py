
counter = 0
N = 1000#20
coords = []
for i in range(N):
    x,y,z = map(int, input().split(","))
    coords.append((x,y,z))


import collections
from itertools import combinations
import math

def complet(arbre):
    visited = set()
    q = collections.deque()
    q.appendleft(0)
    while q and len(visited) < N:
        current = q.pop()
        if current not in arbre.keys():
            return False
        for neigh in arbre[current]:
            if neigh not in visited:
                visited.add(neigh)
                q.appendleft(neigh)
    return (len(visited) == N)


def isPathBetween(arbre,n1,n2):
    visited = set()
    q = collections.deque()
    q.appendleft(n1)
    while q:
        current = q.pop()
        if current not in arbre.keys():
            return False
        for neigh in arbre[current]:
            if neigh == n2:
                return True
            if neigh not in visited:
                visited.add(neigh)
                q.appendleft(neigh)

    q = collections.deque()
    q.appendleft(n2)
    while q:
        current = q.pop()
        if current not in arbre.keys():
            return False
        for neigh in arbre[current]:
            if neigh == n1:
                return True
            if neigh not in visited:
                visited.add(neigh)
                q.appendleft(neigh)

    return False


dists = [(math.dist(coords[v1], coords[v2]),v1, v2) for v1, v2 in combinations(range(len(coords)), 2)]
dists.sort()

neighs = {}
aretes = {}
current = 0
while not complet(neighs):
    if isPathBetween(neighs,dists[current][1],dists[current][2]):
        current += 1
        continue
    print(current)
    (dist,u,v) = dists[current]
    if u not in neighs.keys():
        neighs[u] = []
    if v not in neighs.keys():
        neighs[v] = []
    neighs[u].append(v)
    neighs[v].append(u)
    print(coords[u],coords[v])

    aretes[(u,v)] = dist
    current += 1
    print(coords[u][0]*coords[v][0]) # 8759985540
