from collections import deque
from time import process_time

start_time = process_time()
N = 1024
W = 71
start = (0,0)
exit = (W-1,W-1)
q = deque()
q.appendleft((0,0,0))
forbidden = {start}
for i in range(N):
    (x,y) = [int(j) for j in input().split(",")]
    forbidden.add((x,y))

while q:
    (x,y,depth) = q.pop()
    if (x,y) == exit:
        print(process_time() - start_time, depth)  # 270 0.125
        exit()

    for (a,b) in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
        if 0 <= a < W and 0 <= b < W and (a,b) not in forbidden:
            forbidden.add((a,b))
            q.appendleft((a,b,depth+1))
            
