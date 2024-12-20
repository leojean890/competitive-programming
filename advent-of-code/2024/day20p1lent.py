from collections import deque, defaultdict
from time import process_time

start_time = process_time()
N = 141
lines = []
obstacles = set()
visited = set()
for i in range(N):
    line = input()
    lines.append(list(line))
    for j in range(N):
        if line[j] == "S":
            (sy,sx) = (i,j)
        elif line[j] == "E":
            end = (i,j)
        elif line[j] == "#":
            obstacles.add((i,j))

q = deque()
q.appendleft((sy, sx, 0, {(sy,sx)}))
while q:
    (y,x,depth,path) = q.pop()
    if (y,x) == end:
        mDepth = depth
        break

    for (a,b) in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
        if 0 <= a < N and 0 <= b < N and (b,a) not in visited and (b,a) not in obstacles:
            visited.add((b,a))
            q.appendleft((b,a,depth+1,path|{(b,a)}))

nobs = []
for (a,b) in obstacles:
    if any(abs(a-y) + abs(b-x) == 1 for (y,x) in path):
        nobs.append((a,b))

counter = 0
for incr in range(len(nobs)):
    (a, b) = nobs[incr]
    if not incr%100:
        print(process_time() - start_time, incr,len(nobs))
    nlines = []
    for i in range(N):
        nlines.append(lines[i].copy())
    nlines[a][b] = "."
    visited = set()

    q = deque()
    q.appendleft((sy, sx, 0))
    while q:
        (y,x,depth) = q.pop()
        if (y,x) == end:
            if mDepth-depth >= 100:counter+= 1
            break

        for (a,b) in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
            if 0 <= a < N and 0 <= b < N and (b,a) not in visited and nlines[b][a] != "#":
                visited.add((b,a))
                q.appendleft((b,a,depth+1))
print(process_time() - start_time, counter) # 607.4375 1369
