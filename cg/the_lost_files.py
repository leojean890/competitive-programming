
import collections

def bfs(q):

    if not q:
        return
    node = q.pop()

    global visited

    while node in visited:
        global counterTiles
        counterTiles += 1
        if not q:
            return
        node = q.pop()

    visited.add(node)

    for neigh in neighs[node]:
        if neigh not in visited:
            q.appendleft(neigh)   

    return bfs(q)            

neighs = {}
e = int(input())

for i in range(e):
    n_1, n_2 = [int(j) for j in input().split()]
    if n_1 not in neighs:
        neighs[n_1] = []
    if n_2 not in neighs:
        neighs[n_2] = []
    neighs[n_1].append(n_2)    
    neighs[n_2].append(n_1)    

visited = set()
counterTiles = 0
counterContinents = 0

for node in neighs.keys():
    if node not in visited:
        counterContinents += 1
        q = collections.deque()
        q.appendleft(node)
        bfs(q)

print(counterContinents, counterTiles)
