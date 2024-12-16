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

q = PriorityQueue()
q.put((y,x,(dy,dx),0),0)
visited = {(y,x,dy,dx)}
while q:
    (y, x, d, depth) = q.get()
    if (y,x) == (ey,ex):
        print(process_time() - start_time, depth)  # 0.234375 72400
        exit()
    dy, dx = d
    r,c=y,x
    d2 = rl[(dy,dx)]
    if (r,c,d2[0],d2[1]) not in visited:
        q.put((y,x,d2,depth+1000),depth+1000)
        visited.add((r,c,d2[0],d2[1]))

    d2 = rr[(dy,dx)]
    if (r,c,d2[0],d2[1]) not in visited:
        q.put((y,x,d2,depth+1000),depth+1000)
        visited.add((r,c,d2[0],d2[1]))

    r,c=y+dy,x+dx
    if lines[r][c] != "#" and (r,c,dy,dx) not in visited:
        q.put((r,c,(dy,dx),depth+1),depth+1)
        visited.add((r,c,dy,dx))

