import sys
from time import process_time
import heapq
from typing import List, Tuple


class PriorityQueue:
    def __init__(self):
        self.elements: List[Tuple[tuple, tuple]] = []

    def empty(self) -> bool:
        return not self.elements

    def put(self, item: tuple, priority: tuple):
        heapq.heappush(self.elements, (priority, item))

    def get(self) -> tuple:
        return heapq.heappop(self.elements)[1]


rl = {(0,1):(1,0),(1,0):(0,-1),(0,-1):(-1,0),(-1,0):(0,1)}
rr = {(1,0):(0,1),(0,-1):(1,0),(-1,0):(0,-1),(0,1):(-1,0)}


start_time = process_time()
lines = []
N = 141
for i in range(N):
    lines.append(list(input()))
    for j in range(N):
        if lines[i][j] == "S":
            y,x,dy,dx=i,j,0,1
        if lines[i][j] == "E":
            ey,ex,dy,dx=i,j,0,1


shortest = sys.maxsize
dy,dx=0,1
q = PriorityQueue()
q.put((y,x,(dy,dx),{(y,x,dy,dx)},0),0)
visited = {}
allVisited = {}
visitedTiles = {(y,x)}
while not q.empty():
    (y, x, d,path,depth) = q.get()
    if depth > shortest:
        continue
    if (y,x) == (ey,ex):
        shortest = depth
        for (r,c,dd,ee) in path:
            visitedTiles.add((r, c))
        continue
    dy, dx = d
    r,c=y,x
    d2 = rl[(dy,dx)]
    if (r,c,d2[0],d2[1]) not in path and ((r,c,d2[0],d2[1]) not in visited or visited[(r,c,d2[0],d2[1])] >= depth+1000):
        q.put((y,x,d2,path|{(r,c,d2[0],d2[1])},depth+1000),depth+1000)
        visited[(r,c,d2[0],d2[1])] = depth+1000

    d2 = rr[(dy,dx)]
    if (r,c,d2[0],d2[1]) not in path and ((r,c,d2[0],d2[1]) not in visited or visited[(r,c,d2[0],d2[1])] >= depth+1000):
        q.put((y,x,d2,path|{(r,c,d2[0],d2[1])},depth+1000),depth+1000)
        visited[(r,c,d2[0],d2[1])] = depth+1000

    r,c=y+dy,x+dx
    if (r,c,dy,dx) not in path and lines[r][c] != "#" and ((r,c,dy,dx) not in visited or visited[(r,c,dy,dx)] >= depth+1):
        q.put((r,c,(dy,dx),path|{(r,c,dy,dx)},depth+1),depth+1)
        visited[(r,c,dy,dx)] = depth+1


print(len(visitedTiles),process_time() - start_time) # 435 2.15625
