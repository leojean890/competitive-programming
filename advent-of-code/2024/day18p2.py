from collections import deque
from time import process_time

start_time = process_time()
M = 3450
N = 1024
W = 71
start = (0,0)
exit = (W-1,W-1)

obstacles = {start}
for i in range(N):
    (x,y) = [int(j) for j in input().split(",")]
    obstacles.add((x,y))

for i in range(M-N):
    q = deque()
    q.appendleft((0, 0, 0))
    (x1,y1) = [int(j) for j in input().split(",")]
    obstacles.add((x1,y1))
    forbidden = obstacles.copy()
    found = False
    while q:
        (x,y,depth) = q.pop()
        if (x,y) == exit:
            found = True
            break

        for (a,b) in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
            if 0 <= a < W and 0 <= b < W and (a,b) not in forbidden:
                forbidden.add((a,b))
                q.appendleft((a,b,depth+1))
    if not found:
        print(process_time() - start_time, (x1,y1))  # 25.09375 (51, 40)
        break
