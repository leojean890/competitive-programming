
import sys
from collections import defaultdict, deque
sys.setrecursionlimit(10000000)
from functools import lru_cache
M = 0
sons = defaultdict(list)
parents = {} #defaultdict(list)
for line in sys.stdin:
    x, y = map(int, line.split())
    sons[x].append(y)
    if y not in parents:parents[y] = []
    parents[y].append(x)


def dfs(a, visited):
    global M

    for b in sons[a]:
        if b not in visited:
            dfs(b, visited+[b])
    if len(visited) == 1000:
        print(*visited)
        exit()

l = dfs(719,[719])
print(l)




def dfs1(a, visited):
    global M

    for b in sons[a]:
        if b not in visited:
            dfs1(b, visited+[b])
    if len(visited) > M:
        M = len(visited)
        print(M)
        if len(visited) == 1000:
            print(*visited)
            exit()


l = dfs1(719,[719])
print(l)

