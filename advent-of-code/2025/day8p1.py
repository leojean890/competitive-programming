counter = 0
N = 1000#20
M= 1000#10

coords = []
for i in range(N):
    x,y,z = map(int, input().split(","))
    coords.append((x,y,z))


import collections
from itertools import combinations
import math


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
for ite in range(M):
    if isPathBetween(neighs,dists[current][1],dists[current][2]):
        current += 1
        continue
    (dist,u,v) = dists[current]
    if u not in neighs.keys():
        neighs[u] = []
    if v not in neighs.keys():
        neighs[v] = []
    neighs[u].append(v)
    neighs[v].append(u)

    aretes[(u,v)] = dist
    current += 1

# trouver les clusters via multiples dfs
# multiplier ensemble les tailles des 3 plus grosses CCs

visited = set()
clusterSizes = []
for elt in neighs:
    if elt not in visited:
        q = collections.deque()
        q.appendleft(elt)
        visited.add(elt)
        counter = 1
        while q:
            e = q.pop()
            for n in neighs[e]:
                if n not in visited:
                    q.appendleft(n)
                    visited.add(n)
                    counter += 1
        clusterSizes.append(counter)
clusterSizes.sort()
#clusterSizes.reverse()

print(clusterSizes,clusterSizes[-1]*clusterSizes[-2]*clusterSizes[-3]) # 103488
