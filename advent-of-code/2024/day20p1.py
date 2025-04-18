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
q.appendleft((sy, sx, 0, [(sy,sx)]))
while q:
    (y,x,depth,path) = q.pop()
    if (y,x) == end:
        mDepth = depth
        break

    for (a,b) in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
        if 0 <= a < N and 0 <= b < N and (b,a) not in visited and (b,a) not in obstacles:
            visited.add((b,a))
            q.appendleft((b,a,depth+1,path+[(b,a)]))

# lors du premier passage, on garde la durée utilisée entre chaque paire de cases
# ensuite on garde pour chaque mur les distances entre ses 2 voisins et le début et la fin
# on prend alors la somme des 2 plus courts + 1

counter = 0

for i in range(len(path)-1):
    (a,b) = path[i]
    for j in range(i+1,len(path)):
        (y, x) = path[j]
        if abs(a-y) + abs(b-x) == 2:
            depth = i+1+len(path)-j
            if mDepth - depth >= 100: counter += 1

print(process_time() - start_time, counter) # 20.578125 1369
